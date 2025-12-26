class TitanInterlock:
    def check(self, z_pos):
        return "SCRAM" if abs(z_pos) > 0.10 else "OK"