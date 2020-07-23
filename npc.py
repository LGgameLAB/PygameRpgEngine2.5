import pygame

import animations as anims
import settings as stgs

import random

class npc:
    def __init__(self, name, stats, moveType, interactionType, imgsheet, x, y, w, h):
        self.name = name
        self.stats = stats
        self.moveType = moveType
        self.interactionType = interactionType
        self.imgsheet = imgsheet
        self.dir = 'r'
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.framed = True
        self.setAnimations = anims.animation(self.imgsheet, self.dir, 0.2)
        self.setAnimation()
        self.ticker1 = stgs.ticker(5)
        self.dirs = ['u', 'd', 'l', 'r']

        self.clock = 0
    def update(self):

        self.clock += 1


        if self.ticker1.done:
            self.setAnimations.update(True, self.dir)

        self.setAnimation()

        self.ticker1.tick()

        if self.interactionType == 1:
            pass
        if self.interactionType == 2:
            pass

        if self.moveType == 1:
            if self.clock > 200:
                self.clock = 0
                self.move()

        if self.moveType == 0:
            pass

    def move(self):
        self.newDirs = []
        for val in self.dirs:
            if val != self.dir:
                self.newDirs.append(val)

        self.dir = self.newDirs[random.randint(0, 2)]



    def setAnimation(self):
        self.image = self.setAnimations.GetImg()
        self.frame = self.setAnimations.GetFrame()


def goblin():
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', {'str': 11, 'dex': 12, 'wis': 9}, 1, 2, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'fullArt': gobSamp}, 64*9, 64*10, 64, 64)

# class enemy:
#      def __init__(self, name):
#             self.name = name
#
# def goblin():
#   return enemy('goblin')
#
# gob1 = goblin()
#
