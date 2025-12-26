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
    epsilon: float = 0.02

class RobustTubeMPC:
    def __init__(self, cfg: MPCConfig):
        self.cfg = cfg
        self.K_inf = np.array([[-0.8, -0.2, 0.0, 0.0], [0.0, -0.6, -0.1, 0.0], [0.0, 0.0, -0.4, -0.2]])

    def solve(self, x_meas, x_ref, A_hat, B_hat):
        nu = B_hat.shape[1]
        base = np.array([np.zeros(nu), 0.5 * self.cfg.u_max, -0.5 * self.cfg.u_max])
        num = base.shape[0]
        x_pred = np.tile(x_meas, (num, 1))
        cum_cost = np.zeros(num)
        
        for k in range(self.cfg.N):
            x_pred = x_pred @ A_hat.T + base @ B_hat.T
            e = x_pred - x_ref
            state_cost = np.sum((e @ self.cfg.Q) * e, axis=1)
            ctrl_cost = np.sum((base @ self.cfg.R) * base, axis=1)
            term_cost = np.sum((e @ self.cfg.P_terminal) * e, axis=1) if k == self.cfg.N - 1 else 0.0
            cum_cost += state_cost + ctrl_cost + term_cost

        best_idx = np.argmin(cum_cost)
        return np.clip(base[best_idx] + self.K_inf @ (x_meas - x_ref), self.cfg.u_min, self.cfg.u_max)