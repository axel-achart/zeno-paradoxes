# Pygame Version

import pygame
from config import *

TREE = "zeno-paradoxes/assets/img/tree.png"
ROCK = "zeno-paradoxes/assets/img/rock.jpg"


def dichotomie():
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dichotomie Paradox")

    font = pygame.font.Font(None, 36)

    distance_total = 8
    distance_restante = distance_total
    etape = 1

    margin = 100
    line_y = SCREEN_HEIGHT // 2
    rock_size = 50
    tree_size = 70  

    start_x = margin
    end_x = SCREEN_WIDTH - margin

    # Images
    rock_img = pygame.image.load(ROCK)
    tree_img = pygame.image.load(TREE)
    rock_img = pygame.transform.scale(rock_img, (rock_size, rock_size))
    tree_img = pygame.transform.scale(tree_img, (tree_size, tree_size))

    screen.fill(BACKGROUND_COLOR)
    text_init = font.render(f"Étape 0 = distance initiale : 8.000m", True, (0, 0, 0))
    screen.blit(text_init, (SCREEN_WIDTH // 2 - text_init.get_width() // 2, 40))
    pygame.draw.line(screen, (0, 0, 0), (start_x, line_y), (end_x, line_y), 5)
    rock_x = start_x
    screen.blit(rock_img, (rock_x - rock_size // 2, line_y - rock_size // 2))
    screen.blit(tree_img, (end_x - tree_size // 2, line_y - tree_size // 2))
    pygame.display.flip()
    pygame.time.delay(1500)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        if distance_restante > 0.01:
            distance_restante = distance_restante / 2
            position = distance_total - distance_restante

            pygame.draw.line(screen, (0, 0, 0), (start_x, line_y), (end_x, line_y), 5)

            rock_x = start_x + (position / distance_total) * (end_x - start_x)

            screen.blit(rock_img, (rock_x - rock_size // 2, line_y - rock_size // 2))
            screen.blit(tree_img, (end_x - tree_size // 2, line_y - tree_size // 2))
            
            text = font.render(f"Étape {etape} = distance restante : {distance_restante:.3f} m", True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 40))

            etape += 1

            pygame.display.flip()
            pygame.time.delay(1500) 

        else:
            pygame.quit()

dichotomie()