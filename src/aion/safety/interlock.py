from collections import deque
from dataclasses import dataclass

@dataclass
class TitanConfig:
    z_limit: float = 0.05
    grad_limit: float = 0.01

class TitanControlSuite:
    def __init__(self, cfg: TitanConfig = TitanConfig()):
        self.cfg = cfg
        self.z_window = deque(maxlen=50)
        self.z_precursors = 0
        
    def cycle(self, t: float, z_val: float) -> str:
        if abs(z_val) > self.cfg.z_limit: return "CRITICAL_Z_LIMIT"
        self.z_window.append(z_val)
        if len(self.z_window) > 5 and abs(self.z_window[-1] - self.z_window[-5]) > self.cfg.grad_limit:
            self.z_precursors += 1
        else:
            self.z_precursors = max(0, self.z_precursors - 1)
        if self.z_precursors > 5: return "CRITICAL_PRECURSOR_ACCUMULATION"
        return "OPTIMAL"