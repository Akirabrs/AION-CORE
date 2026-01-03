# AION-CORE: Physics-Aware Adaptive Control Kernel

<p align="center">
  <img src="https://img.shields.io/badge/Status-TRL%204%20(Lab%20Validated)-success?style=for-the-badge&logo=github" alt="Status">
  <img src="https://img.shields.io/badge/Platform-FPGA%20%2F%20Real--Time-red?style=for-the-badge&logo=xilinx" alt="Platform">
  <img src="https://img.shields.io/badge/Latency-%3C%201%C2%B5s%20(Target)-blue?style=for-the-badge&logo=speedtest" alt="Latency">
  <img src="https://img.shields.io/badge/License-Apache%202.0-lightgrey?style=for-the-badge" alt="License">
</p>

---

## ⚛️ The Paradigm Shift in Fast Control

**AION-CORE** is a **Control Kernel** designed for extreme physical systems where traditional PID fails due to latency, and standard MPC fails due to computational load. It unifies the **AEGIS** safety protocols and **NPE-PSQ** metrics into a single architecture.

It introduces the **PACC (Physics-Aware Adaptive Control Core)** paradigm: orchestrating control decisions based on immediate physical precursors rather than delayed error integration.

> **Core Mission:** To provide a deterministic, sub-microsecond "Guardian Layer" for systems operating on the brink of instability, such as Tokamak plasmas and pulsed propulsion drives.

---

## 🏗️ Architecture: The COOK Framework

AION-CORE executes within the **Control-Oriented Operating Kernel (COOK)**, a dual-loop architecture optimized for determinism.

```mermaid
graph TD
    subgraph Plant ["Physical Plant (Tokamak/PEC)"]
        S["⚡ Fast Sensors (dB/dt, Ip)"]
        A["🔌 Actuators (Coils/Pulses)"]
    end

    subgraph Kernel ["COOK Kernel (FPGA Fabric)"]
        direction TB
        
        subgraph L1 ["Layer 1: Reflex Loop (<1µs)"]
            PM["🔍 Precursor Monitor"]
            TM["🧠 Threat Memory (BRAM)"]
            GL["🛡️ Guardian Logic (AEGIS Layer)"]
        end

        subgraph L2 ["Layer 2: Cognitive Loop (~1ms)"]
            ADAPT["🔄 RLS Model Adaptation"]
        end

        S ===>|Raw Data| PM
        PM ===>|Signature Match| TM
        TM ===>|Candidate Action| GL
        GL ===>|Verified Pulse| A
        
        S -.->|Slow Data| ADAPT
        ADAPT -.->|Update Parameters| TM
    end

    style GL fill:#f96,stroke:#333,stroke-width:2px,color:black
    style PM fill:#add8e6,stroke:#333,color:black
