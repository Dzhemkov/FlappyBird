import pygame


class Pipe:
    def __init__(self, top_img, bottom_img, top_ycoord, bottom_ycoord):
        self.top_img = top_img
        self.bottom_img = bottom_img
        self.top_ycoord = top_ycoord
        self.bottom_ycoord = bottom_ycoord
        self.speed = -1
        self.x_pos = 300

    def top_pipe_rect(self):
        return pygame.Rect(self.x_pos, self.top_ycoord, 32, 118)

    def bottom_pipe_rect(self):
        return pygame.Rect(self.x_pos, self.bottom_ycoord, 32, 128)

    def update(self):
        self.x_pos += self.speed

    def render(self, surface):
        surface.blit(self.top_img, (self.x_pos, self.top_ycoord))
        surface.blit(self.bottom_img, (self.x_pos, self.bottom_ycoord))
