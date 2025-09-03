from __future__ import annotations
from dataclasses import dataclass
import pygame
from typing import Tuple
from .. import settings as S
from ..utils import load_image, world_to_screen

@dataclass
class Target:
    x: float
    y: float
    radius_m: float = 0.4  # rayon collision en mètres
    sprite: pygame.Surface | None = None

    def __post_init__(self) -> None:
        if self.sprite is None:
            img = load_image(S.TARGET_IMG)
            if img is None:
                # bullseye de secours
                size = 44
                img = pygame.Surface((size, size), pygame.SRCALPHA)
                center = (size // 2, size // 2)
                for r, col in [(22,(200,0,0)), (15,(255,255,255)), (8,(200,0,0)), (3,(255,255,255))]:
                    pygame.draw.circle(img, col, center, r)
            self.sprite = img

    def draw(self, screen: pygame.Surface, ground_px: int) -> None:
        pos = world_to_screen(self.x, self.y, ground_px)
        if self.sprite:
            rect = self.sprite.get_rect(center=pos)
            screen.blit(self.sprite, rect)
        else:
            pygame.draw.circle(screen, (200, 0, 0), pos, max(4, int(self.radius_m * S.SCALE)))

    def hit_test(self, x: float, y: float) -> bool:
        dx, dy = (self.x - x), (self.y - y)
        return (dx*dx + dy*dy) <= (self.radius_m * self.radius_m)
