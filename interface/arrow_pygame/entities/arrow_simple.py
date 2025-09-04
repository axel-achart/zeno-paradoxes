# arrow_sim.py
# Simulation simple d'une flèche en 2D avec gravité (sans frottements par défaut).
# Affiche la position à chaque pas de temps et la distance à une cible.

from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Tuple

@dataclass
class Arrow:
    pos: Tuple[float, float]      # position (x, y) en mètres
    vel: Tuple[float, float]      # vitesse (vx, vy) en m/s
    g: float = 9.81               # gravité m/s² (positive, on l'applique vers -y)
    k_drag: float = 0.0           # coefficient de frottement quadratique (0 = désactivé)

    def step(self, dt: float) -> None:
        """Intègre la dynamique pendant dt secondes (Euler explicite)."""
        x, y = self.pos
        vx, vy = self.vel

        # Accélération due à la gravité
        ax, ay = 0.0, -self.g

        # (Option) frottements quadratiques ~ -k * |v| * v
        if self.k_drag > 0.0:
            speed = math.hypot(vx, vy)
            ax += -self.k_drag * speed * vx
            ay += -self.k_drag * speed * vy

        # Intégration (Euler)
        vx += ax * dt
        vy += ay * dt
        x  += vx * dt
        y  += vy * dt

        self.pos = (x, y)
        self.vel = (vx, vy)

def simulate(
    v0: float = 45.0,          # vitesse initiale (m/s)
    angle_deg: float = 40.0,   # angle de tir (degrés)
    target: Tuple[float, float] = (60.0, 0.0),  # cible (x,y) en m
    dt: float = 0.02,          # pas de temps (s)
    k_drag: float = 0.0,       # frottements (0 = off)
    max_t: float = 10.0        # garde-fou
) -> None:
    angle = math.radians(angle_deg)
    vx0 = v0 * math.cos(angle)
    vy0 = v0 * math.sin(angle)

    arrow = Arrow(pos=(0.0, 0.0), vel=(vx0, vy0), k_drag=k_drag)
    t = 0.0
    step = 0

    print(f"=== Simulation flèche ===")
    print(f"v0={v0} m/s, angle={angle_deg}°, dt={dt}s, k_drag={k_drag}")
    print(f"Cible à {target} m (x,y)\n")

    while t <= max_t:
        x, y = arrow.pos
        # Distance à la cible
        d = math.hypot(target[0] - x, target[1] - y)
        print(f"t={t:5.2f}s | step={step:4d} | pos=({x:7.3f}, {y:7.3f}) m | dist_cible={d:7.3f} m")

        # Condition d'arrêt: la flèche touche le sol (y <= 0 après avoir décollé)
        if step > 0 and y <= 0.0:
            print("\n→ La flèche a touché le sol.")
            break

        arrow.step(dt)
        t += dt
        step += 1

if __name__ == "__main__":
    # Modifiez ces paramètres librement
    simulate(
        v0=45.0,
        angle_deg=40.0,
        target=(60.0, 0.0),
        dt=0.02,
        k_drag=0.0,   # essayez 0.02 pour voir l'effet des frottements
        max_t=10.0,
    )
