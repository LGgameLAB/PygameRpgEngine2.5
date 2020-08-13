import pygame

import settings
import optionBox as opBox

knightStats = settings.stats(100, 2, 11)
print(knightStats.stats)

class fightScene:

    def __init__(self, side1, side2):
        self.clock = 0
        self.image = pygame.image.load(settings.fightSceneOverlay1)
        self.rect = (0, 0, self.image.get_width(), self.image.get_height())
        self.sprites1 = side1
        self.sprites2 = side2

        self.turn = 1

    def run(self):
        if self.turn == 1:
            if self.options.status == 'off':
                self.giveOption()

            elif self.options.status == 'pending':
                pass

            elif self.options.status == 'done':
                pass
    
    def giveOption(self):
        self.options = opBox.optionBox(settings.fightOptions)
        
