import pygame

import settings

class optionBox:
    def __init__(self, *args):
        if len(args)> 0:
            self.args = args

        else:
            self.args = ['yes', 'no']

        self.active = False

        self.index = 0
        self.delay = settings.ticker(8)
        self.delay.lock = True
        self.delay.done = True
        self.id = "optionBox"

        self.startX = 0
        self.startY = 0
        self.width = 24*7
        self.height = 32*len(self.args) + 24

        self.rect = pygame.Rect(self.startX, self.startY, self.width, self.height)
        self.font = settings.font1

        self.setImage()

        self.status = 'off'

    def setImage(self):
        self.image = pygame.image.load(settings.optionBox1)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.convert()

    def update(self):
        self.status = 'pending'
        self.render()

        self.delay.tick()

        if self.delay.done:
            keys = pygame.key.get_pressed()
            if keys[settings.scrollUpBtn]:
                self.delay.reset()
                self.index -= 1
                if self.index < 0:
                    self.index = int(len(self.args) - 1)
            elif keys[settings.scrollDownBtn]:
                self.delay.reset()
                self.index += 1
                if self.index > int(len(self.args) - 1):
                    self.index = 0


            if keys[settings.menusBtn]:
                self.active = False
                self.status = 'done'
                self.result = self.index + 1
                self.delay.reset()
    
    def render(self):
        self.setImage()

        z = 0
        y = 4*len(self.args) + 8

        for arg in self.args:
            
            text = self.font.render(arg, True, settings.white)
            self.image.blit(text, (30, y))
            if z == self.index:
                pygame.draw.circle(self.image, settings.white, (24, y + 12), 4)
            
            z += 1
            y += 24
        
            
