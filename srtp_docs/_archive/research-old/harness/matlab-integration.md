# MATLAB Integration Strategy

> **Part of:** [[harness index|Agent Harness Research]]  
> **Goal:** Define how to integrate MATLAB/Simulink as a first-class tool in the agent harness  
> **Last Updated:** 2026-07-06

## Overview

MATLAB and Simulink are the industry-standard tools for power electronics simulation. The research agent must be able to:

1. **Invoke MATLAB** — run `.m` scripts, call functions, execute Simulink models
2. **Pass parameters** — send topology parameters, component values, control settings
3. **Retrieve results** — collect waveforms, efficiency data, loss breakdowns
4. **Iterate** — run parameter sweeps, optimization loops, sensitivity analysis

## Integration Approaches

### Approach 1: MATLAB Engine API for Python

```
Agent (Python) → MATLAB Engine API → MATLAB Runtime → Simulink
```

**How it works:**
```python
import matlab.engine

eng = matlab.engine.start_matlab()
result = eng.simulate_inverter(topology='ANPC', voltage=800, frequency=10000)
eng.quit()
```

**Pros:**
- First-class Python integration — natural for Hermes (Python-based)
- Pass complex data structures (dicts, arrays, structs) bidirectionally
- Access to MATLAB workspace variables
- Can call Simulink via `sim()` command

**Cons:**
- Requires MATLAB installation with Engine API
- MATLAB process is heavyweight (startup time ~5-10s)
- License cost for MATLAB

### Approach 2: MATLAB CLI (`matlab -batch`)

```
Agent → Shell → matlab -batch "script.m" → Parse stdout/files
```

**How it works:**
```bash
matlab -batch "run('simulate_inverter.m'); exit"
```

**Pros:**
- No Python dependency for MATLAB calls
- Works with any MATLAB installation
- Can use `-nosplash -nodesktop` for headless

**Cons:**
- Data exchange via files or stdout parsing (fragile)
- MATLAB process startup overhead per call
- No real-time interaction with running simulation

### Approach 3: MATLAB MCP Server (Claude Code Pattern)

```
Agent ←→ MCP Protocol ←→ MATLAB MCP Server ←→ MATLAB Engine API
```

**How it works:**
- Standalone Python process that wraps MATLAB Engine API
- Exposes tools via MCP (Model Context Protocol)
- Agent calls `simulate_inverter` tool → MCP server → MATLAB → results returned

**Pros:**
- Clean separation of concerns
- Language-agnostic (any MCP client can talk to MATLAB)
- Can keep MATLAB process alive between calls (no startup overhead)
- Follows Claude Code's proven MCP integration pattern

**Cons:**
- Additional infrastructure (MCP server process)
- Slightly more complex than direct Engine API

### Approach 4: MATLAB Production Server / Web API

```
Agent → REST API → MATLAB Production Server → Compiled MATLAB
```

**Pros:** Scalable, production-grade, no MATLAB license per call
**Cons:** Requires MATLAB Production Server license (expensive), deployment complexity

## Architecture Analysis: Direct Engine vs. MCP Server

### Direct Engine API
Use Approach 1 for initial development — simplest path to working integration.

```python
# Hermes custom tool: tools/matlab_tool.py
import matlab.engine
from tools.registry import registry

_eng = None

def get_engine():
    global _eng
    if _eng is None:
        _eng = matlab.engine.start_matlab()
    return _eng

def matlab_simulate(topology: str, params: dict, task_id: str = None) -> str:
    """Run a MATLAB/Simulink simulation and return results."""
    eng = get_engine()
    result = eng.simulate_inverter(topology, params)
    return json.dumps({
        "efficiency": result["efficiency"],
        "losses": result["losses"],
        "waveforms": result["waveform_path"]
    })

registry.register(
    name="matlab_simulate",
    toolset="matlab",
    schema={...},
    handler=matlab_simulate,
    check_fn=lambda: check_matlab_available(),
)
```

### MCP Server
Migrate to Approach 3 for robustness — persistent MATLAB process, clean protocol.

```
~/.hermes/mcp-servers/matlab-mcp/
├── server.py          # MCP server wrapping MATLAB Engine
├── requirements.txt   # matlab-engine, mcp
└── tools.yaml         # Tool definitions
```

## Simulink Integration

Simulink models can be driven programmatically:

```matlab
% Load model
load_system('inverter_model');

% Set parameters
set_param('inverter_model/DC_Link', 'Value', '800');
set_param('inverter_model/SwitchingFreq', 'Value', '20000');

% Run simulation
simOut = sim('inverter_model', 'StopTime', '0.1');

% Extract results
Vout = simOut.logsout.getElement('Vout').Values.Data;
Iout = simOut.logsout.getElement('Iout').Values.Data;
efficiency = simOut.logsout.getElement('efficiency').Values.Data(end);
```

For a research agent, Simulink integration requirements include:
1. Update Simulink block parameters
2. Run the model
3. Collect logged signals
4. Compare against baseline models

## Tool API Design

### Core MATLAB Tools

```yaml
tools:
  - name: matlab_simulate
    description: "Run a power electronics simulation in MATLAB/Simulink"
    parameters:
      topology: string        # e.g., "2-level-VSI", "3-level-NPC", "ANPC"
      dc_voltage: number      # DC link voltage
      switching_freq: number  # Switching frequency (Hz)
      output_power: number    # Target output power (W)
      modulation: string      # e.g., "SPWM", "SVPWM", "DPWM"
      device_type: string     # e.g., "IGBT", "SiC_MOSFET", "GaN_HEMT"
      device_model: string    # Specific part number or datasheet params
      
  - name: matlab_sweep
    description: "Run parameter sweep across multiple simulation scenarios"
    parameters:
      base_params: object
      sweep_params: object    # {param_name: [values]}
      
  - name: matlab_analyze
    description: "Analyze existing simulation results"
    parameters:
      results_file: string    # Path to .mat or .csv
      metrics: string[]       # e.g., ["efficiency", "THD", "losses"]
      
  - name: matlab_compare
    description: "Compare two simulation results"
    parameters:
      result_a: string        # Path or reference to baseline
      result_b: string        # Path or reference to new simulation
```

## Performance Considerations

- **MATLAB startup:** 5-10 seconds. Keep engine alive between calls.
- **Simulink compilation:** First run compiles model (~5-30s). Subsequent runs are faster.
- **Parameter sweeps:** Batch parameters into single MATLAB session to avoid recompilation.
- **Parallel simulations:** Multiple MATLAB workers via Parallel Computing Toolbox.


> **References:** [[citations]]


← [[comparative-analysis|Prev: Comparative Analysis]] | [[architecture-patterns|Next: Architecture Patterns]] → | [[README]]
