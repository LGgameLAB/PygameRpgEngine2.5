import pygame

import settings

class subMenu:
    def __init__(self, dictData, dictKey):
        self.active = False
        self.dictData = dictData
        self.dictKey = dictKey
        self.options = optionBox(self.dictData)
        self.sprites = [self.options]
        self.status = 'off'
        
    def update(self):
        if self.active:
            self.options.update()
            self.sprites = [self.options]
            if self.options.subMenu:
                for menu in self.options.subMenus:
                    if menu.active:
                        for sprite in menu.sprites:
                            self.sprites.append(sprite)
            if self.options.status == 'done':
                self.status = self.options.status
                self.result = self.options.result
            else:
                self.status = 'pending'


class optionBox:
    def __init__(self, data):
        self.subMenu = False
        self.subMenus = []
        self.subMenuActive = False
        if data != False:
            if isinstance(data, dict):

                self.dataType = 'd'
                self.args = list(data.keys())
                self.dictData = data
                for k in self.args:
                    if isinstance(self.dictData[k], dict):
                        self.subMenu = True
                        self.subMenus.append(subMenu(self.dictData[k], k))

            elif isinstance(data, list):
                self.dataType = 'l'
                self.args = data

        else:
            self.args = ['yes', 'no']

        self.active = False
        
        self.index = 0
        self.delay = settings.ticker(10)
        self.delay.lock = True
        self.delay.done = False
        self.id = "optionBox"

        self.font = settings.font1

        self.startX = 0
        self.startY = 0
        self.getWidth()
        self.height = (self.font.size('h')[1] + 12)*len(self.args) + 24

        self.rect = pygame.Rect(self.startX, self.startY, self.width, self.height)
       

        self.setImage()

        self.status = 'off'

    def setImage(self):
        self.image = pygame.image.load(settings.optionBox1)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.convert()

    def update(self):
        if self.subMenuActive:
            self.subMenusUpdate()

        else:

            self.status = 'pending'
            self.render()

            self.delay.tick()

            if self.delay.done:
                keys = pygame.key.get_pressed()
                if keys[settings.globalBtnSet['scrollUpBtn']]:
                    self.delay.reset()
                    self.index -= 1
                    if self.index < 0:
                        self.index = int(len(self.args) - 1)
                elif keys[settings.globalBtnSet['scrollDownBtn']]:
                    self.delay.reset()
                    self.index += 1
                    if self.index > int(len(self.args) - 1):
                        self.index = 0


                if keys[settings.globalBtnSet['menusBtn']]:
                    if self.dataType == 'd':
                        if self.subMenu:
                            for menu in self.subMenus:
                                if menu.dictKey == self.args[self.index]:
                                    self.subMenuActive = True
                                    menu.active = True

                            if self.subMenuActive == False:
                                self.status = 'done'
                                self.result = self.dictData[self.args[self.index]]
                                self.active = False
                        else:
                            self.status = 'done'
                            self.result = self.dictData[self.args[self.index]]
                            self.active = False

                        #print(self.result)
                    else:
                        self.active = False
                        self.result = self.index
                        self.status = 'done'
                    self.delay.reset()
                
                if keys[settings.globalBtnSet['menusBack']]:
                    self.active = False
                    self.result = False
                    self.status = 'done'
    
    def render(self):
        self.setImage()

        z = 0
        y = 4*len(self.args) + 8

        for arg in self.args:
            
            text = self.font.render(arg, True, settings.white)
            self.image.blit(text, (int((self.width/24)*5), y))
            if z == self.index:
                pygame.draw.circle(self.image, settings.white, (int((self.width/24)*5 - 8), y + 12), 4)
            
            z += 1
            y += 24
    
    def reset(self):
        self.status = 'off'
        
    def subMenusUpdate(self):

        for menu in self.subMenus:
            menu.update()
            
            if menu.status == 'done':
                if menu.result == False:
                    self.subMenuActive = False
                    menu.active = False
                    menu.status = 'off'
                else:
                    self.subMenuActive = False
                    menu.active = False
                    menu.status = 'off'
                    self.status = 'done'
                    self.result = menu.result
                    self.active = False
                    print(self.result)

    def returnMenu(self):
        for menu in self.subMenus:
            if menu.active:
                return menu.sprites

    def getWidth(self):
        charCount = 0
        for arg in self.args:
            if len(arg) > charCount:
                charCount = max(charCount, len(arg))
        
        self.width = 24*(charCount + 1)
    
    def setPos(self, pos):
        if pos == 'bottomR':
            self.startX = settings.winWidth - self.width
            self.startY = settings.winHeight - self.height
            
            self.rect = pygame.Rect(self.startX, self.startY, self.width, self.height)