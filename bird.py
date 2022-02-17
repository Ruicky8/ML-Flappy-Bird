import pygame

bird1_img = pygame.image.load("imgs/bird1.png")
bird2_img = pygame.image.load("imgs/bird2.png")
bird3_img = pygame.image.load("imgs/bird3.png")

BIRD_IMG = [bird1_img, bird2_img, bird3_img]

class Bird():

    def __init__(self, screen, x, y):
        self.screen = screen

        self.img = BIRD_IMG[0]
        self.img_time = 0
        self.tilt = 0

        self.height = 0
        self.y = y
        self.gravity = 3
        self.vely = 0

        self.x = x
        self.time = 0
        

    def flap(self):
        if self.img_time == 0:
            self.img = BIRD_IMG[0]
        elif self.img_time == 4:
            self.img = BIRD_IMG[1]
        elif self.img_time == 8:
            self.img = BIRD_IMG[2]
        elif self.img_time == 12:
            self.img = BIRD_IMG[1]
        elif self.img_time == 15:
            self.img = BIRD_IMG[0]
            self.img_time = -1
        self.img_time += 1

    def move(self):
        d = self.vely*self.time + 0.47*self.gravity*self.time**2
        if d > 15:
            d = 15
        elif d < 0:
            d -= 2
        
        if d < 0:
            self.tilt = 25
        elif d > 0 and self.tilt > -80:
            self.tilt -= 7

        self.y += d
        self.time += 1

    def jump(self):
        self.vely = -9
        self.time = 1

    def draw(self):
        self.flap()
        
        rotated_img = pygame.transform.rotate(self.img, self.tilt)
        rect = rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        self.screen.blit(rotated_img, rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)