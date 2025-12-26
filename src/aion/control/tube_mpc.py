import numpy as np
from dataclasses import dataclass

@dataclass
class MPCConfig:
    Q: np.ndarray
    R: np.ndarray
    P_terminal: np.ndarray
    u_min: np.ndarray
    u_max: np.ndarray
    N: int = 5

class RobustTubeMPC:
    def __init__(self, cfg: MPCConfig):
        self.cfg = cfg
        self.K_inf = np.array([[-0.8, -0.2, 0.0, 0.0], [0.0, -0.6, -0.1, 0.0], [0.0, 0.0, -0.4, -0.2]])

    def solve(self, x_meas, x_ref, A_hat, B_hat):
        u_nom = -self.K_inf @ (x_meas - x_ref)
        return np.clip(u_nom, self.cfg.u_min, self.cfg.u_max)