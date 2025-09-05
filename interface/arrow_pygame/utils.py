from interface.arrow_pygame import settings as S


def world_to_screen(x_m: float, y_m: float, ground_px: int) -> tuple[int, int]:
    return int(x_m * S.SCALE), int(ground_px - y_m * S.SCALE)
