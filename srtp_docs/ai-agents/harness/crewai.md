---
title: CrewAI — Architecture Deep Dive
type: topic
field: ai-agents
created: 2026-07-08
updated: 2026-07-08
status: unverified
evidence: single-study
tags: [ai-agents, crewai, architecture]
---

## Overview

CrewAI is a **role-based multi-agent orchestration framework** inspired by the "crew" metaphor. Agents are defined with roles, goals, and backstories — then assigned tasks and tools. The framework coordinates their collaboration through hierarchical or sequential execution.

For power electronics research, CrewAI's strength is the **natural mapping to research team structure**: define a "Power Electronics Researcher", a "MATLAB Simulation Engineer", a "Data Analyst", and a "Report Writer" as distinct agents with specialized tools and domain knowledge.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       CREWAI                             │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                    CREW (Team)                      │ │
│  │                                                     │ │
│  │  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │  Researcher  │  │  Sim Engineer│                │ │
│  │  │  Agent       │  │  Agent       │                │ │
│  │  │              │  │              │                │ │
│  │  │ Role: Power  │  │ Role: MATLAB │                │ │
│  │  │ Electronics  │  │ Simulation   │                │ │
│  │  │ Expert       │  │ Engineer     │                │ │
│  │  │              │  │              │                │ │
│  │  │ Tools:       │  │ Tools:       │                │ │
│  │  │ • arXiv API  │  │ • MATLAB Eng │                │ │
│  │  │ • PaperQA2   │  │ • Simulink   │                │ │
│  │  │ • Web Search │  │ • PLECS API  │                │ │
│  │  │ • PDF Reader │  │ • Python     │                │ │
│  │  └──────┬───────┘  └──────┬───────┘                │ │
│  │         │                 │                         │ │
│  │  ┌──────▼───────┐  ┌──────▼───────┐                │ │
│  │  │ Data Analyst │  │ Report Writer│                │ │
│  │  │ Agent        │  │ Agent        │                │ │
│  │  │              │  │              │                │ │
│  │  │ Role: Power  │  │ Role: IEEE   │                │ │
│  │  │ Electronics  │  │ Report       │                │ │
│  │  │ Data Analyst │  │ Author       │                │ │
│  │  │              │  │              │                │ │
│  │  │ Tools:       │  │ Tools:       │                │ │
│  │  │ • Pandas     │  │ • LaTeX      │                │ │
│  │  │ • NumPy/SciPy│  │ • Matplotlib │                │ │
│  │  │ • Plotting   │  │ • Templates  │                │ │
│  │  └──────────────┘  └──────────────┘                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              PROCESS MODES                          │ │
│  │  • Sequential: Task A → Task B → Task C            │ │
│  │  • Hierarchical: Manager agent delegates tasks     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │              MEMORY SYSTEM                          │ │
│  │  • Short-term: Current conversation context        │ │
│  │  • Long-term: Persistent across sessions           │ │
│  │  • Entity: Facts about components, topologies      │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Core Abstractions

| Abstraction | Description | Research Example |
|-------------|-------------|-----------------|
| **Agent** | Role + goal + backstory + tools + LLM + memory | "Power Electronics Researcher" with arXiv, PaperQA2 tools |
| **Task** | Description + expected output + agent assignment + dependencies | "Find optimal inverter topology for 800V EV traction" |
| **Crew** | Orchestrator managing agents and task execution | Research team with sequential simulation-analysis pipeline |
| **Flow** | Event-driven state machine (v0.80+) | Complex experiment design with parameter sweeps |
| **Tool** | Python function decorated as callable tool | `@tool` wrapper around MATLAB Engine API |
| **Memory** | Unified LLM-analyzed memory (v0.80+): scoped hierarchy, composite scoring, adaptive recall | Remember component specs, baselines, design decisions across research sessions |
| **Memory (legacy)** | ⚠️ Pre-v0.80: short-term, long-term, entity memory — removed in current version |

### Example: Power Electronics Research Crew

```python
from crewai import Agent, Task, Crew, Process

# Define specialist agents
researcher = Agent(
    role="Power Electronics Researcher",
    goal="Find optimal inverter topology and component selection for given specs",
    backstory="Senior power electronics researcher with 20 years experience...",
    tools=[arxiv_search, paperqa_query, web_search, datasheet_parser],
    llm="deepseek-chat",
    memory=True  # Remembers findings across sessions
)

sim_engineer = Agent(
    role="MATLAB Simulation Engineer",
    goal="Run accurate MATLAB/Simulink simulations of power electronic circuits",
    backstory="Expert in MATLAB/Simulink for power electronics...",
    tools=[matlab_simulate, simulink_compile, plecs_thermal],
    llm="claude-sonnet-4",
    memory=True
)

analyst = Agent(
    role="Power Electronics Data Analyst",
    goal="Analyze simulation results: efficiency, losses, THD, thermal performance",
    backstory="Specialist in power electronics data analysis...",
    tools=[python_analysis, plot_efficiency, compare_baselines],
    llm="claude-sonnet-4"
)

writer = Agent(
    role="IEEE Report Author",
    goal="Compile research findings into IEEE-formatted technical reports",
    backstory="Published author of 50+ IEEE papers...",
    tools=[latex_compiler, figure_generator, reference_manager],
    llm="gpt-4"
)

# Define tasks with dependencies
research_task = Task(
    description="Research SiC vs IGBT for 800V traction inverter",
    expected_output="Topology recommendation with component selection rationale",
    agent=researcher
)

sim_task = Task(
    description="Simulate the recommended topology with MATLAB/Simulink",
    expected_output="Simulation results: efficiency map, loss breakdown, thermal data",
    agent=sim_engineer,
    context=[research_task]  # Receives output from research task
)

analysis_task = Task(
    description="Analyze simulation results and compare against baselines",
    expected_output="Analysis: efficiency comparison, THD, losses, cost analysis",
    agent=analyst,
    context=[sim_task]
)

report_task = Task(
    description="Write IEEE-formatted research report with findings",
    expected_output="Complete report with abstract, methodology, results, conclusions",
    agent=writer,
    context=[research_task, analysis_task]
)

# Assemble crew
research_crew = Crew(
    agents=[researcher, sim_engineer, analyst, writer],
    tasks=[research_task, sim_task, analysis_task, report_task],
    process=Process.sequential,  # Or Process.hierarchical for manager-coordinated
    memory=True  # Persistent across crew runs
)

# Execute
result = research_crew.kickoff()
```

## Key Features for Research Agent

| Feature | Research Benefit |
|---------|-----------------|
| **Role-based agents** | Natural mapping to research team structure |
| **Task dependencies** | `context=[prev_task]` chains simulation→analysis→report |
| **Built-in memory** | Unified LLM-analyzed with scoped hierarchy, composite scoring, adaptive-depth recall |
| **Tool decorators** | `@tool` wraps MATLAB Engine API in one line |
| **Hierarchical process** | Manager agent coordinates specialists autonomously |
| **Flows (v0.80+)** | Event-driven state machines for complex experiment designs |
| **Human-in-the-loop** | Review simulation parameters before execution |
| **Structured output** | Pydantic models enforce valid simulation result schemas |

## Strengths

1. **Intuitive role-based model** — agents match how humans think about research teams
2. **Built-in memory** — persistent across sessions (unlike all coding agents)
3. **Simple API** — 5-line agent definitions, clean task dependencies
4. **MIT licensed** — no restrictions
5. **Strong community** — 55k stars, active development
6. **Python-native** — direct MATLAB Engine API integration
7. **Hierarchical process** — manager agent can autonomously replan if simulation fails

## Weaknesses

1. **Library, not platform** — no CLI, no cron, no multi-platform gateway
2. **Young Flow system** — state machine support (v0.80+) is newer than LangGraph's
3. **Opinionated** — role metaphor can feel restrictive for non-team-shaped problems
4. **Commercial platform** — CrewAI AMP is proprietary; open-source core is MIT
5. **Less fault-tolerant** — no native checkpointing like LangGraph for long simulations

## MATLAB Integration Potential: 🟢 High

CrewAI's agent + tool model maps cleanly to MATLAB workflows:

- **Simulation Engineer agent** — equipped with `matlab_simulate`, `simulink_compile`, `plecs_thermal` tools
- **Data Analyst agent** — equipped with `python_analysis`, `plot_efficiency` tools that process MATLAB output
- **Task dependencies** — simulation must complete before analysis can start
- **Memory** — remembers component libraries, baseline results across sessions

## Suitability: 🟢 Excellent (for role-based teams)

**Role:** The "research lab" — defines who does what in the research process.  
**Best when:** You think of research as a team of specialists collaborating.  
**Pair with:** LangGraph for the workflow engine, Hermes Agent for infrastructure.


> **References:** [[citations]]


← [[ai-agents/harness/langgraph|Prev: LangGraph]] | [[ai-agents/harness/autogen|Next: AutoGen]] → | [[README]]
