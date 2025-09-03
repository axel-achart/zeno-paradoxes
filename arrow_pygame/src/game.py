# src/game.py
from __future__ import annotations
import math
import pygame
from typing import Tuple, List
from . import settings as S
from .physics import World
from .utils import world_to_screen, clamp
from .entities.arrow import Arrow
from .entities.target import Target


class HUD:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("consolas", 18)
        self.small = pygame.font.SysFont("consolas", 16)

    def draw_text(self, screen: pygame.Surface, text_lines: list[str]) -> None:
        y = 10
        for line in text_lines:
            surf = self.font.render(line, True, S.HUD_COLOR)
            screen.blit(surf, (10, y))
            y += 22


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((S.WIN_W, S.WIN_H))
        pygame.display.set_caption("Flèche en vol — Pygame (pause visible, limite & time scale)")
        self.clock = pygame.time.Clock()
        self.hud = HUD()

        self.world = World(g=S.G, k_drag=S.K_DRAG)
        vx0 = S.V0 * math.cos(math.radians(S.ANGLE_DEG))
        vy0 = S.V0 * math.sin(math.radians(S.ANGLE_DEG))
        self.arrow = Arrow(self.world, x=0.0, y=0.0, vx=vx0, vy=vy0)
        self.target = Target(x=60.0, y=0.0)

        self.paused = False
        self.hold_target = False
        self.scale = S.SCALE
        self.ground_px = S.WIN_H - 60

        # --- Time scale ---
        self.time_scale = S.TIME_SCALE_DEFAULT
        self.accumulator = 0.0

        # --- UI rects (positions fixes) ---
        self.btn_pause_rect = pygame.Rect(10, S.WIN_H - 50, S.BTN_W, S.BTN_H)
        self.slider_rect = pygame.Rect(160, S.WIN_H - 32, S.SLIDER_W, S.SLIDER_H)
        self.slider_dragging = False


    def reset_arrow(self) -> None:
        vx0 = S.V0 * math.cos(math.radians(S.ANGLE_DEG))
        vy0 = S.V0 * math.sin(math.radians(S.ANGLE_DEG))
        self.arrow.reset(0.0, 0.0, vx0, vy0)

    def toggle_drag(self) -> None:
        self.world.k_drag = 0.0 if self.world.k_drag > 0.0 else 0.02

    def handle_events(self) -> bool:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                if e.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if e.key == pygame.K_r:
                    self.reset_arrow()
                    self.paused = False
                if e.key == pygame.K_d:
                    self.toggle_drag()
                if e.key == pygame.K_c:
                    self.scale = {9.0: 7.0, 7.0: 11.0, 11.0: 9.0}.get(self.scale, 9.0)
                if e.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    self.set_v0(S.V0 + 2.0)
                if e.key == pygame.K_MINUS:
                    self.set_v0(S.V0 - 2.0)
                if e.key == pygame.K_LEFT:
                    self.set_angle(S.ANGLE_DEG - 1.0)
                if e.key == pygame.K_RIGHT:
                    self.set_angle(S.ANGLE_DEG + 1.0)
                # Raccourcis time-scale
                if e.key == pygame.K_LEFTBRACKET:   # [
                    self.set_time_scale(self.time_scale * 0.9)
                if e.key == pygame.K_RIGHTBRACKET:  # ]
                    self.set_time_scale(self.time_scale * 1.1)

            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.btn_pause_rect.collidepoint(e.pos):
                        self.paused = not self.paused
                    # slider
                    if self.slider_rect.collidepoint(e.pos):
                        self.slider_dragging = True
                        self._update_time_scale_from_mouse(e.pos[0])
                    # drag cible
                    mx, my = e.pos
                    xw = mx / self.scale
                    yw = (self.ground_px - my) / self.scale
                    if self.target.hit_test(xw, yw):
                        self.hold_target = True

            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.slider_dragging = False
                    self.hold_target = False

            if e.type == pygame.MOUSEMOTION:
                if self.slider_dragging:
                    self._update_time_scale_from_mouse(e.pos[0])
                if self.hold_target:
                    mx, my = e.pos
                    self.target.x = clamp(mx / self.scale, 0.0, 1e6)
                    self.target.y = clamp((self.ground_px - my) / self.scale, 0.0, 1000.0)
        return True
    
    def _update_time_scale_from_mouse(self, mouse_x: int) -> None:
        # position 0..1 dans le slider
        t = clamp((mouse_x - self.slider_rect.x) / self.slider_rect.w, 0.0, 1.0)
        # interpolation linéaire
        val = S.TIME_SCALE_MIN + t * (S.TIME_SCALE_MAX - S.TIME_SCALE_MIN)
        self.set_time_scale(val)

    def set_time_scale(self, val: float) -> None:
        self.time_scale = clamp(val, S.TIME_SCALE_MIN, S.TIME_SCALE_MAX)


    def set_v0(self, v: float) -> None:
        from . import settings as Smod
        Smod.V0 = clamp(v, 5.0, 200.0)
        self.reset_arrow()

    def set_angle(self, angle_deg: float) -> None:
        from . import settings as Smod
        Smod.ANGLE_DEG = clamp(angle_deg, 5.0, 85.0)
        self.reset_arrow()

    def update(self, dt: float) -> None:
        # on “accélère/ralentit” le temps en multipliant l’accumulateur
        self.accumulator += dt * self.time_scale
        while self.accumulator >= S.FIXED_DT:
            if not self.paused:
                self.arrow.update(S.FIXED_DT, self.target)
            self.accumulator -= S.FIXED_DT


    def draw(self) -> None:
        self.screen.fill(S.BG_COLOR)
        pygame.draw.line(self.screen, S.GROUND_COLOR, (0, self.ground_px), (S.WIN_W, self.ground_px), 3)

        # --- Projection future (limite jusqu'à l'arrêt au sol) ---
        ghost, land_x = self.compute_projection()
        if len(ghost) > 1:
            # pointillés
            prev = None
            for p in ghost[::3]:  # espacer les points
                if prev:
                    a = world_to_screen(prev[0], prev[1], self.ground_px)
                    b = world_to_screen(p[0], p[1], self.ground_px)
                    pygame.draw.line(self.screen, S.DASH_COLOR, a, b, 1)
                prev = p
            # marqueur d'atterrissage (ligne verticale + tick au sol)
            lx, ly = world_to_screen(land_x, 0.0, self.ground_px)
            pygame.draw.line(self.screen, S.LAND_COLOR, (lx, self.ground_px-40), (lx, self.ground_px), 2)
            pygame.draw.line(self.screen, S.LAND_COLOR, (lx-6, self.ground_px), (lx+6, self.ground_px), 2)

        # Cible + flèche
        self.target.draw(self.screen, self.ground_px)
        self.arrow.draw(self.screen, self.ground_px)

        # HUD texte
        hit = self.target.hit_test(self.arrow.x, self.arrow.y)
        status = "HIT! 🎯" if hit else ""
        hud_lines = [
            f"v0={S.V0:.1f} m/s | angle={S.ANGLE_DEG:.1f}° | drag={self.world.k_drag:.3f} | speed={self.arrow.speed:.1f} m/s",
            f"arrow: x={self.arrow.x:.1f} m, y={self.arrow.y:.1f} m  |  target: x={self.target.x:.1f} m, y={self.target.y:.1f} m  {status}",
            "Controls: Bouton Pause | R=Reset | D=Drag | C=Scale | +/-=V0 | ←/→=Angle | [ / ] = Time× | Échap=Quit",
        ]
        self.hud.draw_text(self.screen, hud_lines)

        # UI interactifs
        self.draw_button_pause()
        self.draw_slider_timescale()

        pygame.display.flip()


    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(S.FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()

    def compute_projection(self, max_secs: float = 12.0) -> Tuple[List[Tuple[float,float]], float]:
        """
        Simule, sans toucher à l'état réel, la trajectoire future jusqu'au sol (y<=0).
        Retourne la liste des points 'fantômes' et la position x d'atterrissage.
        """
        x, y, vx, vy = self.arrow.x, self.arrow.y, self.arrow.vx, self.arrow.vy
        points: List[Tuple[float,float]] = []
        t = 0.0
        dt = S.FIXED_DT  # même intégrateur que le monde
        while t < max_secs and y >= S.GROUND_Y_M:
            x, y, vx, vy = self.world.step(x, y, vx, vy, dt)
            points.append((x, y))
            t += dt
        land_x = x
        return points, land_x

    def draw_button_pause(self) -> None:
        rect = self.btn_pause_rect
        active = self.paused
        bg = S.BTN_BG_ACTIVE if active else S.BTN_BG
        pygame.draw.rect(self.screen, bg, rect, border_radius=8)
        pygame.draw.rect(self.screen, S.BTN_BORDER, rect, 1, border_radius=8)
        label = "▶ Reprendre" if self.paused else "⏸ Pause"
        txt = self.hud.font.render(label, True, (20,20,20))
        self.screen.blit(txt, (rect.x + 12, rect.y + 7))

    def draw_slider_timescale(self) -> None:
        # rail
        pygame.draw.rect(self.screen, S.SLIDER_BG, self.slider_rect, border_radius=3)
        # position handle
        t = (self.time_scale - S.TIME_SCALE_MIN) / (S.TIME_SCALE_MAX - S.TIME_SCALE_MIN)
        t = clamp(t, 0.0, 1.0)
        x = int(self.slider_rect.x + t * self.slider_rect.w)
        pygame.draw.rect(self.screen, S.SLIDER_FG, (self.slider_rect.x, self.slider_rect.y, x - self.slider_rect.x, S.SLIDER_H), border_radius=3)
        pygame.draw.circle(self.screen, (30,30,30), (x, self.slider_rect.y + S.SLIDER_H//2), 8)
        # label
        label = self.hud.small.render(f"Time× {self.time_scale:.2f}   ([ ] pour -/+)", True, (30,30,30))
        self.screen.blit(label, (self.slider_rect.x, self.slider_rect.y - 18))
