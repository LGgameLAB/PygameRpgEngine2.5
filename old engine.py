import pygame
import sys
import random
from settings import *


class player:
    
    def __init__(self, startX, startY, image, vel):
        self.image = image
        self.x = startX - (self.image.get_width()/2)
        self.y = startY - (self.image.get_height()/2)
        self.startX = startX  - (self.image.get_width()/2)
        self.startY = startY  - (self.image.get_height()/2)
        self.rect = (self.image.get_width(), self.image.get_height(), self.x, self.y)
        self.vel = vel
        self.lockX = True
        self.lockY = True

    def showRect(self):
        return self.rect


    def showPos(self, place):
        if place == False:
            return self.x, self.y
        elif place == "center":
            return self.x + (self.image.get_width()/2), self.y + (self.image.get_height()/2)

    def center(self, location):
        if location == "x":
            self.x = self.startX
        elif location == "y":
            self.y = self.startY
        else:
            self.x = self.startX
            self.y = self.startY
    
    #def move(self):
    #    keys = pygame.key.get_pressed()
    #    if not self.lockY:
    #        if keys[pygame.K_UP]:
    #            self.y -= self.vel
    #        if keys[pygame.K_DOWN]:
    #            self.y += self.vel
    #    if not self.lockX:
    #        if keys[pygame.K_RIGHT]:
    #            self.x += self.vel
    #        if keys[pygame.K_LEFT]:
    #            self.x -= self.vel
    

class room:
    
    def __init__(self, startX, startY, image, vel):
        self.x = startX
        self.y = startY
        self.image = image
        self.rect = (self.image.get_width(), self.image.get_height(), self.x, self.y)
        self.velX = 0
        self.velY = 0
        self.vel = vel
        
    def showRect(self):
        return self.rect

    def showPos(self, place):
        if place == False:
            return self.x, self.y
        elif place == "center":
            return self.x + (self.image.get_width()/2), self.y + (self.image.get_height()/2)
        
    def move(self, halt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.velY = -self.vel 
        elif keys[pygame.K_DOWN]:
            self.velY = self.vel
        else:
            self.velY = 0
        
        if keys[pygame.K_RIGHT]:
            self.velX = self.vel
        elif keys[pygame.K_LEFT]:
            self.velY = -self.vel
        else:
            self.velX = 0 
        
class cam:

    def __init__(self, window, player):
        self.win = window
        self.player = player
        self.objects = []
        self.room = False
        self.background = ((0, 1, 0))
        
    def loadRoom(self, room):
        self.room = room
        

    def checkMoveMap(self):
        self.room.move(False)

    def drawScreen(self):
        roomX = self.room.x
        roomY = self.room.y
        win.blit(self.room.image, (roomX, roomY))
        playerX = self.player.x
        playerY = self.player.y
        win.blit(self.player.image, (playerX, playerY))

    def reset(self):
        self.win.fill(self.background)
        
def mainloop(regulator, delay, player, cam, gameMap):
    pygame.init()

    pygame.display.set_caption(winTitle)
    

    

    run = regulator
    while run:
        #Room reset
        cam.reset()
        pygame.time.delay(delay)
        
        #Window exit checker
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        cam.drawScreen()
        cam.checkMoveMap()
        #cam.edgeCheckCollide(win.get_width(), win.get_height())
        #p1.move()
        #Updates window
        pygame.display.update()

     
    pygame.quit()

dudeImage = pygame.image.load('r.png')
roomImage = pygame.image.load('room2.png')    
winXCenter = winWidth/2
winYCenter = winHeight/2
win = pygame.display.set_mode((winWidth, winHeight))
p1 = player(winXCenter, winYCenter, dudeImage, 10)
room1 = room(0, 0, roomImage, 10)
map1 = [room1]
cam1 = cam(win, p1)
cam1.loadRoom(map1[0])
mainloop(True, 0, p1, cam1, map1)

sys.exit() 
