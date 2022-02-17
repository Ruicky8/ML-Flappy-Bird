import pygame
from pygame.constants import K_UP
pygame.font.init()

import settings as st
from bird import Bird
from base import Base
from pipe import Pipe
from NN import *

BG_IMG = pygame.image.load("imgs/bg.png")
GEN = 0
FONT = pygame.font.SysFont("comicsans", 25)

def main(genomes, config):
    clk = pygame.time.Clock()
    keepRunning = True
    global GEN
    GEN += 1
    screen = pygame.display.set_mode((st.WIN_WIDTH,st.WIN_HEIGHT))
    
    birds = []
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(screen, 20, 200))
        g.fitness = 0
        ge.append(g)

    base = Base(screen)
    pipes = [Pipe(screen, 600), Pipe(screen, 800)]
    
    score = 0
    
    while keepRunning:
        screen.blit(BG_IMG, (0,0))
        clk.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepRunning = False
                pygame.quit()
                quit()
            """
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w
                    or event.key == pygame.K_UP):
                    for bird in birds:
                        bird.jump()
            """

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].u_pipe_img.get_width():
                pipe_ind = 1
        else:
            keepRunning = False
            break

        for i, bird in enumerate(birds):
            ge[i].fitness += 0.2

            output = nets[i].activate((
                bird.y, 
                abs(bird.y - pipes[pipe_ind].height), 
                abs(bird.y - pipes[pipe_ind].bottom))
            )
            if output[0] > 0.5:
                bird.jump()

        for bird in birds:
            bird.draw()
            bird.move()

        for pipe in pipes:
            pipe.draw()
            pipe.move()

        base.draw()
        base.move()

        text = FONT.render("Score: " + str(score), 1, (0,0,0))
        screen.blit(text, (st.WIN_WIDTH - 10 - text.get_width(), 10))
        text = FONT.render("Generation: " + str(GEN), 1, (0,0,0))
        screen.blit(text, (st.WIN_WIDTH - 10 - text.get_width(), 30))

        for i, bird in enumerate(birds):
            if bird.y >= 470 or bird.y < 0:
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)
            else:
                for pipe in pipes:
                    if pipe.collide(bird):
                        ge[i].fitness -= 1
                        birds.pop(i)
                        nets.pop(i)
                        ge.pop(i)
                    if bird.x > pipe.x and pipe.passed == False:
                        score += 1
                        for g in ge:
                            g.fitness += 10
                        pipe.passed = True

        for pipe in pipes:
            if pipe.x < -50:
                pipes.remove(pipe)
                pipes.append(Pipe(screen, 350))

        pygame.display.update()

if __name__ == "__main__":
    #main()
    config_path = get_config_path()
    run_neat(config_path)