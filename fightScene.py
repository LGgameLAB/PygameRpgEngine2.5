import pygame

import settings

class fightScene:

    def __init__(self, side1, side2):
        self.clock = 0
        self.image = pygame.image.load(settings.fightSceneOverlay1)
        self.rect = (0, 0, self.image.get_width(), self.image.get_height())
        self.sprites1 = side1
        self.sprites2 = side2

        self.turn = 1

    def run(self):
        pass

        
