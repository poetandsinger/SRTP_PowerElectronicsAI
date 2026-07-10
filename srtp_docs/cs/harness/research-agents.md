---
title: Research-Specific Agents
type: topic
field: cs
created: 2026-07-06
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [cs, multi-agent, review, benchmark]
---

## Overview

These agents are **not general-purpose harnesses** — they are purpose-built for specific research tasks. In practice, they are typically integrated as **sub-components** within a larger agent framework (such as Hermes, LangGraph, or CrewAI), rather than used as the primary harness.

---

## PaperQA2 — Scientific Literature Q&A

> **Repo:** [github.com/Future-House/paper-qa](https://github.com/Future-House/paper-qa)  
> **Stars:** 8,822 | **License:** Apache 2.0 | **Language:** Python

### Architecture

PaperQA2 implements **agentic RAG** for scientific literature:

```
1. DOCUMENT INGESTION
   PDFs → Parse → Extract metadata (Semantic Scholar/Crossref)
   → Citation counts, journal quality, retraction status
   → Build Tantivy full-text search index

2. AGENTIC RAG LOOP
   User query → LLM generates search queries → Search index
   → Gather evidence → LLM re-ranks (RCS) → Refine query
   → Repeat until sufficient evidence → Generate answer with citations

3. ANSWER GENERATION
   Evidence-based answer with inline citations
   Every claim has a verifiable source
```

### Key Features
- **Metadata-aware:** Papers weighted by citation count, journal quality, retraction status
- **Agentic refinement:** LLM iteratively improves search queries for better evidence
- **Citation-grounded:** Every claim linked to source — critical for research integrity
- **CLI tool:** `pqa ask "What are the switching loss models for SiC MOSFETs?"`
- **Model-agnostic:** LiteLLM supports any LLM provider

### Research Use: Literature Review Sub-Agent

```python
# Within a LangGraph or CrewAI pipeline:
literature_context = paperqa.query(
    "State-of-the-art efficiency of 800V SiC traction inverters",
    corpus_path="papers/power_electronics/"
)
# → Returns cited evidence for agent to use in design decisions
```

### Limitations
- **No simulation** — pure document Q&A
- **No experiment design** — can't propose or validate topologies
- **Corpus-dependent** — quality limited by ingested papers

---

## GPT Researcher — Deep Web Research

> **Repo:** [github.com/assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher)  
> **Stars:** 28,107 | **License:** Apache 2.0 | **Language:** Python

### Architecture

```
Planner Agent → Generates research questions from topic
       ↓
Execution Agents (parallel) → Each scrapes + summarizes for one question
       ↓
Publisher Agent → Aggregates findings into report (PDF/Word/Markdown)
```

### Key Features
- **Plan-and-Solve:** Decomposes broad topics into answerable questions
- **Parallel execution:** Multiple crawlers work simultaneously (20+ sources)
- **JavaScript scraping:** Handles dynamic pages (datasheets, vendor sites)
- **MCP integration:** Connect to custom data sources (component databases)
- **Multi-format export:** PDF, Word, Markdown reports

### Research Use: Component/Market Research

```python
# Research available SiC MOSFET modules for 800V inverter:
report = gpt_researcher.research(
    "Available 1200V SiC MOSFET power modules from Wolfspeed, Infineon, onsemi, STMicro in 2026"
)
# → Returns structured report with specs, pricing, availability
```

### Limitations
- **Opinionated toward web research** — hard to add simulation loops
- **No iterative refinement** — one-pass research, not iterative like LangGraph
- **Report-focused** — output is a document, not structured data for further processing

---

## STORM (Stanford) — Multi-Perspective Report Generation

> **Repo:** [github.com/stanford-oval/storm](https://github.com/stanford-oval/storm)  
> **Stars:** 29,864 | **License:** MIT | **Language:** Python

### Architecture

```
1. PERSPECTIVE-DRIVEN QUESTION ASKING
   Simulated conversation: "Writer" interviews multiple "Expert" personas
   Each expert brings different perspective → diverse questions

2. MULTI-TURN INFORMATION GATHERING
   For each question: web search → retrieval → answer synthesis
   Builds comprehensive knowledge base

3. OUTLINE GENERATION
   Organize gathered information into structured outline

4. FULL-LENGTH ARTICLE GENERATION
   Write section-by-section with citations
```

### Key Features
- **Multi-perspective:** Generates questions from different viewpoints (e.g., thermal expert, EMI expert, reliability expert, cost expert)
- **Conversation simulation:** Writer interviews experts — more thorough than single-pass Q&A
- **Full reports:** Generates complete articles with citations
- **Customizable perspectives:** Define your own expert personas

### Research Use: Report Generation

```python
# Define power electronics expert perspectives:
perspectives = [
    "Power Electronics Design Engineer",
    "Thermal Management Specialist", 
    "EMI/EMC Compliance Engineer",
    "Reliability Engineer (physics of failure)",
    "Cost/Manufacturing Engineer"
]

report = storm.generate_report(
    topic="Design considerations for 800V SiC traction inverter",
    perspectives=perspectives
)
# → Comprehensive report covering all engineering perspectives
```

### Limitations
- **Information synthesis only** — no simulation, no experiment
- **Web-grounded** — quality limited by available web content
- **No iterative refinement** — generated report is final; no feedback loop

---

## Comparison

| Feature | PaperQA2 | GPT Researcher | STORM |
|---------|:---:|:---:|:---:|
| **Primary function** | Scientific Q&A | Web research + report | Multi-perspective report |
| **Source type** | Academic papers (PDFs) | Web pages + APIs | Web pages |
| **Citation quality** | 🟢 Excellent (verified metadata) | 🟡 Good (URL-based) | 🟡 Good (URL-based) |
| **Iterative refinement** | ✅ Agentic query loop | ❌ One-pass | ❌ One-pass |
| **Multi-perspective** | ❌ Single query | ❌ Single topic | ✅ Core feature |
| **Report format** | Answer + citations | PDF/Word/Markdown | Full article |
| **MATLAB integration** | ❌ None | ❌ None | ❌ None |
| **Best for** | Literature grounding | Market/component research | Final report writing |

## Integration Strategy

These agents should **not** be the primary harness. Instead:

```
┌──────────────────────────────────────────────────┐
│         PRIMARY HARNESS (Hermes/LangGraph/CrewAI) │
│                                                    │
│  ┌──────────────┐  ┌──────────┐  ┌─────────────┐ │
│  │ PaperQA2     │  │ GPT      │  │ STORM       │ │
│  │ Literature   │  │ Researcher│  │ Report      │ │
│  │ Grounding    │  │ Component │  │ Generation  │ │
│  │              │  │ Research  │  │             │ │
│  └──────┬───────┘  └────┬─────┘  └──────┬──────┘ │
│         │               │               │         │
│         ▼               ▼               ▼         │
│  ┌─────────────────────────────────────────────┐ │
│  │         MATLAB SIMULATION ENGINE             │ │
│  │  (Custom tool — the core differentiator)     │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Flow:**
1. PaperQA2 grounds the design in published research → provides cited evidence
2. GPT Researcher finds available components matching the specs → provides options
3. MATLAB tool simulates the design with real component models → produces results
4. STORM generates the final report with multi-perspective analysis → delivers output


> **References:** [[citations]]


← [[cs/harness/crewai|Prev: CrewAI]] | [[cs/harness/autogen|Next: AutoGen]] → | [[README]]
