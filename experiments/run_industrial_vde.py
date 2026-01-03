import numpy as np
import matplotlib.pyplot as plt

class TokamakPlant:
    def __init__(self):
        self.gamma = 2800.0 
        self.dt = 1e-6
        self.z = 0.001
        self.vz = 0.0

    def step(self, u_control):
        noise = np.random.normal(0, 0.002)
        accel = (self.gamma**2 * self.z) + u_control + noise
        self.vz += accel * self.dt
        self.z += self.vz * self.dt
        return self.z, self.vz

class AION_Controller:
    def __init__(self):
        self.kp = 20.0
        self.kd = 5.0

    def compute_action(self, z, vz):
        guardian_gain = 1.0
        if abs(vz) > 10.0: guardian_gain = np.exp(0.1 * abs(vz))
        u = - (self.kp * z) - (self.kd * guardian_gain * vz)
        return np.clip(u, -50000, 50000)

if __name__ == "__main__":
    print("⚡ SIMULAÇÃO AION-CORE INICIADA...")
    plant = TokamakPlant()
    ctrl = AION_Controller()
    for _ in range(5000):
        plant.step(ctrl.compute_action(plant.z, plant.vz))
    print("✅ Simulação concluída com sucesso.")
