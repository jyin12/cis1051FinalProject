import pygame
import sys

def infinite_base():
    screen.blit(base, (base_x_pos, 680))
    screen.blit(base, (base_x_pos + 576, 680))

pygame.init()
screen = pygame.display.set_mode((576, 780))  # will change screen size later
frames = pygame.time.Clock()

background = pygame.image.load('images/bg-3.jpg').convert()
background = pygame.transform.scale(background, (576, 780))

base = pygame.image.load("images/base-1.jfif").convert()
base = pygame.transform.scale(base, (576, 500))
base_x_pos = 0

while True:
    for game in pygame.event.get():
        if game.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))  # coordinate system: (from left, from top)
    base_x_pos -= 1  # moves the base to left (higher the number, moves slower)
    infinite_base()
    if base_x_pos <= -576:  # if the image is "ending", set the pos back to 0 again
        base_x_pos = 0

    pygame.display.update()
    frames.tick(120)  # 120 is the frame rate
