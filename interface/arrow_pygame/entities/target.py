import pygame
from interface.arrow_pygame import settings as S


class WallTarget:
    def __init__(self, screen_w: int, thickness_px: int = 8):
        self.screen_w = screen_w
        self.thickness_px = thickness_px

    def draw(self, screen: pygame.Surface, ground_px: int):
        rect = pygame.Rect(self.screen_w - self.thickness_px, 0, self.thickness_px, ground_px)
        pygame.draw.rect(screen, S.WALL, rect)

    def wall_x_m(self) -> float:
        return (self.screen_w - self.thickness_px) / S.SCALE
