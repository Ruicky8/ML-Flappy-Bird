import pygame
import random

PIPE_IMG = pygame.image.load("imgs/pipe.png")

class Pipe():

    def __init__(self, screen, x):
        self.screen = screen
        
        self.x = x
        self.velx = -7
        
        self.gap = 140
        self.height = random.randint(175, 337)
        self.bottom = self.height - self.gap
        
        self.passed = False

        self.l_pipe_img = PIPE_IMG
        self.u_pipe_img = pygame.transform.flip(PIPE_IMG, False, True)

    def move(self):
        self.x += self.velx
    
    def draw(self):
        self.screen.blit(self.l_pipe_img, (self.x, self.height))
        self.screen.blit(self.u_pipe_img, (self.x, (self.height - self.gap) - 320))
    
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.u_pipe_img)
        bottom_mask = pygame.mask.from_surface(self.l_pipe_img)

        top_offset = (self.x - bird.x, (self.height - self.gap) - 320 - round(bird.y))
        bottom_offset = (self.x - bird.x, self.height - round(bird.y))

        t_collide = bird_mask.overlap(top_mask, top_offset)
        b_collide = bird_mask.overlap(bottom_mask, bottom_offset)

        if t_collide or b_collide:
            return True
        return False

    