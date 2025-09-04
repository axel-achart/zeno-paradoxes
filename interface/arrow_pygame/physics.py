from interface.arrow_pygame import settings as S

def step(x: float, y: float, vx: float, vy: float, dt: float) -> tuple[float, float, float, float]:
    """Euler semi-implicite avec gravité (sans frottements)."""
    ax, ay = 0.0, -S.G
    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt
    return x, y, vx, vy
