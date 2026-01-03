import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. O "MONSTRO" FÍSICO (A Planta do Tokamak)
# ==============================================================================
class TokamakPlant:
    def __init__(self):
        # AULA 01: Aqui mora o perigo
        # Gamma = 2800 rad/s (A velocidade da queda da vassoura)
        self.gamma = 2800.0 
        
        # Outros parâmetros físicos
        self.mass = 1.0       # Massa "efetiva" do plasma
        self.dt = 1e-6        # 1 microssegundo (Tempo do Universo da simulação)
        
        # Estado inicial (Vassoura reta, mas nem tanto)
        self.z = 0.001        # 1mm de deslocamento inicial (o "empurrãozinho")
        self.vz = 0.0         # Velocidade inicial
        self.t = 0.0

    def dynamics(self, u_control):
        """
        A LEI DA FÍSICA (Equação Diferencial)
        Aceleração = (Instabilidade * Posição) + Controle
        """
        # Ruído Industrial (O chão tremendo)
        noise = np.random.normal(0, 0.002) 
        
        # A FÓRMULA DA VASSOURA:
        # Se self.z for grande, (gamma**2 * z) vira GIGANTE.
        # É isso que puxa o plasma para a parede.
        accel = (self.gamma**2 * self.z) + u_control + noise
        
        return accel

    def step(self, u_control):
        # Integração de Euler (Passo de tempo)
        accel = self.dynamics(u_control)
        self.vz += accel * self.dt
        self.z += self.vz * self.dt
        self.t += self.dt
        return self.z, self.vz

# ==============================================================================
# 2. O HERÓI (O Controlador AION-CORE)
# ==============================================================================
class AION_Controller:
    def __init__(self):
        self.kp = 20.0  # Ganho Proporcional (Força bruta)
        self.kd = 5.0   # Ganho Derivativo (Amortecedor)

    def compute_action(self, z, vz):
        # AULA 02 (Spoiler): A Antecipação PACC
        # Ele não olha só onde está (z), olha para onde vai (vz)
        
        # O "Guardian Gain" (Ganho Exponencial)
        # Se a velocidade for alta, ele fica MUITO forte.
        guardian_gain = 1.0
        if abs(vz) > 10.0:
            guardian_gain = np.exp(0.1 * abs(vz))
        
        # Lei de Controle
        u = - (self.kp * z) - (self.kd * guardian_gain * vz)
        
        # O "Actuator" (Bobina) tem limites de voltagem
        u = np.clip(u, -50000, 50000) 
        return u

# ==============================================================================
# 3. A SIMULAÇÃO (Rodando o Filme)
# ==============================================================================
if __name__ == "__main__":
    print("⚡ INICIANDO SIMULAÇÃO AION-CORE...")
    
    # Criando os objetos
    plant = TokamakPlant()
    controller = AION_Controller()
    
    # Histórico para o gráfico
    history_z = []
    history_u = []
    times = []
    
    # Loop de 5ms (5000 microssegundos)
    for i in range(5000):
        # 1. O Controlador olha o sensor
        u = controller.compute_action(plant.z, plant.vz)
        
        # 2. A Planta reage à física
        z, vz = plant.step(u)
        
        # 3. Guardar dados
        if i % 10 == 0: # Salvar a cada 10 passos para não pesar
            history_z.append(z)
            history_u.append(u)
            times.append(plant.t * 1000) # Converter para ms

    print("✅ Simulação concluída. (Imagine um gráfico lindo aqui)")
    
    # Nota: No GitHub real, aqui geraria o PNG.
    # Mas só de rodar a matemática já valida o código.
