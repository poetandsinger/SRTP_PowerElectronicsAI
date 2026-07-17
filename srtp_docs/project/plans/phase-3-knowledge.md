---
title: Phase 3 — Knowledge + Components
type: plan
field: project
created: 2026-07-06
updated: 2026-07-10
tags: [plan]
---

# Phase 3 — Knowledge + Components (Weeks 9-10)

> **Part of:** [[plans-index|Plan Index]]
> **Goal:** Literature agent (PaperQA2), component agent (Nexar API), persistent memory. Agent selects real components and cites real papers.
> **Architecture:** PaperQA2 + Nexar GraphQL + SQLite/LanceDB dual memory store

---

## Context

Phase 1-2 agents simulated inverters with idealized components and no literature grounding. Phase 3 connects the agent to the real world:
- **Literature Agent:** Finds real papers, cites real baselines, grounds design decisions in published work
- **Component Agent:** Selects real parts from DigiKey/Mouser/Arrow (via Nexar API) with verified specs
- **Memory:** Remembers designs, components, papers across sessions

This is where the agent transitions from "toy prototype" to "research tool."

---

## Week 9: Literature Agent

### P3.1 — PaperQA2 Integration (Days 1-3)

```python
# src/srtp_ai/agents/literature.py
from paperqa import Settings, Docs, agent_query

class LiteratureAgent:
    """
    Literature review agent using PaperQA2 for citation-grounded answers.
    
    Model: claude-sonnet (best for deep reading and synthesis)
    PaperQA2 algorithm: Search → Gather Evidence → Generate Answer (with citations)
    """
    
    model = "claude-sonnet"
    
    def __init__(self, papers_dir: str = "papers/"):
        self.settings = Settings(
            llm="claude-sonnet",
            summary_llm="claude-sonnet",
            embedding="text-embedding-3-small",
            temperature=0.1,
            paper_directory=papers_dir,
            agent=AgentSettings(
                agent_llm="claude-sonnet",
                search_count=8,        # Search breadth
                timeout=300.0,          # 5 min timeout for complex queries
            ),
            answer=dict(
                evidence_k=10,          # Evidence chunks to retrieve
                answer_max_sources=6,   # Max cited sources
                evidence_summary_length="about 100 words",
                answer_length="about 200 words",
            ),
        )
        self.docs = Docs()
    
    async def search_papers(self, query: str) -> list[dict]:
        """Search arXiv + Semantic Scholar for relevant papers."""
        # PaperQA2 handles the search internally
        # Returns papers added to Docs with metadata
        ...
    
    async def answer_question(self, question: str) -> dict:
        """
        Answer a domain question with citations.
        
        Example queries:
        - "What is the state-of-the-art efficiency for 800V SiC traction inverters?"
        - "What are the key failure modes of SiC MOSFETs in automotive applications?"
        - "Compare 2L-B6 vs 3L-TNPC efficiency at 800V 200kW"
        """
        response = await agent_query(
            query=question,
            settings=self.settings,
        )
        
        return {
            "answer": response.answer,
            "citations": response.context,  # PaperQA2 provides cited sources
            "confidence": self._estimate_confidence(response),
        }
    
    def review_literature(self, spec: InverterSpec) -> LiteratureReport:
        """
        Systematic literature review for an inverter design spec.
        
        Queries:
        1. Baseline efficiency: best published efficiency for this voltage/power class
        2. Topology comparison: papers comparing topologies at this voltage
        3. Component recommendations: SiC MOSFETs used in similar designs
        4. Control strategies: FOC vs MPC at this power level
        5. EMI mitigation: dv/dt filtering approaches for this voltage class
        """
        questions = [
            f"What is the best demonstrated efficiency for a {spec.vdc}V {spec.pout}kW traction inverter?",
            f"Compare 2-level vs 3-level inverter topologies at {spec.vdc}V for EV traction",
            f"What SiC MOSFET modules are recommended for {spec.vdc}V {spec.pout}kW traction inverters?",
            f"What control strategy achieves the best efficiency for {spec.pout}kW PMSM drives?",
            f"How to mitigate dv/dt EMI in {spec.vdc}V SiC traction inverters?",
        ]
        
        findings = [await self.answer_question(q) for q in questions]
        
        return LiteratureReport(
            baseline_efficiency=self._extract_baseline(findings[0]),
            topology_comparison=findings[1],
            component_recommendations=findings[2],
            control_recommendations=findings[3],
            emi_approaches=findings[4],
            paper_count=sum(len(f["citations"]) for f in findings),
        )
```

**Deliverable:** Literature agent that answers 5 domain questions with real citations.
**Verify:** Query 3 questions → manually verify 5 citations are real papers. ≥ 80% must be real.

### P3.2 — Citation Verification (Days 3-4)

PaperQA2 can hallucinate citations. Cross-check with arXiv API:

```python
# src/srtp_ai/agents/citation_checker.py
import arxiv

class CitationChecker:
    """Cross-check PaperQA2 citations against arXiv API."""
    
    def verify(self, citation: dict) -> dict:
        """Verify a citation is real and retrievable."""
        try:
            search = arxiv.Search(id_list=[citation.get("arxiv_id")])
            paper = next(search.results())
            return {
                "verified": True,
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "published": paper.published,
                "match_score": self._title_similarity(citation["title"], paper.title),
            }
        except Exception:
            return {"verified": False, "error": "Not found on arXiv"}
```

**Deliverable:** Citation verifier. Flag unverifiable citations.
**Verify:** Run against 20 PaperQA2 citations → ≥ 90% verified.

---

## Week 10: Component Agent + Memory

### P3.3 — Nexar Component Agent (Days 5-7)

```python
# src/srtp_ai/agents/component.py
import httpx

class ComponentAgent:
    """
    Component selection agent using Nexar GraphQL API.
    
    Covers 30+ distributors: DigiKey, Mouser, Arrow, Avnet, Farnell, LCSC.
    Free tier: ~1,000 queries/month.
    """
    
    NEXAR_API = "https://api.nexar.com/graphql"
    NEXAR_AUTH = "https://identity.nexar.com/connect/token"
    
    async def search_components(self, spec: dict) -> list[dict]:
        """
        Search for components matching electrical specs.
        
        Queries:
        - MOSFETs: Vds ≥ 1.5×Vdc, Id ≥ rated, Rds(on) minimized
        - Gate drivers: isolated, ±10A peak, desat detection
        - DC-link caps: film, 500+Vdc, ESR < 1mΩ, ripple current rated
        - Current sensors: isolated, 50+kHz bandwidth, ±1% accuracy
        """
        queries = [
            self._mosfet_query(spec),
            self._gate_driver_query(spec),
            self._dc_link_cap_query(spec),
            self._current_sensor_query(spec),
        ]
        
        results = await asyncio.gather(*queries)
        return self._select_best(results, spec)
    
    async def _mosfet_query(self, spec: dict) -> list[dict]:
        query = """
        query SearchSiCMOSFET($q: String!, $limit: Int!) {
          supSearch(q: $q, limit: $limit) {
            results {
              part {
                mpn
                manufacturer { name }
                specs {
                  attribute
                  displayValue
                }
                medianPrice1000 {
                  price
                  currency
                }
                sellers {
                  company { name }
                  offers {
                    inventoryLevel
                    moq
                    prices { quantity price }
                  }
                }
              }
            }
          }
        }
        """
        
        # Search for SiC MOSFET modules
        voltage_class = spec["vdc"] * 1.5  # 1.5× margin for SiC
        current_class = spec["pout"] * 1000 / (1.732 * spec["vdc"]) * 1.2  # 20% margin
        
        q = f"SiC MOSFET module {voltage_class}V {current_class}A automotive"
        variables = {"q": q, "limit": 20}
        
        async with httpx.AsyncClient() as client:
            token = await self._get_token()
            headers = {"Authorization": f"Bearer {token}"}
            response = await client.post(
                self.NEXAR_API,
                json={"query": query, "variables": variables},
                headers=headers,
            )
            return response.json()["data"]["supSearch"]["results"]
```

**Deliverable:** Component agent that searches and selects real components.
**Verify:** Search for SiC MOSFETs for 800V 150kW → returns real parts with MPNs and prices.

### P3.4 — Component Validation (Days 7-8)

```python
# src/srtp_ai/agents/component_validator.py
class ComponentValidator:
    """Validate selected components against design requirements."""
    
    def validate_mosfet(self, mosfet: dict, spec: dict) -> list[str]:
        violations = []
        
        # Voltage rating check
        vds_rating = self._extract_spec(mosfet, "Drain-Source Voltage")
        if vds_rating and vds_rating < spec["vdc"] * 1.2:
            violations.append(f"Vds rating {vds_rating}V < 1.2×{spec['vdc']}V")
        
        # Current rating check
        id_rating = self._extract_spec(mosfet, "Continuous Drain Current")
        required_id = spec["pout"] * 1000 / (1.732 * spec["vdc"])
        if id_rating and id_rating < required_id * 1.2:
            violations.append(f"Id rating {id_rating}A < required {required_id*1.2:.0f}A")
        
        # Package check (automotive qualified?)
        if "AEC-Q101" not in str(mosfet.get("qualifications", "")):
            violations.append("Not AEC-Q101 qualified (automotive)")
        
        return violations
```

**Deliverable:** Component validator catching specs mismatches.
**Verify:** Feed 10 components with intentional spec violations → all caught.

### P3.5 — Persistent Memory (Days 8-10)

```python
# src/srtp_ai/memory.py
import sqlite3
import lancedb
import json

class MemoryStore:
    """
    Dual memory: SQLite (structured) + LanceDB (vector/semantic).
    
    Pattern: CrewAI unified memory (v0.80+) + PE-MAS lifelong memory.
    """
    
    def __init__(self):
        self.structured = sqlite3.connect("srtp_memory.db")
        self.vector = lancedb.connect("srtp_vectors")
        self._init_tables()
    
    def _init_tables(self):
        """Create schema for design records, components, papers, iterations."""
        self.structured.executescript("""
            CREATE TABLE IF NOT EXISTS designs (
                id TEXT PRIMARY KEY,          -- SHA256 of spec
                spec_json TEXT,                -- Full spec
                topology TEXT,
                efficiency REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                best_design BOOLEAN DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS components (
                mpn TEXT PRIMARY KEY,
                manufacturer TEXT,
                category TEXT,
                specs_json TEXT,
                used_in_design TEXT,          -- FK to designs.id
                verified_at TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS papers (
                arxiv_id TEXT PRIMARY KEY,
                title TEXT,
                authors TEXT,
                key_findings TEXT,
                cited_in_design TEXT,
                verified BOOLEAN DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS iterations (
                design_id TEXT,
                iteration INTEGER,
                efficiency REAL,
                issues_found TEXT,
                fixes_applied TEXT,
                wall_time_seconds REAL,
                token_cost REAL,
                PRIMARY KEY (design_id, iteration)
            );
            CREATE TABLE IF NOT EXISTS guardrail_violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                design_id TEXT,
                iteration INTEGER,
                violation TEXT,
                resolved BOOLEAN DEFAULT 0,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    
    def save_design(self, state: DesignState):
        """Save a completed design with all its context."""
        design_id = hashlib.sha256(json.dumps(state["spec"]).encode()).hexdigest()[:16]
        
        # Check if this beats the previous best for this spec
        prev_best = self.structured.execute(
            "SELECT efficiency FROM designs WHERE id = ? AND best_design = 1",
            (design_id,)
        ).fetchone()
        
        is_best = not prev_best or state["simulation_results"]["efficiency"] > prev_best[0]
        
        if is_best:
            # Update: this is the new best
            self.structured.execute(
                "UPDATE designs SET best_design = 0 WHERE id = ?", (design_id,)
            )
        
        self.structured.execute(
            """INSERT OR REPLACE INTO designs (id, spec_json, topology, efficiency, best_design)
               VALUES (?, ?, ?, ?, ?)""",
            (design_id, json.dumps(state["spec"]), state["topology"],
             state["simulation_results"]["efficiency"], is_best)
        )
        
        # Save iteration history
        self.structured.execute(
            """INSERT INTO iterations (design_id, iteration, efficiency, issues_found, fixes_applied, wall_time_seconds, token_cost)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (design_id, state["iteration"], state["simulation_results"]["efficiency"],
             json.dumps(state.get("review_findings", [])),
             json.dumps(state.get("fixes", [])),
             state.get("wall_time", 0), state.get("token_cost", 0))
        )
    
    def recall_similar(self, spec: dict, k: int = 3) -> list[dict]:
        """Find similar past designs using LanceDB semantic search."""
        query_vector = self._embed(json.dumps(spec))
        results = self.vector_table.search(query_vector).limit(k).to_list()
        return results
    
    def get_iteration_playbook(self, issue_type: str) -> list[str]:
        """PE-MAS pattern: learn which fixes work for which failure modes."""
        rows = self.structured.execute(
            """SELECT fixes_applied FROM iterations
               WHERE issues_found LIKE ?
               ORDER BY efficiency DESC LIMIT 5""",
            (f"%{issue_type}%",)
        ).fetchall()
        return [json.loads(r[0]) for r in rows if r[0]]
```

**Deliverable:** Dual memory store with design records, component DB, paper index, iteration playbooks.
**Verify:** Design 3 inverters. Restart process. Recall previous designs → results match. Iteration playbooks populated.

---

## Phase 3 Checklist

- [ ] P3.1: Literature agent answers 5 domain questions with real citations
- [ ] P3.2: Citation verifier confirms ≥ 90% of PaperQA2 citations are real
- [ ] P3.3: Component agent searches Nexar and selects real SiC MOSFETs, gate drivers, caps
- [ ] P3.4: Component validator catches 10/10 spec mismatches
- [ ] P3.5: Memory store persists designs, components, papers across sessions
- [ ] P3.6: Agent uses real literature baselines for efficiency comparison
- [ ] P3.7: Agent uses real component MPNs (not idealized params)

## Phase 3 Acceptance

1. Literature agent: designs cite real, verifiable papers (≥ 80% verification rate)
2. Component agent: designs use real component MPNs with verified specs
3. Memory: designs persist across sessions; iteration playbooks capture which fixes work
4. Full pipeline: spec → lit review → component search → simulate → review (all with real data)

---

← [[project/plans/phase-2-simulation]] | [[project/plans/phase-4-production]] →
