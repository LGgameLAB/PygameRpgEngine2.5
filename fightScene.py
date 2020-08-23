import pygame

import settings
import optionBox as opBox

class healthBar:
    def __init__(self, entityStats, entityPos):
        self.total = entityStats.stats[settings.maxHpKey]
        self.current = entityStats.stats[settings.healthKey]
        self.pos = entityPos

    def update(self):
        pass

    def render(self):
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.total*2 + 4, 12)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))

class fightScene:

    def __init__(self, side1, side2):
        self.clock = 0
        self.image = pygame.image.load(settings.fightSceneOverlay1)
        self.rect = (0, 0, self.image.get_width(), self.image.get_height())
        self.sprites1 = [side1]
        self.sprites2 = [side2]

        self.player = self.sprites1[0]
        self.side1Rect = pygame.Rect(0, 0, settings.winWidth/2, settings.winHeight)
        self.side2Rect = pygame.Rect(settings.winWidth/2, 0, settings.winWidth/2, settings.winHeight)

        self.turn = 1
        self.stage = 1

        self.giveOption()

        self.delay = settings.ticker(20)
        self.delay.lock = True

    def update(self):
        self.image = pygame.image.load(settings.fightSceneOverlay1)

        for sprite in self.sprites1:
            self.image.blit(sprite.fullArt, (self.side1Rect.centerx - sprite.fullArt.get_width()/2, self.side1Rect.centery - sprite.fullArt.get_height()/2))

        for sprite in self.sprites2:
            self.image.blit(sprite.fullArt, (self.side2Rect.centerx - sprite.fullArt.get_width()/2, self.side2Rect.centery - sprite.fullArt.get_height()/2))

        
        self.delay.tick()

        if self.delay.done:
            if self.turn == 1:
                if self.options.status == 'pending':
                    pass

                elif self.options.status == 'done':
                    if self.options.result.id == "attack":
                        self.sprites2[0].stats.recvHit(self.options.result)

                    elif self.options.result.id == "run":
                        self.sprites2[0].fightActive = False

                    print(self.options.result)
                    self.turn += 2
                        

        self.options.update()

    def giveOption(self):
        fightSceneOptions = {}
        attackOptions = {}
        itemOptions = {}

        for item in self.player.stats.inventory.items:
            if item.id == "weapon":
                attackOptions[item.name] = item.attack
            else:
                itemOptions[item.name] = item.effect

        for option in settings.fightOptions:
            if option == "Attack":
                fightSceneOptions[option] = attackOptions
            
            elif option == "Items":
                fightSceneOptions[option] = itemOptions
            
            elif option == "Run":
                fightSceneOptions[option] = settings.run()
            else:
                fightSceneOptions[option] = '??'

        self.options = opBox.optionBox(fightSceneOptions)
    
        self.options.setPos('bottomR')
