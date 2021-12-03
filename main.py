import random

import pygame
import sys


def infinite_base():
    screen.blit(base, (base_x_pos, 680))
    screen.blit(base, (base_x_pos + 576, 680))

def create_gate():
    random_gate_pos = random.choice(gate_height)
    bottom_gate = gate.get_rect(midtop=(700, random_gate_pos))  # coordinate is the middle of the screen on top
    top_gate = gate.get_rect(midbottom=(700, random_gate_pos - 300))
    return bottom_gate, top_gate

def move_gates(gates):
    for g in gates:
        g.centerx -= 5  # gets the coordinate from gate list and move a little to the left
    return gates  # returns a new list

def draw_gates(gates):
    for g in gates:
        if g.bottom >= 780:
            screen.blit(gate, g)
        else:
            upsidedown_gate = pygame.transform.flip(gate, False, True)
            screen.blit(upsidedown_gate, g)

def check_collision(gates):
    for g in gates:
        if totoro_rect.colliderect(g):
            return False
    if totoro_rect.top <= -100 or totoro_rect.bottom >= 680:
        return False
    return True

def rotate_totoro(totoro):
    new_totoro = pygame.transform.rotozoom(totoro, -totoro_movement * 3, 1)  # need to multiply by 2 b/c it gives the "turn" effects
    return new_totoro

pygame.init()
screen = pygame.display.set_mode((576, 780))  # will change screen size later
frames = pygame.time.Clock()

# Game variables
gravity = 0.25
totoro_movement = 0
game_active = True

# background image
background = pygame.image.load('images/bg-1.jpg').convert()
background = pygame.transform.scale(background, (576, 780))

# the moving floor
base = pygame.image.load("images/base-1.jfif").convert()
base = pygame.transform.scale(base, (576, 500))
base_x_pos = 0

# the "bird"
totoro = pygame.image.load('images/catbus.png')  # not convert() since it's for surfaces that have no transparency
totoro = pygame.transform.scale(totoro, (40, 60))
totoro_rect = totoro.get_rect(center=(100, 390))

# the torii gates as the pipes
gate = pygame.image.load('images/torii-gate.png').convert()
gate = pygame.transform.scale(gate, (150, 410))
gate_list = []  # continues to make the gates
SPAWNGATE = pygame.USEREVENT
pygame.time.set_timer(SPAWNGATE, 1200)
gate_height = [380, 410, 450]

while True:
    for game in pygame.event.get():
        if game.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game.type == pygame.KEYDOWN:
            if game.key == pygame.K_SPACE:
                totoro_movement = 0  # resets whatever is in the gravity and just apply the speed below
                totoro_movement -= 8

            if game.key == pygame.K_SPACE and game_active == False:
                game_active = True
                gate_list.clear()  # clears list so that gates don't appear in a bunch from previous game
                totoro_rect.center = (100, 390)  # re-centers the bird
                totoro_movement = 0

        if game.type == SPAWNGATE:
            gate_list.extend(create_gate())  # every 1.2s, it creates another gate and stores into create_gate list

    screen.blit(background, (0, 0))  # coordinate system: (from left, from top)

    if game_active:
        # Totoro
        totoro_movement += gravity # so the totoro can have the "jump" effect
        rotated_totoro = rotate_totoro(totoro)
        totoro_rect.centery += totoro_movement
        screen.blit(rotated_totoro, totoro_rect)
        game_active = check_collision(gate_list)

        # Gates
        gate_list = move_gates(gate_list)
        draw_gates(gate_list)

    # The moving "Brick"
    base_x_pos -= 1  # moves the base to left (higher the number, moves slower)
    infinite_base()
    if base_x_pos <= -576:  # if the image is "ending", set the pos back to 0 again
        base_x_pos = 0

    pygame.display.update()
    frames.tick(120)  # 120 is the frame rate
