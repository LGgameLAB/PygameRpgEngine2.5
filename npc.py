import random

import pygame

import animations as anims
import optionBox as opBox
import settings as stgs


class dialogue:
    def __init__(self, text):
        self.image = pygame.image.load(stgs.dialogueBox1)
        self.rect = pygame.Rect(0, stgs.winHeight - self.image.get_height(), self.image.get_height(), self.image.get_width())
        self.active = False

        self.id = "dialogue"

        self.strText = text
        self.font = stgs.font1
        self.text = self.font.render(self.strText, True , stgs.white)

        self.typed = False

        self.startBuffer = stgs.ticker(20)
        self.startBuffer.lock = True


    def update(self):
        if self.active:
            self.startBuffer.tick()
            if not self.typed:
                self.image.blit(self.text, (50, 30))
                self.typed = True

            if self.startBuffer.done:
                keys = pygame.key.get_pressed()
                if keys[stgs.globalBtnSet['interactionBtn']]:
                    self.active = False
                    self.startBuffer.reset()

                

class npc:
    def __init__(self, name, stats, moveType, interactionType, imgSheet, x, y, w, h, text):
        self.name = name
        self.stats = stats
        self.moveType = moveType
        self.interactionType = interactionType
        self.imgSheet = imgSheet
        self.dir = 'r'
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fullArt = imgSheet["fullArt"]
        self.fightRect = pygame.Rect(800, 320, self.fullArt.get_width(), self.fullArt.get_height())
        self.framed = True
        self.setAnimations = anims.animation(self.imgSheet, self.dir, 0.2, self.imgSheet['startFrame'])
        self.setAnimation()
        self.ticker1 = stgs.ticker(5)
        self.dirs = ['u', 'd', 'l', 'r']
        self.moving = False
        self.vel = 1
        self.dist = 0

        self.text = text #"Watcha bee doin' ouwt by yershelf?!"
        self.dialogueBox = dialogue(self.text)
        self.interTick = stgs.ticker(8)
        self.clock = 0
        self.optionBox = opBox.optionBox('yes', 'no', 'what', 'why')
        self.optionTick = stgs.ticker(10)

        self.fightActive = False
        self.id = "battleSprite"

    def update(self, walls, pRect, pause):
        if pause:
            self.dialogueBox.update()
            self.optionBox.update()
        else:
            self.clock += 1

            if self.ticker1.done:
                self.setAnimations.update(self.moving, self.dir)

            self.setAnimation()

            self.ticker1.tick()
            self.interTick.tick()
            self.optionTick.tick()

            if self.interactionType == 1:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.interTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.dialogueBox.active = True

            if self.interactionType == 2:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.interTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.fightActive = True
                pass

            if self.interactionType == 3:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.optionTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.optionBox.active = True
                            

            if self.moveType == 1:
                if self.clock > 200:
                    self.clock = 0
                    self.changeDir()

            if self.moveType == 0:
                pass
            
            pRect = [pRect]
            self.move(walls + pRect)

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







#Talking goblin
def goblin(x, y, text):
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', {'str': 11, 'dex': 12, 'wis': 9}, 1, 1, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, text)

#Fighting goblin
def goblin2(x, y):
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', {'str': 11, 'dex': 12, 'wis': 9}, 1, 3, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, '')


# class enemy:
#      def __init__(self, name):
#             self.name = name
#
# def goblin():
#   return enemy('goblin')
#
# gob1 = goblin()
#
