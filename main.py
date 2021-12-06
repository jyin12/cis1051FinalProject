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
        g.centerx -= 3  # gets the coordinate from gate list and move a little to the left (higher # = faster it moves)
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

def create_coin():
    random_coin_pos = random.choice(coin_height)
    bottom_coin = gate.get_rect(midtop=(950, random_coin_pos))  # coordinate is the middle of the screen on top
    top_coin = gate.get_rect(midbottom=(300, random_coin_pos - 600))  # Cannot delete, shows error for some reason (place the top coin off the screen)
    return bottom_coin, top_coin

def move_coins(coins):
    for c in coins:
        c.centerx -= 3  # gets the coordinate from gate list and move a little to the left
    return coins  # returns a new list

def draw_coins(coins):
    for c in coins:
        screen.blit(coin, c)

def check_collision_coin(coins):
    for c in coins:
        if c.colliderect(totoro_rect):
            coins.remove(c)
            return True
    return False

def rotate_totoro(totoro):
    new_totoro = pygame.transform.rotozoom(totoro, -totoro_movement * 3, 1)  # need to multiply by 2 b/c it gives the "turn" effects
    return new_totoro

def display_score(game_state):
    if game_state == 'game_start':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        hi_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        hi_score_rect = hi_score_surface.get_rect(center=(288, 600))
        screen.blit(hi_score_surface, hi_score_rect)

def score_update(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()
screen = pygame.display.set_mode((576, 780))  # will change screen size later
frames = pygame.time.Clock()
game_font = pygame.font.Font('magilio-font/MagilioRegular-Yzv2O.ttf',35)  # (fontStyle file, fontSize)

# Game variables
gravity = 0.25
totoro_movement = 0
game_active = True
score = 0
high_score = 0

# background image
background = pygame.image.load('images/bg-5.jpg').convert()
background = pygame.transform.scale(background, (576, 780))

# the moving floor
base = pygame.image.load("images/base-1.jfif").convert()
base = pygame.transform.scale(base, (576, 500))
base_x_pos = 0

# the "bird"
totoro = pygame.image.load('images/catbus.png').convert_alpha()  # convert_alpha() since it's for surfaces that have no transparency
totoro = pygame.transform.scale(totoro, (50, 70))
totoro_rect = totoro.get_rect(center=(100, 390))

# the torii gates as the pipes
gate = pygame.image.load('images/torii-gate.png').convert_alpha()
gate = pygame.transform.scale(gate, (150, 410))
gate_list = []  # continues to make the gates
SPAWNGATE = pygame.USEREVENT
pygame.time.set_timer(SPAWNGATE, 2000)  # when the first gate will show up (in ms)
gate_height = [380, 410, 450]

# Game over page
game_over = pygame.image.load('images/game-title-removebg-preview.png').convert_alpha()
game_over = pygame.transform.scale(game_over, (350, 80))
game_over_rect = game_over.get_rect(center=(288, 390))

# Coins
coin = pygame.image.load('images/goldCoin/goldCoin5.png').convert_alpha()
coin = pygame.transform.scale(coin, (50, 50))
coin_list = []
SPAWNCOIN = pygame.USEREVENT
pygame.time.set_timer(SPAWNCOIN, 2000)  # time (in ms) when the first coin comes out
coin_height = [150, 200, 250, 300, 350]

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
                coin_list.clear()
                totoro_rect.center = (100, 390)  # re-centers the bird
                totoro_movement = 0
                score = 0  # resets the score board everytime a new game starts

        if game.type == SPAWNGATE and game.type == SPAWNCOIN:
            gate_list.extend(create_gate())  # every 1.2s, it creates another gate and stores into create_gate list
            coin_list.extend(create_coin())

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

        # Coins
        coin_list = move_coins(coin_list)
        draw_coins(coin_list)
        if check_collision_coin(coin_list):
            score += 0.9
        else:
            score += 0.01

        display_score('game_start')

    else:
        screen.blit(game_over, game_over_rect)
        high_score = score_update(score, high_score)
        display_score('game_over')


    # The moving "Brick"
    base_x_pos -= 1  # moves the base to left (higher the number, moves faster)
    infinite_base()
    if base_x_pos <= -576:  # if the image is "ending", set the pos back to 0 again
        base_x_pos = 0

    pygame.display.update()
    frames.tick(115)  # 120 is the frame rate (lower frame rate = slower the game goes, may have to increase gravity)
