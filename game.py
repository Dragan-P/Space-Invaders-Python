import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# create the screen. 800 is width, 600 is height
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("space.jpg")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # -1 makes it play on loop without ending

# Title and Icon
pygame.display.set_caption("Space Invaders")  # 32pixels of icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)  # variable name of icon, from the spaceship.png

# Player
playerIMG = pygame.image.load("spaceship.png")
playerX = 370  # x,y coordinates for the spaceship on screen
playerY = 480
playerX_change = 0

# Enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load("alien.png"))  # append adds an element to a list
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

# Bullet

# Ready - You cannot see the bullet on the screen
# Fire - The bullet is currently moving
bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.7  # Speed of bullet
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)  # text type and size

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)  # text type and size


def show_score(x, y):
    score = font.render("score :" + str(score_value), True,
                        (255, 255, 255))  # we type caste(convert) the score_value to a string.
    # The last numbers are the RGB values for the color
    screen.blit(score, (x, y))


def game_over_text(x, y):
    over_text = over_font.render("GAME OVER :" + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerIMG, (x, y))  # blit = drawing image of playerIMG on the screen


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # We make the variable global accessible
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 1, y + 10))  # bullet goes from the middle of the ship


# Mathematical equation for the collision detection
def isCollision(enemyX, enemyY, bulletX,
                bulletY):  # sgrt is the square root. math.pow() returns the value of x raised to power y.
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    # put everything after screen.fill so it will appear on the screen, otherwise it will appear before the screen
    # any key pressed is an event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX  # if bullet_state is "ready":
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries of spaceship so it does not go out of the screen.
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # updating display
