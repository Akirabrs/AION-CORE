# AION-CORE: Physics-Anchored Anticipatory Control Kernel

<p align="center">
  <img src="https://img.shields.io/badge/Status-TRL%204%20(Sim%20Validated)-success?style=for-the-badge&logo=python" alt="Status">
  <img src="https://img.shields.io/badge/Architecture-COOK%20Framework-blueviolet?style=for-the-badge&logo=arduino" alt="Architecture">
  <img src="https://img.shields.io/badge/Platform-FPGA%20%2F%20Verilog%20HDL-red?style=for-the-badge&logo=xilinx" alt="Platform">
</p>

---

## 📊 LIVE TELEMETRY DASHBOARD
**Validation Shot:** NSTX-U High Performance | **Controller:** PI-POD v2.2

![Telemetry Dashboard](validation/media/telemetry_dashboard.png)

> **NOTA:** Se a imagem acima não carregar, verifique a pasta `validation/media/` no repositório.
>
> **SUCCESS:** The graph above shows the AION-CORE stabilizing a vertical displacement event (VDE) within 5ms.

---

## 🏗️ Módulos de Código (Agora Disponíveis)

Os códigos de "Propriedade Industrial" (AION-BURN) foram restaurados e estão seguros na pasta `src/`:

| Arquivo | Descrição | Linguagem |
| :--- | :--- | :--- |
| **`aion_burn_prototype_v2.py`** | Prova física do acoplamento térmico-mecânico | Python |
| **`aion_fpga_twin_bus.sv`** | Hardware Guardian que conecta as torres | SystemVerilog |
| **`aion_burn_types_v1.sv`** | Definição de tipos Q16.16 para FPGA | SystemVerilog |

---
*AION-CORE Project - MARK X*
