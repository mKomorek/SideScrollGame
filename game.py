import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()
clock = pygame.time.Clock()

W, H = 1200, 500
gameWindow = pygame.display.set_mode((W,H))
pygame.display.set_caption('Game')

bg = pygame.image.load(os.path.join('images','bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()


"""
Player class
"""
class Player(object):
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, gameWindow):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            pygame.draw.rect(gameWindow, (0, 0, 0), (self.x, self.y, self.width, self.height))
            self.jumpCount += 1
            if self.jumpCount > 138:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitBox = (self.x, self.y, self.width, self.height)

        elif self.sliding or self.slideUp:
            if self.slideCount == 80:
                self.sliding = False
                self.slideUp = True
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            pygame.draw.rect(gameWindow, (0, 0, 0), (self.x, self.y+45, self.height, self.width))
            self.slideCount += 1
            self.hitBox = (self.x, self.y+45, self.height, self.width)
            
        else:
            if self.runCount > 42:
                self.runCount = 0
            pygame.draw.rect(gameWindow, (0, 0, 0), (self.x, self.y, self.width, self.height))
            self.runCount += 1
            self.hitBox = (self.x, self.y, self.width, self.height)

"""
Obstacle class
"""
class Obstacle(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitBox = (x, y, width, height)
        self.count = 0

    def draw(self, gameWindow):
        self.hitBox = (self.x, self.y, self.width, self.height)
        if self.count >= 8:
            self.count = 0
        self.count += 1
        pygame.draw.rect(gameWindow, (255,255,255), self.hitBox)

    def collide(self, colideObject):
        if self.hitBox[1] < 300:
            if colideObject[0] + colideObject[2] > self.hitBox[0] and colideObject[0] < self.hitBox[0] + self.hitBox[2]:
                if colideObject[1] < self.hitBox[1] + self.hitBox[3]:
                    return True
        else:
            if colideObject[0] + colideObject[2] > self.hitBox[0] and colideObject[0] < self.hitBox[0] + self.hitBox[2]:
                if colideObject[1] + colideObject[3] > self.hitBox[1]:
                    return True
        return False

"""
Necessary functions
"""
def redrawWindow():
    gameWindow.blit(bg, (bgX,0))
    gameWindow.blit(bg, (bgX2,0))
    user.draw(gameWindow)
    for element in objects:
        element.draw(gameWindow)

    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Score: ' + str(score), 1, (255,255,255))
    gameWindow.blit(text, (1100,10))
    pygame.display.update()

def saveScore():
    f = open('scores.txt', 'r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        return score

    return last

def gameOver():
    global score, speed, objects
    speed = 100
    objects = []

    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        largeFont = pygame.font.SysFont('comicsans', 96)
        lastScore = largeFont.render('Best Score: ' + str(saveScore()),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        gameWindow.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        gameWindow.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()

    score = 0
    

"""
Main part of script
"""
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(1500,3000))
speed = 100
user = Player(200,300,45,90)
objects = []
score = 0

redrawWindow()

while True:
    run = False
    largeFont = pygame.font.SysFont('comicsans', 96)
    startButton = largeFont.render('START', 1, (255,255,255))
    gameWindow.blit(startButton, (W/2 - startButton.get_width()/2,150))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = True

    while run:
        redrawWindow()
        score = speed // 10 - 10

        for element in objects:
            if element.collide(user.hitBox):
                gameOver()
            element.x -= 1.5
            if element.x < element.width * -1:
                objects.pop(objects.index(element))

        bgX -= 1.5
        bgX2 -= 1.5 
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == USEREVENT+1:
                speed += 2
            if event.type == USEREVENT+2:
                r = random.randrange(0,2)
                if r == 0:
                    objects.append(Obstacle(1110,345,30,45))
                else:
                    objects.append(Obstacle(1110,270,45,45))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not(user.jumping):
                user.jumping = True

        if keys[pygame.K_DOWN]:
            if not(user.sliding):
                user.sliding = True

        clock.tick(speed)
