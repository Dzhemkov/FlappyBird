import sys
import pygame


class BirdPhysics:
    def __init__(self, img, img_loc, velocity, pipes, running):
        self.img = img
        self.img_loc = list(img_loc)
        self.velocity = velocity
        self.collisions = {'up': False, 'down': False, 'right': False}
        self.pipes = pipes
        self.running = running

    def bird_rect(self):
        return pygame.Rect(self.img_loc[0] + 2, self.img_loc[1], 12, 8)

    def update(self, movement=0):
        frame_movement = movement + self.velocity
        self.collisions = {'up': False, 'down': False, 'right': False}

        self.img_loc[1] += frame_movement

        pipe_rects = []
        for pipe in self.pipes:
            top_rect = pipe.top_pipe_rect()
            bottom_rect = pipe.bottom_pipe_rect()
            pipe_rects.append((bottom_rect, top_rect))

        bird_rect = self.bird_rect()
        for pipe_rect in pipe_rects:
            if bird_rect.colliderect(pipe_rect[0]) or bird_rect.colliderect(pipe_rect[1]):
                self.running = False

        self.velocity = min(5, self.velocity + .15)
        if self.collisions['down'] or self.collisions['up']:
            self.velocity = 0

    def render(self, surface):
        surface.blit(self.img, self.img_loc)
