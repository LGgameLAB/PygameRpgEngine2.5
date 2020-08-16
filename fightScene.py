import pygame

import settings
import optionBox as opBox


class fightScene:

    def __init__(self, side1, side2):
        self.clock = 0
        self.image = pygame.image.load(settings.fightSceneOverlay1)
        self.rect = (0, 0, self.image.get_width(), self.image.get_height())
        self.sprites1 = [side1]
        self.sprites2 = [side2]

        self.side1Rect = pygame.Rect(0, 0, settings.winWidth/2, settings.winHeight)
        self.side2Rect = pygame.Rect(settings.winWidth/2, 0, settings.winWidth/2, settings.winHeight)

        self.turn = 0

    def update(self):
        self.image = pygame.image.load(settings.fightSceneOverlay1)

        for sprite in self.sprites1:
            self.image.blit(sprite.fullArt, (self.side1Rect.centerx - sprite.rect.width/2, self.side1Rect.centery - sprite.rect.height/2))

        for sprite in self.sprites2:
            self.image.blit(sprite.fullArt, (self.side2Rect.centerx - sprite.rect.width/2, self.side2Rect.centery - sprite.rect.height/2))


        if self.turn == 1:
            if self.options.status == 'off':
                self.giveOption()

            elif self.options.status == 'pending':
                pass

            elif self.options.status == 'done':
                pass
    
    def giveOption(self):
        self.options = opBox.optionBox(settings.fightOptions)
        
