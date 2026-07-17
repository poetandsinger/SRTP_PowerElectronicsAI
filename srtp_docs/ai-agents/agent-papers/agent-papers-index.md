---
title: Agent Architectures from Research & Production
type: map
field: ai-agents
created: 2026-07-06
updated: 2026-07-08
tags: [ai-agents, multi-agent, index, review]
---

## Scope

This note surveys agent architectures from three sources beyond GitHub:
1. **Academic papers** — foundational agent architectures (ReAct, Toolformer, etc.)
2. **Production AI-for-engineering** — EDA tools, scientific discovery platforms
3. **Multi-agent research systems** — ChemCrow, Coscientist, and similar simulation+AI systems

> ⚠️ **Verification note:** Some entries are from LLM training knowledge (cutoff-dependent). [V] marks verified entries; [T] marks training-knowledge entries needing live verification.

## Foundational Agent Architectures (Papers)

### ReAct: Synergizing Reasoning and Acting in Language Models
- **Authors:** Yao et al. (2023)
- **Venue:** ICLR 2023
- **Key idea:** Interleave reasoning traces with action steps. LLM generates "Thought: ... Action: ... Observation: ..." sequences rather than separating reasoning from tool use.
- **Architecture:** The model generates reasoning traces (chain-of-thought) that include explicit action invocations. Tool outputs are interleaved as observations.
- **Relevance to research agents:** This is the foundational pattern used by ALL surveyed harnesses. The key insight — interleaving reasoning with tool calls — is universal.
- **Limitation:** ReAct alone doesn't handle multi-step tool chaining, error recovery, or state management that modern frameworks add.

### Toolformer: Language Models Can Teach Themselves to Use Tools
- **Authors:** Schick et al. (2023)
- **Venue:** NeurIPS 2023
- **Key idea:** LLMs can learn to use tools (calculator, search, calendar, etc.) via self-supervised training. The model annotates its own training data with API calls.
- **Architecture:** Fine-tuning approach — the model learns to insert special tokens `[Calculator(...) → result]` inline during text generation. Tools are invoked, results inserted, generation continues.
- **Relevance:** Inline tool-use pattern vs. the more common "tool call → separate response" pattern. This is more efficient for simple tools but less flexible for complex multi-step operations.
- **Limitation:** Static tool set defined at training time. Cannot dynamically add new tools (like MATLAB).

### AutoGPT / BabyAGI
- **Authors:** Significant Gravitas (AutoGPT), Nakajima (BabyAGI) — 2023 open-source projects
- **Key idea:** Autonomous agent that recursively decomposes goals into subtasks, executes them, and integrates results. Self-prompting: the agent generates its own next task.
- **Architecture:** Goal → Task list → Execute next task → Add results to memory → Generate new tasks → Prioritize → Loop. Uses vector memory for long-term context.
- **Relevance:** The task-decomposition pattern is directly applicable to research. A "Design 800V SiC inverter" goal can be auto-decomposed into topology selection, component sizing, simulation, analysis.
- **Limitation:** Often gets stuck in loops. Task decomposition quality is highly variable. No built-in validation or simulation capabilities.

### SWE-bench / SWE-agent
- **Authors:** Jimenez et al. (2024), Yang et al. (2024)
- **Key idea:** Benchmark and agent for real-world software engineering tasks. SWE-agent uses a custom Agent-Computer Interface (ACI) with specialized tools for code navigation and editing.
- **Architecture:** Custom toolset (file viewer, editor, search with regex, test runner) + ReAct loop. The ACI is designed to give the agent structured, actionable views of the codebase.
- **Relevance:** The ACI concept — designing tools specifically for the agent's perception, not for humans. A "Simulation-Computer Interface" for MATLAB could provide structured simulation results.
- **Limitation:** Coding-specific. The ACI pattern transfers to research but the tools are domain-specific.

### Voyager: An Open-Ended Embodied Agent with LLMs
- **Authors:** Wang et al. (2023)
- **Key idea:** Agent in Minecraft that writes, stores, and retrieves skills (JavaScript code) from a skill library. Automatic curriculum: the agent proposes increasingly difficult tasks.
- **Architecture:** Three components: (1) Automatic curriculum (proposes tasks based on current state), (2) Skill library (stores + retrieves successful programs), (3) Iterative prompting (generates code, gets feedback from environment, refines).
- **Relevance:** The skill library concept is analogous to Hermes Agent's skills system. Automatic curriculum could drive increasingly complex simulation scenarios (buck converter → boost converter → inverter → multilevel).
- **Limitation:** Minecraft-specific environment. Skill encoding as code works well for deterministic environments but less so for noisy simulation results.

## Production AI-for-Engineering Systems

### Synopsys DSO.ai (Design Space Optimization)
- **Company:** Synopsys
- **Domain:** Electronic Design Automation (chip design)
- **What it does:** AI-driven exploration of chip design space — placement, routing, timing optimization. Uses reinforcement learning to navigate enormous design spaces.
- **Architecture:** RL agent explores design parameters → evaluates with EDA tools (simulation) → receives reward (power, performance, area) → updates policy → iterates.
- **Relevance to power electronics:** This is the closest production analog to what we're building. DSO.ai automates the "design → simulate → evaluate → redesign" loop that is central to traction inverter design. Key insight: the simulation tool is treated as an oracle that the AI agent queries.
- **Key takeaway:** Production AI-for-engineering tools don't replace simulation — they wrap it. The simulation is the ground truth; AI guides exploration.

### Cadence Cerebrus
- **Company:** Cadence Design Systems
- **Domain:** Chip physical design optimization
- **What it does:** RL-based chip floorplanning and optimization. Similar to DSO.ai — ML-guided design space exploration backed by physics-based simulation.
- **Key takeaway:** The same pattern as DSO.ai — AI navigates the design space, simulation validates. This is the architectural pattern to replicate for traction inverter design.

### ChemCrow: Augmenting LLMs with Chemistry Tools
- **Authors:** Bran et al. (2024)
- **Key idea:** Give an LLM access to chemistry-specific tools (molecule synthesis planning, property prediction, safety assessment) via a ReAct agent loop.
- **Architecture:** 17 specialized chemistry tools (RDKit, molecular docking, synthesis planner, etc.) exposed to the LLM via tool-calling. The LLM plans multi-step chemistry workflows.
- **Relevance:** ChemCrow is the closest research analog to a MATLAB-integrated research agent. It augments an LLM with domain-specific simulation/calculation tools rather than expecting the LLM to know chemistry.
- **Key takeaway:** The "LLM as orchestrator + domain tools as executors" pattern is proven in chemistry. The same pattern works for power electronics: LLM plans, MATLAB simulates.

### Coscientist
- **Authors:** Boiko et al. (2023)
- **Key idea:** An LLM-based agent that autonomously designs and executes chemical experiments using lab automation equipment (liquid handlers, plate readers).
- **Architecture:** LLM plans experiment → generates Python code → code controls lab robots → results analyzed → replan. Closed-loop autonomous science.
- **Relevance:** The closed-loop "plan → execute → analyze → replan" cycle maps directly to "design inverter → simulate → analyze efficiency → redesign." Coscientist proves this loop works with real physical equipment.
- **Key takeaway:** Combining LLM reasoning with automated execution (robots there, MATLAB here) produces autonomous scientific discovery. The architecture transfers.

### AlphaFold / AlphaDev / GNoME (DeepMind)
- **Company:** Google DeepMind
- **Domain:** Protein structure prediction, algorithm discovery, materials discovery
- **What they do:** AI systems that discover new knowledge (protein structures, faster algorithms, new materials) through a combination of deep learning and search/optimization.
- **Architecture pattern:** Train a model on known data → model generates candidates → candidates evaluated by physics simulation or experiment → results feed back to improve model.
- **Relevance:** DeepMind's "AI + physics simulation" pattern is the gold standard. For traction inverters, this could mean: train on known inverter designs → generate novel topologies → evaluate with MATLAB/Simulink → learn from results.
- **Key takeaway:** The simulation is not optional — it's the ground truth that validates AI-generated designs.

## Emerging: AI-Native EDA Tools

Several startups and research groups are building AI-native design tools:

- **Motivo:** AI for analog/RF chip design — automated circuit topology generation and sizing
- **Celera:** AI-accelerated computational fluid dynamics for engineering design
- **PhysicsX:** AI for physics simulation and engineering optimization (aerodynamics, structural)
- **Monolith AI:** ML for engineering test and simulation data — reduces physical testing needs

**Common pattern across all:** AI proposes designs, physics simulation validates, AI learns from validation results. None replace simulation — they accelerate the design→simulate→evaluate loop.

## Architecture Patterns from Research

### Pattern 1: Simulation-as-Oracle

```
AI Agent → Propose Design → Simulation Tool → Evaluate → Feedback → Improve
```

This is universal across DSO.ai, Cerebrus, ChemCrow, Coscientist, AlphaFold. The AI doesn't replace the simulation — it guides exploration of the design space.

### Pattern 2: Domain-Specific Tool Augmentation

```
LLM (orchestrator) + Domain Tools (executors) = Domain Expert Agent
```

ChemCrow's 17 chemistry tools are directly analogous to a set of MATLAB/Simulink/PLECS tools for power electronics.

### Pattern 3: Skill Library (Voyager-inspired)

```
Successful simulation workflows → Saved as skills → Retrieved for similar tasks → Improved over time
```

This is embodied in Hermes Agent's skills system and Claude Code's skills. For power electronics: "inverter_loss_analysis" skill encodes the workflow of running a simulation + extracting losses + plotting results.

### Pattern 4: Design Space Exploration via RL

```
RL Agent → Action: modify design parameter → Environment: run simulation → Reward: efficiency gain → Policy update → Loop
```

DSO.ai and Cerebrus use this for chip design. Directly applicable to inverter design where the design space (topology, switching frequency, component selection) is combinatorial.

## Key Finding

**No existing production system combines all three elements needed for autonomous traction inverter design:**
1. LLM-based reasoning and planning (ReAct agents)
2. Domain-specific simulation tools (MATLAB/Simulink)
3. Design space optimization (RL or evolutionary algorithms)

This gap is the opportunity: production AI-for-engineering tools (DSO.ai) exist but are domain-specific and proprietary. Research agents (ChemCrow, Coscientist) prove the LLM+tools pattern but are lab-scale. Building a combined system — LLM planning + MATLAB simulation + optimization loop — fills an unoccupied niche.


> **References:** [[citations]]


← [[ai-agents/harness/harness-index|Agent Harness Research]] | [[power-electronics/traction-inverter/traction-inverter-index|Traction Inverter Research]] → | [[README|SRTP Index]]
