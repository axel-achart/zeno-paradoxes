import pygame
import sys

# Simulation parameters
speed_achille = 10
speed_tortoise = speed_achille / 2
position_achille = 0
position_tortoise = 100
iteration = 0
total_time = 0

WIDTH, HEIGHT = 800, 200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ACHILLE_COLOR = (0, 128, 255)
TORTOISE_COLOR = (0, 200, 0)

def move_ach_to_tort(position_achille, position_tortoise, speed_achille, speed_tortoise, iteration, total_time):
    length_achille_to_tortoise = position_tortoise - position_achille
    position_achille = position_tortoise
    time_spent = length_achille_to_tortoise / speed_achille
    position_tortoise = position_tortoise + time_spent * speed_tortoise
    iteration += 1
    total_time += time_spent
    return position_achille, position_tortoise, iteration, total_time

def race(position_achille, speed_achille, position_tortoise, speed_tortoise, iteration, total_time):
    position_achille += speed_achille
    position_tortoise += speed_tortoise
    iteration += 1
    total_time += 1
    return position_achille, position_tortoise, iteration, total_time


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Achille and the Tortoise")
    mode = None

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    choosing = True

    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mode = 1
                    choosing =False
                if event.key == pygame.K_b:
                    mode = 2
                    choosing =False

        screen.fill(WHITE)
        msg = font.render("Press a for Zeno Paradox, Press b for the normal race",True,BLACK)
        screen.blit(msg, (50, HEIGHT//2 - 20))
        pygame.display.flip()
        clock.tick(30)

    running = True
    achille_x = position_achille
    tortoise_x = position_tortoise
    iteration = 0
    total_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw Achille
        pygame.draw.circle(screen, ACHILLE_COLOR, (int(achille_x)+50, HEIGHT//2-30), 20)
        achille_label = font.render(f"Achille: {achille_x:.2f}m", True, BLACK)
        screen.blit(achille_label, (int(achille_x)+30, HEIGHT//2-60))

        # Draw Tortoise
        pygame.draw.circle(screen, TORTOISE_COLOR, (int(tortoise_x)+50, HEIGHT//2+30), 20)
        tortoise_label = font.render(f"Tortoise: {tortoise_x:.2f}m", True, BLACK)
        screen.blit(tortoise_label, (int(tortoise_x)+30, HEIGHT//2+10))

        # Draw info
        info = font.render(f"Iteration: {iteration}  Total time: {total_time:.2f}s  Mode: {mode}", True, BLACK)
        screen.blit(info, (10, 10))

        pygame.display.flip()
        clock.tick(1)  # Slow down for visualization
        print(mode)
        # Update positions
        if achille_x < tortoise_x:
            if mode == 1:
                achille_x, tortoise_x, iteration, total_time = move_ach_to_tort(
                    achille_x, tortoise_x, speed_achille, speed_tortoise, iteration, total_time
                )
            elif mode == 2:
                achille_x, tortoise_x, iteration, total_time = race(
                    achille_x, speed_achille, tortoise_x, speed_tortoise, iteration, total_time
                )
        else:
            end_text = font.render("Achille has caught the Tortoise!", True, (200, 0, 0))
            screen.blit(end_text, (WIDTH//2-100, HEIGHT//2-10))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

if __name__ == "__main__":
    main()