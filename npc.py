import pygame

import animations as anims
import settings as stgs

import random


class npc:
    def __init__(self, name, stats, moveType, interactionType, imgSheet, x, y, w, h):
        self.name = name
        self.stats = stats
        self.moveType = moveType
        self.interactionType = interactionType
        self.imgSheet = imgSheet
        self.dir = 'r'
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.framed = True
        self.setAnimations = anims.animation(self.imgSheet, self.dir, 0.2, self.imgSheet['startFrame'])
        self.setAnimation()
        self.ticker1 = stgs.ticker(5)
        self.dirs = ['u', 'd', 'l', 'r']
        self.moving = False
        self.vel = 1
        self.dist = 0

        self.clock = 0

    def update(self, walls):

        self.clock += 1

        if self.ticker1.done:
            self.setAnimations.update(self.moving, self.dir)

        self.setAnimation()

        self.ticker1.tick()

        if self.interactionType == 1:
            pass
        if self.interactionType == 2:
            pass

        if self.moveType == 1:
            if self.clock > 200:
                self.clock = 0
                self.changeDir()

        if self.moveType == 0:
            pass

        self.move(walls)

    def changeDir(self):
        self.newDirs = []
        for val in self.dirs:
            if val != self.dir:
                self.newDirs.append(val)

        self.dir = self.newDirs[random.randint(0, 2)]
        if self.moveType == 1:
            self.moving = True
            self.dist = 64

    def move(self, walls):
        if self.moving:
            if self.dist < self.vel:
                self.moving = False
                self.dist = 0
            else:
                self.dist -= self.vel

                if self.dir == 'u':
                    self.y -= self.vel
                    self.checkCollide(walls)

                if self.dir == 'd':
                    self.y += self.vel
                    self.checkCollide(walls)
                if self.dir == 'l':
                    self.x -= self.vel
                    self.checkCollide(walls)
                if self.dir == 'r':
                    self.x += self.vel
                    self.checkCollide(walls)

                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def checkCollide(self, walls):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if wall.colliderect(self.rect):
                if self.dir == 'l':
                    self.x += self.vel
                elif self.dir == 'r':
                    self.x -= self.vel
                elif self.dir == 'u':
                    self.y += self.vel
                else:
                    self.y -= self.vel 
                self.changeDir()

    def setAnimation(self):
        self.image = self.setAnimations.GetImg()
        self.frame = self.setAnimations.GetFrame()


def goblin(x, y):
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', {'str': 11, 'dex': 12, 'wis': 9}, 1, 2, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize)

# class enemy:
#      def __init__(self, name):
#             self.name = name
#
# def goblin():
#   return enemy('goblin')
#
# gob1 = goblin()
#
