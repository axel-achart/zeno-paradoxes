from __future__ import annotations
import os
import math
import pygame
from typing import Tuple
from . import settings as S

Vec2 = Tuple[float, float]

def assets_path(name: str) -> str:
    return os.path.join(S.ASSETS_DIR, name)

def load_image(name: str) -> pygame.Surface | None:
    path = assets_path(name)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        return img
    return None

def rotate_center(image: pygame.Surface, angle_deg: float) -> pygame.Surface:
    # angle en degrés (pygame rotate: sens antihoraire)
    return pygame.transform.rotate(image, angle_deg)

def world_to_screen(x_m: float, y_m: float, ground_px: int) -> tuple[int, int]:
    """Convertit coordonnées monde (m) -> écran (px). y monde ↑, y écran ↓"""
    x_px = int(x_m * S.SCALE)
    y_px = int(ground_px - y_m * S.SCALE)
    return x_px, y_px

def norm(vx: float, vy: float) -> float:
    return math.hypot(vx, vy)

def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))
