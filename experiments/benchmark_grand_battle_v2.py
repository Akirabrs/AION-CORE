import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Tuple, List, Dict, Callable
import os

# ============================================================================
# CONFIGURAÇÃO DA FÍSICA DO TOKAMAK
# ============================================================================
class TokamakPhysics:
    def __init__(self, gamma: float = 2800.0, dt: float = 1e-6):
        self.gamma = gamma  # Frequência característica do plasma (rad/s)
        self.dt = dt        # Passo de tempo (s)
        
    def step(self, z: float, vz: float, u: float, noise: float = 0.0) -> Tuple[float, float]:
        # Equação do movimento: d²z/dt² = γ²z + u + ruído
        acceleration = (self.gamma**2 * z) + u + noise
        vz_new = vz + acceleration * self.dt
        z_new = z + vz_new * self.dt
        return z_new, vz_new

# ============================================================================
# CONTROLADORES
# ============================================================================
class PIDController:
    def __init__(self, kp: float = 7e6, kd: float = 5e4):
        self.kp = kp
        self.kd = kd
        
    def __call__(self, z: float, vz: float) -> float:
        return -self.kp * z - self.kd * vz

class AIONController:
    def __init__(self):
        self.normal_kp = 7e6
        self.normal_kd = 5e4
        self.turbo_kp = 1.5e7
        self.turbo_kd = 2e5
        self.turbo_threshold = 0.5 
        
    def __call__(self, z: float, vz: float) -> float:
        # Lógica Adaptativa (Professor Distillation)
        if abs(vz) > self.turbo_threshold:
            kp, kd = self.turbo_kp, self.turbo_kd
        else:
            kp, kd = self.normal_kp, self.normal_kd
        return -kp * z - kd * vz

class MPCController:
    def __init__(self, horizon: int = 10, n_candidates: int = 15):
        self.horizon = horizon
        self.n_candidates = n_candidates
        self.physics = TokamakPhysics()
        
    def __call__(self, z: float, vz: float) -> float:
        candidates = np.linspace(-50000, 50000, self.n_candidates)
        best_u = 0.0
        min_cost = float('inf')
        
        for u in candidates:
            z_sim, vz_sim = z, vz
            cost = 0.0
            for _ in range(self.horizon):
                z_sim, vz_sim = self.physics.step(z_sim, vz_sim, u)
                cost += z_sim**2 
            if cost < min_cost:
                min_cost = cost
                best_u = u
        return best_u

# ============================================================================
# MOTOR DE SIMULAÇÃO
# ============================================================================
def simulate_controller(controller: Callable, controller_name: str, z0: float, vz0: float, steps: int):
    physics = TokamakPhysics()
    z, vz = z0, vz0
    trajectory = []
    
    start_time = time.perf_counter()
    
    for i in range(steps):
        noise = np.random.normal(0, 10000)
        u = controller(z, vz)
        u = np.clip(u, -50000, 50000)
        z, vz = physics.step(z, vz, u, noise)
        trajectory.append(z * 1000) # mm
        
        if abs(z) > 0.1: # Falha (10cm)
            trajectory.extend([100.0] * (steps - i - 1))
            break
            
    return trajectory, time.perf_counter() - start_time

# ============================================================================
# EXECUÇÃO E VISUALIZAÇÃO
# ============================================================================
def main():
    print("⚔️  AION-CORE: GRAND BATTLE BENCHMARK")
    
    STEPS = 1500 # 1.5ms
    DT = 1e-6
    controllers = {
        'PID (Classic)': PIDController(),
        'MPC (Ideal)': MPCController(),
        'AION (Ours)': AIONController()
    }
    
    results = {}
    times = {}
    
    for name, ctrl in controllers.items():
        print(f"▶️  Rodando {name}...")
        traj, t = simulate_controller(ctrl, name, 0.003, 0.5, STEPS)
        results[name] = traj
        times[name] = t
        
    # Plotagem
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Cores
    colors = {'PID (Classic)': '#E74C3C', 'MPC (Ideal)': '#2ECC71', 'AION (Ours)': '#3498DB'}
    
    # 1. Trajetórias
    for name, traj in results.items():
        ax1.plot(traj, color=colors[name], label=name, alpha=0.8, linewidth=2)
    ax1.set_title("Estabilidade (VDE Recovery)")
    ax1.set_ylabel("Z (mm)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Custo Computacional
    ax2.bar(times.keys(), times.values(), color=[colors[c] for c in times])
    ax2.set_title("Latência (Log Scale)")
    ax2.set_ylabel("Segundos")
    ax2.set_yscale('log')
    for i, v in enumerate(times.values()):
        ax2.text(i, v, f"{v:.4f}s", ha='center', va='bottom')
        
    # 3. Zoom Inicial
    for name, traj in results.items():
        ax3.plot(traj[:200], color=colors[name], linewidth=2)
    ax3.set_title("Resposta Transiente (Zoom 200us)")
    ax3.grid(True, alpha=0.3)
    
    # 4. Métricas Finais
    metrics = ['Overshoot', 'Steady Error']
    x = np.arange(len(metrics))
    width = 0.25
    for i, (name, traj) in enumerate(results.items()):
        val = [np.max(np.abs(traj)), np.mean(np.abs(traj[-100:]))]
        ax4.bar(x + i*width, val, width, label=name, color=colors[name])
    ax4.set_xticks(x + width)
    ax4.set_xticklabels(metrics)
    ax4.set_title("Métricas de Erro (mm)")
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('grand_battle_results_v2.png')
    print("✅ Benchmark concluído. Imagem salva: grand_battle_results_v2.png")

if __name__ == "__main__":
    main()
