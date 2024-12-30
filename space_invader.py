import pygame
import sys
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 4
ENEMY_DROP = 40
NUM_OF_ENEMIES = 6

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Background image
background_img = pygame.image.load('background.png')

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load('arcade_space.png')
player_x, player_y = 370, 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
for i in range(NUM_OF_ENEMIES):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(ENEMY_SPEED)
    enemy_y_change.append(ENEMY_DROP)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x, bullet_y = 0, 480
bullet_x_change = 0
bullet_y_change = BULLET_SPEED
bullet_state = "rest"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x, text_y = 10, 10

# Game Over
over_font = pygame.font.Font("freesansbold.ttf", 64)

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    screen.blit(bullet_img, (x + 16, y))
    bullet_state = "fire"

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (200, 250))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

running = True
while running:

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE and bullet_state == "rest":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
                bullet_sound = mixer.Sound("laser.wav")
                bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= SCREEN_WIDTH - 64:
        player_x = SCREEN_WIDTH - 64

    # Enemy movement
    for i in range(NUM_OF_ENEMIES):
        if enemy_y[i] >= 450 and abs(player_x - enemy_x[i]) < 80:
            for j in range(NUM_OF_ENEMIES):
                enemy_y[j] = 2000
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            game_over_text()
            running = False

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = ENEMY_SPEED
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= SCREEN_WIDTH - 64:
            enemy_x_change[i] = -ENEMY_SPEED
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "rest"
            score_value += 1
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "rest"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
