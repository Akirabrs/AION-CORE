
import numpy as np
import matplotlib.pyplot as plt

def run_demo():
    print("🚀 Running AION Stabilization Demo...")
    
    # 1. Setup Simulation Params
    T_steps = 100
    dt = 0.001
    
    # 2. Simulate System Response (Mock Data)
    time = np.linspace(0, T_steps*dt, T_steps)
    z_pos = 0.05 * np.exp(-50 * time) * np.cos(200 * time) # Amortecido
    
    print(f"✅ Simulation complete. Final Error: {z_pos[-1]:.6f}")

if __name__ == "__main__":
    run_demo()
