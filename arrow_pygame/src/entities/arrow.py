# src/entities/arrow.py
from __future__ import annotations
from dataclasses import dataclass, field
import math
import pygame
from typing import List, Tuple
from .. import settings as S
from ..utils import load_image, rotate_center, world_to_screen, norm

@dataclass
class Arrow:
    world: "World"
    x: float
    y: float
    vx: float
    vy: float
    active: bool = True
    trail: List[Tuple[float, float]] = field(default_factory=list)
    sprite_base: pygame.Surface | None = None

    def __post_init__(self) -> None:
        if self.sprite_base is None:
            img = load_image(S.ARROW_IMG)
            if img is None:
                img = pygame.Surface((80, 20), pygame.SRCALPHA)
                pygame.draw.polygon(img, (10, 120, 10), [(10,10),(70,3),(70,17)])
                pygame.draw.polygon(img, (0, 60, 0), [(65,10),(78,4),(78,16)])
            self.sprite_base = img

    def reset(self, x: float, y: float, vx: float, vy: float) -> None:
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.trail.clear()
        self.active = True

    def update(self, dt: float, target=None) -> None:
        if not self.active:
            return
        # Avance physique
        self.x, self.y, self.vx, self.vy = self.world.step(self.x, self.y, self.vx, self.vy, dt)
        self.trail.append((self.x, self.y))
        if len(self.trail) > S.MAX_TRAIL:
            self.trail.pop(0)
        # Arrêts (sol / cible)
        if self.y <= S.GROUND_Y_M:
            self.active = False
        if target and target.hit_test(self.x, self.y):
            self.active = False

    def draw(self, screen: pygame.Surface, ground_px: int) -> None:
        # Trajectoire
        if len(self.trail) > 1:
            pts = [world_to_screen(x, y, ground_px) for (x, y) in self.trail if y >= -5]
            if len(pts) > 1:
                pygame.draw.lines(screen, S.TRAIL_COLOR, False, pts, 2)
        # Sprite orienté
        if self.sprite_base:
            angle_rad = math.atan2(-self.vy, self.vx)  # -vy car y écran va vers le bas
            angle_deg = math.degrees(angle_rad)
            spr = rotate_center(self.sprite_base, angle_deg)
            rect = spr.get_rect(center=world_to_screen(self.x, self.y, ground_px))
            screen.blit(spr, rect)
        else:
            pygame.draw.circle(screen, (0, 120, 0), world_to_screen(self.x, self.y, ground_px), 6)

    @property
    def speed(self) -> float:
        return norm(self.vx, self.vy)
