from __future__ import annotations
from dataclasses import dataclass
import math
from . import settings as S

@dataclass
class World:
    g: float = S.G
    k_drag: float = S.K_DRAG

    def step(self, x: float, y: float, vx: float, vy: float, dt: float) -> tuple[float, float, float, float]:
        # Accélérations
        ax, ay = 0.0, -self.g
        if self.k_drag > 0.0:
            speed = math.hypot(vx, vy)
            ax += -self.k_drag * speed * vx
            ay += -self.k_drag * speed * vy

        # Semi-implicite (symplectic Euler) : v ← v + a dt ; x ← x + v dt
        vx += ax * dt
        vy += ay * dt
        x  += vx * dt
        y  += vy * dt

        return x, y, vx, vy
