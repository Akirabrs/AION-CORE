# Arquitetura do Sistema AION-CORE
> **Paradigma:** Dual-Loop Control com Desacoplamento Temporal

Este documento detalha a engenharia de sistemas do AION-CORE, focando na integração segura entre Deep Learning (Python) e Controle em Tempo Real (FPGA).

---

## 1. O Desafio da Latência Física
Em reactores tokamak de alto beta, os Eventos de Deslocamento Vertical (VDEs) crescem exponencialmente com taxas de crescimento $\gamma \approx 2800$ rad/s.
* **Tempo de colisão:** $< 500 \mu s$.
* **Latência de inferência (IA):** $\approx 1 \dots 5$ ms.

**Problema:** Um loop de controle acoplado tradicional (Sensor -> IA -> Atuador) introduziria um atraso fatal, levando à perda do plasma.

---

## 2. A Solução: Arquitetura Dual-Loop
O AION-CORE resolve este problema através do **Desacoplamento Temporal Estrito**. O sistema é dividido em duas camadas assíncronas:

### Diagrama de Fluxo de Dados
```mermaid
graph TD
    subgraph "Layer 2: Cognitivo (Professor)"
        NPE[NPE Brain<br/>PyTorch/CNN]
        State[Análise de Estado]
        Planner[Planeador de Ganhos]
    end

    subgraph "Layer 1: Reflexo (Aluno)"
        FPGA[Reflex Core<br/>Verilog HDL]
        Cache[Registos de Ganhos]
        Law[Lei de Controle PD]
    end

    subgraph "Layer 0: Planta Física"
        Plasma((Tokamak Plasma))
        Sensors[Sensores Magnéticos]
        Coils[Bobinas Atuadoras]
    end

    %% Fluxo Rápido
    Plasma -->|1us| Sensors
    Sensors -->|Latência Zero| FPGA
    FPGA -->|PWM Action| Coils
    Coils --> Plasma

    %% Fluxo Lento
    Sensors -.->|Buffer 1ms| NPE
    NPE -.->|Sugestão Kp, Kd| Cache
