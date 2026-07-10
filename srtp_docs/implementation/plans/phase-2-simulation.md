# Phase 2 — Simulation Depth (Weeks 6-8)

> **Part of:** [[plan index|Plan Index]]
> **Goal:** MATLAB/Simulink backend, PySpice device-level co-simulation, ltspice-mcp integration.
> **Architecture:** Dual-engine: PySpice (device-level) + MATLAB (system-level) + ltspice-mcp (verification)

---

## Context

Phase 1 proved the multi-agent system works with PySpice. Phase 2 adds simulation depth:
1. **MATLAB/Simulink** for system-level motor drive simulation (if license available)
2. **ltspice-mcp** for device-level verification (gate drive, snubber, EMI filter)
3. **Co-simulation**: PySpice inverter + MATLAB motor model (or Python motor model if no MATLAB)

The goal is simulation fidelity comparable to what a human engineer would use for final verification.

---

## Week 6: MATLAB/Simulink Backend

### P2.1 — MATLAB Engine API Integration (Days 1-3)

**Only if MATLAB license is available.** If not, skip to P2.3 (PySpice motor model).

```python
# src/srtp_ai/backends/matlab_backend.py
import matlab.engine

class MatlabBackend:
    """
    MATLAB/Simulink simulation backend via Engine API for Python.
    
    Requirements:
    - MATLAB R2024a+ with Simscape Electrical
    - pip install matlabengine
    - MATLAB license
    """
    
    def __init__(self):
        self.eng = matlab.engine.start_matlab()
        self.eng.addpath(self.eng.genpath('models'))  # Simulink models path
    
    def load_model(self, model_name: str):
        """Load a Simulink model."""
        self.eng.load_system(model_name)
    
    def set_params(self, model: str, params: dict):
        """Set block parameters programmatically."""
        for block_path, param_dict in params.items():
            for param, value in param_dict.items():
                self.eng.set_param(f"{model}/{block_path}", param, value)
    
    def simulate(self, model: str, stop_time: float = 0.1) -> dict:
        """
        Run Simulink simulation and extract results.
        
        Key outputs:
        - efficiency: from power measurement blocks
        - thd: from THD measurement blocks
        - waveforms: Va, Vb, Vc, Ia, Ib, Ic (logged via To Workspace blocks)
        - losses: conduction + switching from device blocks
        - thermal: Tj from Simscape thermal network
        """
        result = self.eng.sim(model, 'StopTime', str(stop_time))
        
        return {
            "efficiency": float(self.eng.eval('efficiency(end)')),
            "thd": float(self.eng.eval('THD')),
            "waveforms": self._extract_waveforms(result),
            "losses": self._extract_losses(result),
            "thermal": self._extract_thermal(result),
        }
    
    def pause(self): self.eng.set_param(bdroot, 'SimulationCommand', 'pause')
    def continue_(self): self.eng.set_param(bdroot, 'SimulationCommand', 'continue')
    def stop(self): self.eng.set_param(bdroot, 'SimulationCommand', 'stop')
    def quit(self): self.eng.quit()

# Simulink model template (to be built once, parameterized programmatically)
# Models needed:
# 1. inverter_2l_b6.slx — 2-level VSI with Simscape MOSFET blocks
# 2. inverter_3l_npc.slx — 3-level NPC (stretch)
# 3. pmsm_drive.slx — PMSM + FOC control + inverter
# 4. thermal_network.slx — Foster/Cauer thermal model
```

**Deliverable:** MATLAB backend class + 2 Simulink model templates (2L-B6, PMSM drive).
**Verify:** Load model, set parameters, run simulation, extract efficiency → matches within 2% of published baseline.

### P2.2 — Simulink Model Parameterization (Days 2-4)

The agent must be able to programmatically modify Simulink models:

```python
# src/srtp_ai/backends/matlab_params.py
def configure_inverter_model(backend: MatlabBackend, components: dict, spec: dict):
    """Configure Simulink model from agent-selected components."""
    backend.set_params("inverter_2l_b6", {
        # MOSFET parameters
        "PowerStage/MOSFET_A_HS": {
            "Rds_on": str(components["switches"]["rds_on"]),
            "Vth": str(components["switches"]["vth"]),
            "Ciss": str(components["switches"]["ciss"]),
        },
        # DC-link
        "DC_Link/Capacitor": {
            "Capacitance": str(components["dc_link_cap"]["capacitance"]),
            "ESR": str(components["dc_link_cap"]["esr"]),
        },
        # PWM
        "Control/PWM_Generator": {
            "Frequency": str(components["fs"]),
            "DeadTime": str(components["dead_time"]),
        },
        # Motor load
        "Load/PMSM": {
            "Rs": str(components.get("motor_rs", 0.015)),
            "Ld": str(components.get("motor_ld", 0.0003)),
            "Lq": str(components.get("motor_lq", 0.0005)),
            "FluxPM": str(components.get("motor_flux", 0.1)),
            "PolePairs": str(components.get("motor_poles", 4)),
        },
    })
```

**Deliverable:** Parameter mapping from agent component dict → Simulink block parameters.
**Verify:** Configure model with 3 different component sets → each simulates correctly.

---

## Week 7: Device-Level Simulation + Co-Simulation

### P2.3 — PySpice Motor Model (Days 5-7)

**If MATLAB unavailable: build a behavioral PMSM model in Python + SPICE.**

```python
# src/srtp_ai/models/pmsm_behavioral.py
class PMSMBehavioralModel:
    """
    Behavioral PMSM model for co-simulation with PySpice inverter.
    
    Implements dq-frame motor equations:
    vd = Rs*id + Ld*did/dt - ωe*Lq*iq
    vq = Rs*iq + Lq*diq/dt + ωe*(Ld*id + λPM)
    Te = (3/2)*(P/2)*(λPM*iq + (Ld-Lq)*id*iq)
    
    Co-simulation pattern:
    1. SPICE inverter model generates Va, Vb, Vc at each timestep
    2. Clarke/Park transform → Vd, Vq
    3. Motor ODE solver → Id, Iq (Python, scipy.integrate)
    4. Inverse Park/Clarke → Ia, Ib, Ic → back to SPICE as current sources
    """
    
    def __init__(self, params: dict):
        self.Rs = params["Rs"]
        self.Ld = params["Ld"]
        self.Lq = params["Lq"]
        self.lambda_pm = params["flux_pm"]
        self.P = params["pole_pairs"]
        self.J = params.get("inertia", 0.1)
    
    def step(self, vd: float, vq: float, omega_e: float, dt: float) -> tuple:
        """One timestep of the motor model. Returns (id, iq, Te)."""
        # Euler integration of dq-frame electrical dynamics
        did_dt = (vd - self.Rs * self.id + omega_e * self.Lq * self.iq) / self.Ld
        diq_dt = (vq - self.Rs * self.iq - omega_e * (self.Ld * self.id + self.lambda_pm)) / self.Lq
        
        self.id += did_dt * dt
        self.iq += diq_dt * dt
        
        # Torque
        Te = (3/2) * (self.P/2) * (self.lambda_pm * self.iq + (self.Ld - self.Lq) * self.id * self.iq)
        
        return self.id, self.iq, Te
```

**Deliverable:** Python PMSM model that couples to PySpice inverter. Working co-simulation.
**Verify:** Run inverter + motor co-simulation at 400V, 10 kHz PWM. Motor spins. Currents are sinusoidal.

### P2.4 — ltspice-mcp Integration (Days 7-8)

The ltspice-mcp server provides 51 tools for device-level verification:

```python
# src/srtp_ai/backends/ltspice_mcp_client.py
class LtSpiceMCPClient:
    """
    Client for ltspice-mcp MCP server.
    Provides 51 SPICE simulation tools via MCP protocol.
    
    Key tools for SRTP:
    - transient_analysis: gate drive switching waveforms
    - operating_point: bias point with gm/gds/vth readback
    - ac_analysis: control loop stability (Bode, phase margin)
    - monte_carlo: component tolerance analysis
    - thd_analysis: harmonic distortion
    - parameter_sweep: sweep gate resistor, snubber values
    """
    
    TOOLS = [
        "transient_analysis", "operating_point", "ac_analysis",
        "monte_carlo", "thd_analysis", "parameter_sweep",
        "dc_operating_point", "noise_analysis", "pulse_response",
    ]
    
    def verify_gate_drive(self, gate_drive_params: dict) -> dict:
        """Verify gate drive switching: Vgs waveform, turn-on/off times, Miller plateau."""
        netlist = GATE_DRIVE_TEMPLATE.format(**gate_drive_params)
        result = self.run_tool("transient_analysis", netlist=netlist, stop_time="10u")
        return {
            "turn_on_time": result["rise_time"],
            "turn_off_time": result["fall_time"],
            "miller_plateau": result.get("plateau_voltage"),
            "ringing": result.get("ringing_frequency"),
        }
    
    def verify_snubber(self, snubber_params: dict) -> dict:
        """Verify snubber design: Vds overshoot, ringing damping."""
        ...
    
    def verify_emi_filter(self, filter_params: dict) -> dict:
        """Verify EMI filter: insertion loss vs frequency."""
        ...
```

**Deliverable:** `LtSpiceMCPClient` wrapping key ltspice-mcp tools for SRTP use cases.
**Verify:** Gate drive verification → reports turn-on/off times. Snubber verification → reports Vds overshoot.

### P2.5 — Dual-Engine Architecture (Days 8-10)

```python
# src/srtp_ai/simulation_engine.py
class SimulationEngine:
    """
    Routes simulation tasks to the appropriate backend:
    - System-level motor drive → MATLAB (if available) or PySpice+Python motor
    - Device-level switching → ltspice-mcp
    - Thermal network → MATLAB (if available) or PySpice Foster/Cauer
    """
    
    def __init__(self, matlab_available: bool = False):
        self.pypsice = PySpiceBackend()
        self.matlab = MatlabBackend() if matlab_available else None
        self.ltspice = LtSpiceMCPClient()
    
    def simulate_inverter_system(self, design: dict) -> SimulationResult:
        """System-level: inverter + motor + control."""
        if self.matlab:
            return self.matlab.simulate(design)
        else:
            return self.pypsice.simulate_with_motor_model(design)
    
    def verify_gate_drive(self, params: dict) -> dict:
        """Device-level: gate drive switching waveforms."""
        return self.ltspice.verify_gate_drive(params)
    
    def verify_thermal(self, losses: dict, thermal_params: dict) -> dict:
        """Thermal: Tj estimation from losses + Foster/Cauer network."""
        return ThermalModel(losses, thermal_params).estimate()
```

**Deliverable:** `SimulationEngine` unified interface for all 3 backends.
**Verify:** Same design simulated on PySpice and MATLAB (if available). Results within 5%.

---

## Week 8: Validation & Hardening

### P2.6 — Simulation Accuracy Validation (Days 10-12)

Validate simulation accuracy against known reference designs:

```python
# tests/test_simulation_accuracy.py
def test_tesla_model3_approximate():
    """Verify simulation matches approximate Tesla Model 3 rear drive unit specs."""
    spec = {"vdc": 400, "pout": 211, "topology": "2L-B6"}
    result = engine.simulate_inverter_system(spec)
    
    # Published: Tesla Model 3 rear inverter ~96-97% peak efficiency
    assert 0.94 <= result.efficiency <= 0.98, f"Efficiency {result.efficiency} outside expected range"
    # Published: 24 SiC MOSFETs in parallel, ~800A phase current capability
    assert result.phase_current < 900, "Phase current unrealistically high"
```

**Deliverable:** Validation test suite comparing against published specs.
**Verify:** All validation tests pass. Simulation results within published ranges.

### P2.7 — Co-Simulation Test (Day 12)

End-to-end test: inverter SPICE model + Python motor model + FOC control:

```python
async def test_cosimulation():
    """Test co-simulation: SPICE inverter + Python motor model."""
    spec = {"vdc": 400, "pout": 100, "topology": "2L-B6"}
    
    # Design
    state = await app.ainvoke({"spec": spec})
    
    # Verify co-simulation results
    assert state["simulation_results"]["converged"]
    assert state["simulation_results"]["motor_speed"] > 0  # Motor actually spins!
    assert state["simulation_results"]["efficiency"] > 0.90
```

**Deliverable:** Co-simulation integration test passing.
**Verify:** SPICE inverter switches → motor model produces torque → speed builds up → steady-state reached.

---

## Phase 2 Checklist

- [ ] P2.1: MATLAB backend operational (or: confirmed unavailable, P2.3 covers it)
- [ ] P2.2: Simulink model parameterization working (or: PySpice equivalent)
- [ ] P2.3: PySpice + Python motor model co-simulation working
- [ ] P2.4: ltspice-mcp device-level verification: gate drive, snubber, EMI filter
- [ ] P2.5: Unified SimulationEngine routing to correct backend
- [ ] P2.6: Simulation accuracy validation against published specs
- [ ] P2.7: Full co-simulation integration test: inverter + motor + control

## Phase 2 Acceptance

1. System-level simulation (inverter + motor) converges and produces physically plausible results
2. Device-level verification (gate drive, snubber) via ltspice-mcp
3. Simulation results within 5% of published reference designs
4. Dual-engine architecture transparent to agents (same interface regardless of backend)

---

← [[implementation/plans/phase-1-multi-agent]] | [[implementation/plans/phase-3-knowledge]] →
