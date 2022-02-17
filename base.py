import pygame

BASE_IMG = pygame.image.load("imgs/base.png")

class Base():

    def __init__(self, screen):
        self.img = BASE_IMG
        self.x1 = -10
        self.x2 = 325
        self.velx = -7
        self.y = 470
        self.screen = screen

    def move(self):
        self.x1 += self.velx
        self.x2 += self.velx
        if self.x1 < -340:
            self.x1 = 325
        elif self.x2 < -340:
            self.x2 = 325

    def draw(self):
        self.screen.blit(self.img, (self.x1, self.y))
        self.screen.blit(self.img, (self.x2, self.y))
