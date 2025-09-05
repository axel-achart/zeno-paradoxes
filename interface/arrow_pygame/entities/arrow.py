import math
import pygame
from interface.arrow_pygame import settings as S, physics, utils


class Arrow:
    def __init__(self, x: float, y: float, vx: float, vy: float):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.px, self.py = x, y        # position précédente (pour Δs en mode Zénon)
        self.active = True
        self.trail: list[tuple[float, float]] = []

        # Sprite petit (~60x30 px), orienté par défaut vers la gauche puis flip → droite
        self.sprite = pygame.Surface((60, 30), pygame.SRCALPHA)
        pygame.draw.rect(self.sprite, (160, 120, 60), pygame.Rect(6, 4, 24, 2))       # fût
        pygame.draw.polygon(self.sprite, (200, 40, 40), [(4, 5), (10, 1), (10, 9)])   # empennage
        pygame.draw.polygon(self.sprite, (160, 160, 160), [(28, 5), (38, 1), (38, 9)])# pointe
        self.sprite = pygame.transform.flip(self.sprite, True, False)                 # pointe → droite

    def reset(self, x: float, y: float, vx: float, vy: float):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.px, self.py = x, y
        self.trail.clear()
        self.active = True

    def update(self, dt: float, ground_y: float, wall_x_m: float):
        """Intégration + collisions sol/mur avec clipping linéaire."""
        if not self.active:
            return

        # mémoriser position précédente (pour Δs)
        self.px, self.py = self.x, self.y

        # intégrer
        self.x, self.y, self.vx, self.vy = physics.step(self.x, self.y, self.vx, self.vy, dt)
        x0, y0 = self.px, self.py
        x1, y1 = self.x, self.y

        # sol
        if y1 <= ground_y:
            if y1 != y0:
                a = (ground_y - y0) / max(1e-9, (y1 - y0))
                self.x = x0 + a * (x1 - x0)
                self.y = ground_y
            self.active = False

        # mur à droite
        if self.active and x0 < wall_x_m <= x1 and self.vx > 0:
            a = (wall_x_m - x0) / max(1e-9, (x1 - x0))
            self.x = wall_x_m
            self.y = y0 + a * (y1 - y0)
            self.active = False

        # trace
        self.trail.append((self.x, self.y))
        if len(self.trail) > 1200:
            self.trail.pop(0)

    def draw(self, screen: pygame.Surface, ground_px: int):
        # trajectoire
        if len(self.trail) > 1:
            pts = [utils.world_to_screen(x, y, ground_px) for (x, y) in self.trail if y >= -5]
            if len(pts) > 1:
                pygame.draw.lines(screen, S.TRAIL, False, pts, 2)

        # sprite FIXE (pas de rotation)
        rect = self.sprite.get_rect(center=utils.world_to_screen(self.x, self.y, ground_px))
        screen.blit(self.sprite, rect)
