from __future__ import annotations

# Fenêtre
WIN_W, WIN_H = 1200, 700
FPS = 60

# Monde (unités en mètres)
G = 9.81          # gravité
SCALE = 9.0       # pixels par mètre
GROUND_Y_M = 0.0  # niveau du sol en coordonnées monde (y=0)

# Tir initial
V0 = 45.0         # m/s
ANGLE_DEG = 40.0  # degrés

# Frottement quadratique ~ -k*|v|*v (0 = désactivé)
K_DRAG = 0.0

# Simulation
FIXED_DT = 1.0 / 120.0  # intégration à pas fixe (plus stable)
MAX_TRAIL = 1500        # points max dans la trajectoire

# UI
BG_COLOR = (245, 245, 245)
GROUND_COLOR = (60, 60, 60)
TRAIL_COLOR = (20, 90, 180)
HUD_COLOR = (15, 15, 15)

# Assets
ASSETS_DIR = "assets"
ARROW_IMG = "arrow.png"
TARGET_IMG = "target.png"


TIME_SCALE_MIN = 0.05
TIME_SCALE_MAX = 3.0
TIME_SCALE_DEFAULT = 1.0

# UI Bouton & Slider
BTN_W, BTN_H = 130, 36
BTN_BG = (235, 235, 235)
BTN_BG_ACTIVE = (210, 235, 210)
BTN_BORDER = (60, 60, 60)
SLIDER_W, SLIDER_H = 220, 6
SLIDER_BG = (210, 210, 210)
SLIDER_FG = (40, 120, 220)
DASH_COLOR = (140, 140, 140)  # projection en pointillés
LAND_COLOR = (220, 120, 40)   # marqueur d’atterrissage
