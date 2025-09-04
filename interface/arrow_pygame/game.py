from doctest import OutputChecker
import math
from tkinter import font
from matplotlib.pyplot import sca
import pygame
from interface.arrow_pygame import settings as S
from interface.arrow_pygame.entities.arrow import Arrow
from interface.arrow_pygame.entities.target import WallTarget
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# --- Composant bouton simple ---
class Button:
    def __init__(self, label: str, rect: pygame.Rect, on_click):
        self.label = label
        self.rect = rect
        self.on_click = on_click
        self.enabled = True
        self.active = False
        self.hover = False

    def draw(self, screen: pygame.Surface, font: pygame.font.Font):
        base = S.BTN_BG
        active = S.BTN_BG_ACTIVE
        disabled = (220, 220, 220)
        hover = (245, 245, 245)
        border = S.BTN_BORDER
        bg = active if self.active else base
        if not self.enabled:
            bg = disabled
        elif self.hover and not self.active:
            bg = hover
        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        pygame.draw.rect(screen, border, self.rect, 1, border_radius=8)
        txt = font.render(self.label, True, (20, 20, 20))
        screen.blit(txt, (self.rect.x + (self.rect.w - txt.get_width()) // 2,
                          self.rect.y + (self.rect.h - txt.get_height()) // 2))

    def handle_event(self, e: pygame.event.Event):
        if e.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(e.pos)
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.enabled:
            if self.rect.collidepoint(e.pos) and self.on_click:
                self.on_click()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((S.WIN_W, S.WIN_H))
        pygame.display.set_caption("Flèche — Contrôles à l'écran")
        self.clock = pygame.time.Clock()
        self.ground_px = S.WIN_H - 60

        # entités
        vx0 = S.V0 * math.cos(math.radians(S.ANGLE_DEG))
        vy0 = S.V0 * math.sin(math.radians(S.ANGLE_DEG))
        self.arrow = Arrow(0.0, 0.0, vx0, vy0)
        self.wall = WallTarget(S.WIN_W)

        # états
        self.ready = True
        self.paused = False
        self.zeno_mode = False
        self.accumulator = 0.0

        # polices
        self.font = pygame.font.SysFont("consolas", 18)
        self.font_small = pygame.font.SysFont("consolas", 16)

        # sliders
        self.sliderSpeed = Slider(self.screen,30,80,100,20,min=1,max=100,step=1,initial=42)
        self.outputSpeed = TextBox(self.screen,150,75,50,33)
        self.outputSpeed.disable()

        self.sliderAngle = Slider(self.screen,400,80,100,20,min=1,max=100,step=1,initial=38)
        self.outputAngle = TextBox(self.screen,520,75,50,33)
        self.outputAngle.disable()

        # barre de contrôle
        self.controls_h = 54
        pad = 10
        y = S.WIN_H - self.controls_h + (self.controls_h - S.BTN_H) // 2

        
        x = pad
        self.btn_launch = Button(" Lancer", pygame.Rect(x, y, 120, S.BTN_H), self.launch); x += 120 + pad
        self.btn_pause  = Button(" Pause", pygame.Rect(x, y, 120, S.BTN_H), self.toggle_pause); x += 120 + pad
        self.btn_reset  = Button(" Reset", pygame.Rect(x, y, 110, S.BTN_H), self.reset); x += 110 + pad
        self.btn_zeno   = Button(" Zénon", pygame.Rect(x, y, 120, S.BTN_H), self.toggle_zeno); x += 120 + pad
        self.btn_step   = Button(" Pas (Δt)", pygame.Rect(x, y, 140, S.BTN_H), self.step_once)
        x += 140 + pad
        self.btn_quit = Button(" Quit", pygame.Rect(x, y, 110, S.BTN_H), self.quit_game)

        self.buttons = [
        self.btn_launch, self.btn_pause, self.btn_reset,
        self.btn_zeno, self.btn_step, self.btn_quit
    ]

        self.buttons = [self.btn_launch, self.btn_pause, self.btn_reset, self.btn_zeno, self.btn_step, self.btn_quit]
        self.sync_buttons()

    # --- callbacks ---
    def launch(self):
        self.reset()
        self.ready = False
        self.paused = False
        self.sync_buttons()

    def toggle_pause(self):
        if not self.ready:
            self.paused = not self.paused
            self.sync_buttons()

    def reset(self):
        vx0 = S.V0 * math.cos(math.radians(S.ANGLE_DEG))
        vy0 = S.V0 * math.sin(math.radians(S.ANGLE_DEG))
        self.arrow.reset(0.0, 0.0, vx0, vy0)
        self.ready, self.paused, self.accumulator = True, False, 0.0
        self.sync_buttons()

    def toggle_zeno(self):
        self.zeno_mode = not self.zeno_mode
        self.sync_buttons()

    def step_once(self):
        if not self.ready and self.paused and self.arrow.active:
            self.arrow.update(S.FIXED_DT, ground_y=S.GROUND_Y_M, wall_x_m=self.wall.wall_x_m())

    def sync_buttons(self):
        self.btn_launch.enabled = True
        self.btn_pause.enabled = not self.ready
        self.btn_step.enabled  = (not self.ready) and self.paused and self.arrow.active
        self.btn_pause.label = " Reprendre" if self.paused else "Pause"
        self.btn_zeno.active = self.zeno_mode

    # --- events ---
    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            for b in self.buttons:
                b.handle_event(e)
        return True
    
    def quit_game(self):
        pygame.quit()
        raise SystemExit

    # --- update ---
    def update(self, dt: float):
        if self.ready:
            return
        self.accumulator += dt
        while self.accumulator >= S.FIXED_DT:
            if not self.paused and self.arrow.active:
                self.arrow.update(S.FIXED_DT, ground_y=S.GROUND_Y_M, wall_x_m=self.wall.wall_x_m())
            self.accumulator -= S.FIXED_DT
        self.sync_buttons()

    # --- draw ---
    def draw_controls_bar(self):
        bar_rect = pygame.Rect(0, S.WIN_H - self.controls_h, S.WIN_W, self.controls_h)
        pygame.draw.rect(self.screen, (250, 250, 250), bar_rect)
        pygame.draw.line(self.screen, (200, 200, 200), (0, bar_rect.top), (S.WIN_W, bar_rect.top), 1)
        for b in self.buttons:
            b.draw(self.screen, self.font)

    def draw(self):
        events = pygame.event.get()
        self.screen.fill(S.BG)
        pygame.draw.line(self.screen, S.GROUND, (0, self.ground_px), (S.WIN_W, self.ground_px), 3)
        self.wall.draw(self.screen, self.ground_px)
        self.arrow.draw(self.screen, self.ground_px)

        state = "PRÊT (clic  Lancer)" if self.ready else ("PAUSE" if self.paused else "EN COURS")
        self.screen.blit(self.font.render(f"État: {state}", True, S.HUD), (10, 10))
        self.screen.blit(
            self.font_small.render(
                f"v0={S.V0:.1f} m/s | angle={S.ANGLE_DEG:.1f}° | speed={math.hypot(self.arrow.vx, self.arrow.vy):.1f} m/s",
                True, (40, 40, 40)), (10, 40)
        )

        self.outputSpeed.setText(str(self.sliderSpeed.getValue()))
        self.outputAngle.setText(str(self.sliderAngle.getValue()))
        pygame_widgets.update(events)

        # Overlay Zénon (optionnel visuel simple)
        if self.zeno_mode:
            dx = self.arrow.x - getattr(self.arrow, "px", self.arrow.x)
            dy = self.arrow.y - getattr(self.arrow, "py", self.arrow.y)
            ds = math.hypot(dx, dy)
            dt = S.FIXED_DT
            ax, ay = int(self.arrow.px * S.SCALE), int(self.ground_px - self.arrow.py * S.SCALE)
            bx, by = int(self.arrow.x  * S.SCALE), int(self.ground_px - self.arrow.y  * S.SCALE)
            pygame.draw.line(self.screen, (255, 140, 0), (ax, ay), (bx, by), 3)
            pygame.draw.circle(self.screen, (255, 140, 0), (bx, by), 4)
            panel = f"ZÉNON: Δx={dx:.3f}m, Δy={dy:.3f}m, Δs={ds:.3f}m, Δt={dt:.3f}s, |v|≈{(ds/dt if dt>0 else 0):.2f}m/s"
            self.screen.blit(self.font_small.render(panel, True, (15, 15, 15)), (10, 58))

        self.draw_controls_bar()
        pygame.display.flip()

    # --- main loop ---
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(S.FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
