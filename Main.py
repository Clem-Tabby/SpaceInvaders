import pygame
from pygame import mixer

import random

import math

pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('graphics/background.jpg')

# Background sound
mixer.music.load('sounds/background.wav')
mixer.music.play(-1)

# Lose sounds
num_lose_sounds = 9
for i in range(num_lose_sounds):
    lose_sounds = ['sounds/lose'+str(i + 1)]

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('graphics/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('graphics/spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('graphics/alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('graphics/blast.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"

# Initialize score
score_value = 0
score_font = pygame.font.Font('fonts/Friedrich.ttf', 32)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('fonts/Friedrich.ttf', 64)


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 18, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) +
                         math.pow(enemyY-bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
game_over = False
while running:

    # RGB for screen fill
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if event.key == pygame.K_RIGHT:
                playerX_change = 1
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(playerX, bulletY)
                blast_Sound = mixer.Sound('sounds/laser.wav')
                blast_Sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    playerX_change = 1
                else:
                    playerX_change = 0
            if event.key == pygame.K_RIGHT:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    playerX_change = -1
                else:
                    playerX_change = 0

    # Checking for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 350:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            if not game_over:
                lose_num = random.randint(1, 9)
                lose_sound = mixer.Sound('sounds/lose' + str(lose_num) + '.wav')
                lose_sound.play()
            game_over = True
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5 + score_value/7 * 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5 - score_value/7 * 0.1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('sounds/explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # Blast movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
