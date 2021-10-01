import pygame
#from pygame.locals import *
#import sys
#import os
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))
background=pygame.image.load('bg.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)
pygame.display.set_caption('Jargu')
icon= pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerimg= pygame.image.load('hero.png')
playerX=375
playerY=536
playerX_change=0
#enemy code:
enemyimg=[]
enemyX=[]
enemyY=[]
enemyY_change=[]
enemyX_change=[]
num_of_enem= 6
for i in range(num_of_enem):
    enemyimg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(4)
    enemyY_change.append(40)
#bullet
bulletimg= pygame.image.load('fire.png')
bulletX=0
bulletY=536
bulletX_change=0
bulletY_change=10
bullet_state="ready"
#score
score_value=0
font=pygame.font.Font('aAdistro.ttf',70)
textX=10
textY=10
over_font= pygame.font.Font('aAdistro.ttf',70)
def show_score(x,y):
    score=font.render("score:"+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text=over_font.render("Game Over",True,(255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))

def isc(enemyX,enemyY,bulletX,bulletY):
    dist=(math.sqrt(math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if dist<30:
        return True
    else:
        return False


running=True
#game loop
while running:
    #screen.fill((25,2,25))
    screen.blit(background,(0,0))
   # playerX-=0.3
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type== pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change= -5
            if event.key==pygame.K_RIGHT:
              playerX_change=5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletsound= mixer.Sound("laser.wav")
                    bulletsound.play()
                    #
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
#
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or  event.key==pygame.K_RIGHT:
                   playerX_change=0
#player seting
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerY>=736:
        playerY=736
    #loop
    for i in range(num_of_enem):
        if enemyY[i] > 440:
            for j in range(num_of_enem):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i]=0.9
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i] >= 736:
              enemyX_change[i] =-0.9
              enemyY[i]+=enemyY_change[i]

        collision = isc(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exp_sound = mixer.Sound('explosion.wav')
            exp_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY<=0:
        bulletY=536
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(playerX,bulletY)
        bulletY-=bulletY_change

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()
