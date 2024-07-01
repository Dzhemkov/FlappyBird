"""
This is code by Dmitriy Zhemkov

It is a recreation of the famous game Flappy Bird

"""

import sys
import os
import pygame
import random

from HelperFunctions.bird_movement import BirdPhysics
from HelperFunctions.pipe_movement import Pipe
from HelperFunctions.button import Button

WIDTH, HEIGHT = 1500, 840
MWIDTH, MHEIGHT = 300, 168
BIRD_SPAWN = (100, 50)
SPEED = 0
CROSSED = True
SPAWN = 200

BIRD = pygame.image.load(os.path.join("Sprites", "bird.png"))
BIRD.set_colorkey((0, 0, 255))

TOP_PIPE = pygame.image.load(os.path.join("Sprites", "top_pipe.png"))
TOP_PIPE.set_colorkey((0, 0, 255))

BOTTOM_PIPE = pygame.image.load(os.path.join("Sprites", "bottom_pipe.png"))
BOTTOM_PIPE.set_colorkey((0, 0, 255))

BACKGROUND = pygame.image.load(os.path.join("Sprites", "background.png"))

START_BUTTON_IMG = pygame.image.load(os.path.join("Sprites", "start_button.png"))
START_BUTTON = Button(150 - START_BUTTON_IMG.get_width() / 2, 84 - START_BUTTON_IMG.get_height() / 2, START_BUTTON_IMG,
                      START_BUTTON_IMG.get_width(), START_BUTTON_IMG.get_height())

PLAY_AGAIN_IMG = pygame.image.load(os.path.join("Sprites", "play_again.png"))
PLAY_AGAIN_BUTTON = Button(150 - PLAY_AGAIN_IMG.get_width() / 2, 84 - PLAY_AGAIN_IMG.get_height() / 2, PLAY_AGAIN_IMG,
                           PLAY_AGAIN_IMG.get_width(), PLAY_AGAIN_IMG.get_height())

MAIN_MENU_IMG = pygame.image.load(os.path.join("Sprites", "main_menu.png"))
MAIN_MENU_BUTTON = Button(150 - MAIN_MENU_IMG.get_width() / 2, 44 - MAIN_MENU_IMG.get_height() / 2, MAIN_MENU_IMG,
                          MAIN_MENU_IMG.get_width(), MAIN_MENU_IMG.get_height())

PAUSE_BUTTON_IMG = pygame.image.load(os.path.join("Sprites", "pause_button.png"))
PAUSE_BUTTON = Button(285 - PAUSE_BUTTON_IMG.get_width() / 2, 10 - PAUSE_BUTTON_IMG.get_height() / 2, PAUSE_BUTTON_IMG,
                      PAUSE_BUTTON_IMG.get_width(), PAUSE_BUTTON_IMG.get_height())

EXIT_BUTTON_IMG = pygame.image.load(os.path.join("Sprites", "exit_button.png"))
EXIT_BUTTON = Button(150 - EXIT_BUTTON_IMG.get_width() / 2, 114 - EXIT_BUTTON_IMG.get_height() / 2, EXIT_BUTTON_IMG,
                     EXIT_BUTTON_IMG.get_width(), EXIT_BUTTON_IMG.get_height())

pipes = []

SCORE = ""
HIGH_SCORE = False

RUNNING = True
PRESSED_START = False


def main():
    global CROSSED, PRESSED_START, SCORE, HIGH_SCORE
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    pygame.display.set_icon(BIRD)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    display = pygame.Surface((MWIDTH, MHEIGHT))
    clock = pygame.time.Clock()

    bird = BirdPhysics(BIRD, BIRD_SPAWN, SPEED, pipes, RUNNING)
    bird_movement = False

    counter = 0

    score_font = pygame.font.SysFont('Courier New', 35)
    white = (255, 255, 255)

    score_message_font = pygame.font.SysFont('Courier New', 15)

    while True:

        score_img = score_font.render(str(counter), True, white)

        display.blit(BACKGROUND, (0, 0))

        if bird.running and PRESSED_START:
            bird.update(bird_movement)
        bird.render(display)

        top_ycoord = random.randrange(-110, -50)
        bottom_ycoord = top_ycoord + 175

        if bird.running and PRESSED_START:
            if CROSSED:
                pipes.append(Pipe(TOP_PIPE, BOTTOM_PIPE, top_ycoord, bottom_ycoord))
                CROSSED = False
            if len(pipes) != 0:
                if pipes[len(pipes) - 1].x_pos <= SPAWN:
                    CROSSED = True
                if pipes[0].x_pos <= -75:
                    del pipes[0]
            for pipe in pipes:
                if bird.running:
                    pipe.update()
                pipe.render(display)
            if bird.img_loc[1] >= HEIGHT / 5 or bird.img_loc[1] <= -15:
                bird.running = False
            for pipe in pipes:
                if pipe.x_pos == 100:
                    counter = counter + 1
        if not bird.running:
            for pipe in pipes:
                pipe.render(display)

        if not START_BUTTON.action or not bird.running:
            if not START_BUTTON.action:
                PRESSED_START = START_BUTTON.draw(display)
                if EXIT_BUTTON.draw(display):
                    pygame.quit()
                    sys.exit()
            else:
                PRESSED_START = PLAY_AGAIN_BUTTON.draw(display)
                if EXIT_BUTTON.draw(display):
                    pygame.quit()
                    sys.exit()
                if MAIN_MENU_BUTTON.draw(display):
                    counter = 0
                    pipes.clear()
                    CROSSED = True
                    bird = BirdPhysics(BIRD, BIRD_SPAWN, SPEED, pipes, RUNNING)
                    PRESSED_START = False
                    START_BUTTON.action = False
                    MAIN_MENU_BUTTON.action = False
                    HIGH_SCORE = False
                with open('score.txt', 'r+') as file:
                    SCORE = file.readline()
                    file.seek(0)
                    file.write(str(max(int(SCORE), counter)))

                if int(SCORE) < counter or HIGH_SCORE:
                    SCORE = "New High Score!"
                    HIGH_SCORE = True
                else:
                    if not HIGH_SCORE:
                        SCORE = "High Score: " + SCORE

                score_message_img = score_message_font.render(str(SCORE), True, white)
                display.blit(score_message_img, (80, 10))

        if PLAY_AGAIN_BUTTON.action:
            counter = 0
            pipes.clear()
            CROSSED = True
            bird = BirdPhysics(BIRD, BIRD_SPAWN, SPEED, pipes, RUNNING)
            PLAY_AGAIN_BUTTON.action = False
            HIGH_SCORE = False

        """if PAUSE_BUTTON.draw(display):
            bird.running = False
            PAUSE_BUTTON.action = False
            if not PAUSE_BUTTON.action:
                bird.running = True"""

        display.blit(score_img, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.velocity = -2.5

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(60)


main()
