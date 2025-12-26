import numpy as np

class SquareRootRLS:
    def __init__(self, n_params: int, lambda_init: float = 0.995, delta: float = 100.0):
        self.n_params = n_params
        self.lambda_ = lambda_init
        self.S = np.eye(n_params) * np.sqrt(delta)
        self.theta = np.zeros(n_params)

    def reset_covariance(self, delta: float = 100.0):
        self.S = np.eye(self.n_params) * np.sqrt(delta)

    def update(self, phi: np.ndarray, y: float) -> np.ndarray:
        phi = phi.reshape(-1, 1)
        y_hat = float(self.theta @ phi.flatten())
        error = y - y_hat
        self.lambda_ = 0.98 if abs(error) > 0.05 else 0.995

        A = np.block([[np.sqrt(self.lambda_) * self.S, phi], [np.zeros((1, self.n_params)), 1.0]])
        try:
            _, R = np.linalg.qr(A.T)
            self.S = R[:self.n_params, :self.n_params].T
        except np.linalg.LinAlgError:
            self.reset_covariance()
            return self.theta

        P_curr = self.S @ self.S.T
        denom = float((self.lambda_ + phi.T @ P_curr @ phi).item())
        K = (P_curr @ phi) / denom if denom > 1e-9 else np.zeros((self.n_params, 1))
        self.theta += (K.flatten() * error)
        return self.theta