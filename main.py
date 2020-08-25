import pygame
import random
import math
from pygame import mixer

# initialise pygame
pygame.init()

# Create the screen 800 width and 600 height
screen = pygame.display.set_mode((800, 600))

# title and Icon
pygame.display.set_caption("Space Invaders")
myicon = pygame.image.load("ufo.png")
pygame.display.set_icon(myicon)

# BACKGROUND
background = pygame.image.load("background.png")

# Player
playerimg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

n = 2
enemyimg1 = []
enemyX1 = []
enemyY1 = []
enemyX1_change = []

enemyimg2 = []
enemyX2 = []
enemyY2 = []
enemyX2_change = []

enemyimg3 = []
enemyX3 = []
enemyY3 = []
enemyX3_change = []

for i in range(n):
    # Enemy Type 1
    enemyimg1.append(pygame.image.load("monster.png"))
    enemyX1.append(random.randint(0, 730))
    enemyY1.append(random.randint(30, 280))
    enemyX1_change.append(i + 2)

    # Enemy Type 2
    enemyimg2.append(pygame.image.load("monster1.png"))
    enemyX2.append(random.randint(0, 730))
    enemyY2.append(random.randint(30, 150))
    enemyX2_change.append(i + 2.5)

    # Enemy Type 3
    enemyimg3.append(pygame.image.load("alien.png"))
    enemyX3.append(random.randint(0, 730))
    enemyY3.append(random.randint(40, 280))
    enemyX3_change.append(i + 3)

# Bullet
bullet = pygame.image.load("bullet.png")
bulletX = 370
bulletY = 480
bulletX_change = 0
bulletY_change = 14
bullet_state = "ready"

# score
scoreval = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 20
textY = 20

GOfont = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    for j in range(n):
        enemyY1[j] = 2000
        enemyY2[j] = 2000
        enemyY3[j] = 2000

    OT = GOfont.render("GAME OVER", True, (255, 0, 0))
    screen.blit(OT, (200, 250))


def showscore(x, y):
    score = font.render("Score: " + str(scoreval), True, (255, 255, 255))
    screen.blit(score, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def player(x, y):
    # blit means to draw on screen(game surface)
    screen.blit(playerimg, (x, y))


def enemy(img, x, y):
    # blit means to draw on screen(game surface)
    screen.blit(img, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))
    if dist < 27:
        exp_sound = mixer.Sound('explosion.wav')
        exp_sound.play()
        return True
    else:
        return False


# To play a background music continuously
# mixer.music.load('background.wav')
# mixer.music.play(-1)


running = True
# Game loop
while running:

    # screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check if keystroke is pressed
        if event.type == pygame.KEYDOWN:

            # check if the keystroke is left arrow key
            if event.key == pygame.K_LEFT:
                playerX_change = -3

            # check if the keystroke is right arrow key
            if event.key == pygame.K_RIGHT:
                playerX_change = 3

            if event.key == pygame.K_SPACE:
                if (bullet_state == "ready"):
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_state = "fire"
                    bulletX = playerX

            if event.key == pygame.K_ESCAPE:
                game_over_text()

        if event.type == pygame.KEYUP:

            if (event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                playerX_change = 0

    # draw player
    playerX += playerX_change
    if (playerX > 736 or playerX < 0):
        playerX_change = 0

    for i in range(n):

        if ((enemyY1[i] > 440) or (enemyY2[i] > 440) or (enemyY3[i] > 440)):
            game_over_text()
            break

        enemyX1[i] += enemyX1_change[i]
        if (enemyX1[i] > 736):
            enemyX1_change[i] = -1
            enemyY1[i] += 3
        if (enemyX1[i] < 0):
            enemyX1_change[i] = 1
            enemyY1[i] += 3

        enemyX2[i] += enemyX2_change[i]
        if (enemyX2[i] > 736):
            enemyX2_change[i] = -2
            enemyY2[i] += 3
        if (enemyX2[i] < 0):
            enemyX2_change[i] = 2
            enemyY2[i] += 3

        enemyX3[i] += enemyX3_change[i]
        if (enemyX3[i] > 736):
            enemyX3_change[i] = -2.5
            enemyY3[i] += 4
        if (enemyX3[i] < 0):
            enemyX3_change[i] = 2.5
            enemyY3[i] += 4

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
        bulletX = playerX

    for i in range(n):
        if (isCollision(enemyX1[i], enemyY1[i], bulletX, bulletY)):
            bullet_state = "ready"
            bulletY = 480
            bulletX = playerX
            scoreval += 1
            enemyX1[i] = random.randint(0, 736)
            enemyY1[i] = random.randint(200, 300)

        if (isCollision(enemyX2[i], enemyY2[i], bulletX, bulletY)):
            bullet_state = "ready"
            bulletY = 480
            bulletX = playerX
            scoreval += 1
            enemyX2[i] = random.randint(0, 736)
            enemyY2[i] = random.randint(200, 300)

        if (isCollision(enemyX3[i], enemyY3[i], bulletX, bulletY)):
            bullet_state = "ready"
            bulletY = 480
            bulletX = playerX
            scoreval += 1
            enemyX3[i] = random.randint(0, 736)
            enemyY3[i] = random.randint(200, 300)

    for i in range(n):
        enemy(enemyimg1[i], enemyX1[i], enemyY1[i])
        enemy(enemyimg2[i], enemyX2[i], enemyY2[i])
        enemy(enemyimg3[i], enemyX3[i], enemyY3[i])

    player(playerX, playerY)
    showscore(textX, textY)
    pygame.display.update()
