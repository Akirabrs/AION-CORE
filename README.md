# AION-CORE: Physics-Anchored Anticipatory Control Kernel

<p align="center">
  <img src="https://img.shields.io/badge/Status-TRL%204%20(Sim%20Validated)-success?style=for-the-badge&logo=python" alt="Status">
  <img src="https://img.shields.io/badge/Architecture-COOK%20Framework-blueviolet?style=for-the-badge&logo=arduino" alt="Architecture">
  <img src="https://img.shields.io/badge/Latency-%3C%201%C2%B5s%20(Determininstic)-blue?style=for-the-badge&logo=speedtest" alt="Latency">
  <img src="https://img.shields.io/badge/Platform-FPGA%20%2F%20Verilog%20HDL-red?style=for-the-badge&logo=xilinx" alt="Platform">
  <a href="https://doi.org/10.5281/zenodo.18136444"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.18136444.svg" alt="DOI"></a>
</p>

---

## 📑 Executive Abstract

**AION-CORE** is a deterministic control kernel designed for the stabilization of high-$\beta$ tokamak plasmas, specifically targeting **Vertical Displacement Events (VDEs)**. Unlike traditional PID controllers that react to error integration ($\int e(t)dt$), AION utilizes the **PACC (Physics-Aware Adaptive Control)** paradigm to preemptively act upon physical precursors ($\frac{dI_p}{dt}, \frac{dB}{dt}$) within the microsecond regime.

The system is implemented on bare-metal FPGA fabric (Verilog HDL), unifying the **AEGIS** safety protocols and **NPE-PSQ** synchronization metrics into a monolithic **Control-Oriented Operating Kernel (COOK)**.

> **Key Performance Indicator:** Stabilizes VDEs with growth rates $\gamma \approx 2800$ rad/s with a reflex latency of $\tau < 1 \mu s$.

---

## ⚠️ Ethical Disclosure & Project Status

**1. AI-Assisted Development:**
This project utilizes Large Language Models (LLMs) as a technical co-pilot for code generation, LaTeX formatting, and architectural structuring. While the core concepts (PACC/COOK/AEGIS) and system architecture were conceived by the human author, implementation details rely heavily on AI synthesis and rapid prototyping.

**2. Validation Limitations (TRL 4):**
* ✅ **Validated:** Mathematical logic and control loops via Python stochastic simulation (Industrial Noise Model).
* ❌ **Not Validated:** Physical FPGA hardware implementation (HIL), real plasma coupling, or industrial safety certification.
* **Warning:** This is an academic proof-of-concept. **Do not deploy** on active magnetic confinement devices without rigorous independent review.

---

## 📐 The PACC Mathematical Model

The core control law deviates from standard MPC. It minimizes a physics-anchored cost function $J$ based on the Hamiltonian energy of the plasma column:

$$
u(t) = - K_p(t) \cdot Z(t) - K_d(t) \cdot \Gamma_{boost}(\dot{Z}) \cdot \dot{Z}(t)
$$

Where $\Gamma_{boost}$ is the nonlinear **Guardian Gain** derived from the AEGIS layer:

$$
\Gamma_{boost}(\dot{Z}) = 
\begin{cases} 
1 & \text{if } |\dot{Z}| < V_{thresh} \text{ (Linear Regime)} \\
\alpha \cdot e^{\beta (|\dot{Z}| - V_{thresh})} & \text{if } |\dot{Z}| \geq V_{thresh} \text{ (Guardian Regime)}
\end{cases}
$$

This ensures linear compliance during quiescence and exponential stiffness during instability onset.

---

## 🏗️ System Architecture: The COOK Framework

The **Control-Oriented Operating Kernel (COOK)** operates on a dual-loop frequency domain, separating reflex safety actions from cognitive adaptations.

```mermaid
graph TD
    subgraph Plant ["⚛️ TOKAMAK PHYSICAL PLANT"]
        S_FAST["⚡ Magnetic Probes (Mirnov Coils)"]
        S_SLOW["🌡️ Thomson Scattering / CXRS"]
        ACT["🔌 Poloidal Field Coils (PF)"]
    end

    subgraph FPGA ["💻 COOK KERNEL (FPGA FABRIC)"]
        direction TB
        
        subgraph LAYER_1 ["🔴 LAYER 1: REFLEX CORE (100 MHz)"]
            ADC["ADC Interface"]
            PRE["🔍 Precursor Monitor (dB/dt)"]
            TM["🧠 Threat Memory (BRAM)"]
            AEGIS["🛡️ AEGIS Guardian Logic"]
            PWM["PWM Generator"]
            
            ADC ==> PRE
            PRE ==>|Event Trigger| TM
            TM ==>|Zero-Copy Access| AEGIS
            AEGIS ==>|Hard Real-Time Pulse| PWM
        end

        subgraph LAYER_2 ["🔵 LAYER 2: COGNITIVE LOOP (1 kHz)"]
            RLS["🔄 RLS Parameter Estimator"]
            MODEL["📈 Digital Twin Model"]
            
            RLS -.->|Update Gains Kp, Kd| AEGIS
            MODEL -.->|Verify Safety Margins| TM
        end
    end

    S_FAST ==>|LVDS Link| ADC
    S_SLOW -.->|Ethernet| RLS
    PWM ==>|IGBT Gate Drive| ACT
    
    style AEGIS fill:#ff4d4d,stroke:#333,stroke-width:3px,color:white
    style RLS fill:#4d79ff,stroke:#333,stroke-width:2px,color:white

---

## 📊 Scientific Validation (Monte Carlo Analysis)

To validate the robustness of the Dual-Loop architecture, we performed a Monte Carlo simulation (N=1000 runs) comparing AION-CORE against a tuned industrial PID controller under high-voltage noise conditions (0-50kV disturbance).

### The "Storm Test" Results
As process noise increases, the static PID fails to compensate for the exponential growth of the VDE instability. The AION-CORE (Blue), leveraging its **Adaptive Neural Scheduler**, detects the high-velocity transient and dynamically boosts the gain ($K_p 	o 15M$), maintaining the plasma within the safety envelope.

| Metric | Classic PID | AION-CORE | Improvement |
|:---|:---:|:---:|:---:|
| **Mean Error (Low Noise)** | 0.0021 m | 0.0020 m | ~0% (Parity) |
| **Mean Error (High Noise)**| 0.0450 m | 0.0120 m | **3.7x Better** |
| **Survival Rate** | 62% | 99% | **+37%** |

> *Data generated via `experiments/monte_carlo_validation.py` simulation engine.*
