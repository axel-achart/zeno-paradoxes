from random import choice
import time
import pygame
import sys
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

# Simulation parameterspip
speed_achille = 10
speed_tortoise = speed_achille / 2
position_achille = 0
position_tortoise = 100
iteration = 0
total_time = 0

WIDTH, HEIGHT = 800, 600
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
    time.sleep(1)
    return position_achille, position_tortoise, iteration, total_time

def race(position_achille, position_tortoise,speed_achille, speed_tortoise, iteration, total_time):
    position_achille += speed_achille
    position_tortoise += speed_tortoise
    iteration += 1
    total_time += 1
    return position_achille, position_tortoise, iteration, total_time


def main_achille():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zeno Paradox - Achille and the Tortoise")
    mode = None

    sliderTurtlePos = Slider(screen, 230, 120, 400, 40, min=10, max=99, step=1, initial=10)
    outputTurtlePos = TextBox(screen, 680, 115, 80, 50, fontSize=30)
    outputTurtlePos.disable()

    sliderTurtleSpeed = Slider(screen, 230, 220, 400, 40, min=0, max=100, step=1,initial=5)
    outputTurtleSpeed = TextBox(screen, 680, 215, 80, 50, fontSize=30)
    outputTurtleSpeed.disable()

    sliderAchilleSpeed = Slider(screen, 230, 320, 400, 40, min=0, max=100, step=1,initial=10)
    outputAchilleSpeed = TextBox(screen, 680, 315, 80, 50, fontSize=30)
    outputAchilleSpeed.disable()


    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    conditionmsg = font.render("Keep in mind that Achille IS faster than the turtle",True,(255,0,0))

    choosing = True

    while choosing:
    
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if sliderAchilleSpeed.getValue()>sliderTurtleSpeed.getValue():    
                        mode = 1
                        choosing =False
                    else:
                        screen.blit(conditionmsg,(210,80))
                        pygame.display.flip()
                        time.sleep(2)
                        clock.tick(30)
                if event.key == pygame.K_b:
                    if sliderAchilleSpeed.getValue()>sliderTurtleSpeed.getValue():    
                        mode = 2
                        choosing =False
                    else:
                        screen.blit(conditionmsg,(210,80))
                        pygame.display.flip()
                        time.sleep(2)
                        clock.tick(30)


        screen.fill(WHITE)
        turtleposmsg = font.render("Turtle Position",True,BLACK)
        turtlespeedmsg = font.render("Turtle Speed",True, BLACK)
        achillespeedmsg = font.render("Achille Speed",True, BLACK)
        slidermsg = font.render("Try to change the parameters of the simulation",True,BLACK)
        choicemsg = font.render("Press a for Zeno Paradox, Press b for the normal race",True,BLACK)
        screen.blit(slidermsg, (200, 50))
        screen.blit(choicemsg, (200, HEIGHT//2 + 220))
        screen.blit(turtleposmsg,(50,133))
        screen.blit(turtlespeedmsg,(50,233))
        screen.blit(achillespeedmsg,(50,333))

        
        # Draw Sliders
        outputTurtlePos.setText(str(sliderTurtlePos.getValue()))
        outputTurtleSpeed.setText(str(sliderTurtleSpeed.getValue()))
        outputAchilleSpeed.setText(str(sliderAchilleSpeed.getValue()))
        pygame_widgets.update(events)

        pygame.display.flip()
        clock.tick(30)

    running = True
    achille_x = position_achille
    tortoise_x = sliderTurtlePos.getValue()
    iteration = 0
    total_time = 0

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    choosing = True

        screen.fill(WHITE)

        # Draw Achille
        pygame.draw.circle(screen, ACHILLE_COLOR, (int(achille_x)+50, HEIGHT//2-30), 20)
        achille_label = font.render(f"Achille: {achille_x:.2f}m", True, BLACK)
        screen.blit(achille_label, (int(achille_x)+30, HEIGHT//2))

        # Draw Tortoise
        pygame.draw.circle(screen, TORTOISE_COLOR, (int(tortoise_x)+50, HEIGHT//2+60), 20)
        tortoise_label = font.render(f"Tortoise: {tortoise_x:.2f}m", True, BLACK)
        screen.blit(tortoise_label, (int(tortoise_x)+30, HEIGHT//2+90))

        # Draw Info
        info = font.render(f"Iteration: {iteration}  Total time: {total_time:.2f}s  Mode: {mode}", True, BLACK)
        screen.blit(info, (10, 10))



        pygame.display.flip()
        clock.tick(1)  # Slow down for visualization
        print(mode)
        # Update positions
        if achille_x < tortoise_x:
            if mode == 1:
                achille_x, tortoise_x, iteration, total_time = move_ach_to_tort(
                    achille_x, tortoise_x, sliderAchilleSpeed.getValue(), sliderTurtleSpeed.getValue(), iteration, total_time
                )
            elif mode == 2:
                achille_x, tortoise_x, iteration, total_time = race(
                    achille_x,tortoise_x,sliderAchilleSpeed.getValue(),sliderTurtleSpeed.getValue(), iteration, total_time
                )
            print(f"pos T = {tortoise_x}\nspeed T {speed_tortoise}\nspeed A {speed_achille}") 

        else:
            end_text = font.render("Achille has caught back the Tortoise!", True, (200, 0, 0))
            screen.blit(end_text, (WIDTH//2-100, HEIGHT//2-10))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

if __name__ == "__main__":
    main_achille()