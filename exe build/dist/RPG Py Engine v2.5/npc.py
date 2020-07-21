import pygame

class npc:
    def __init__(self, name, stats, moveType, interactionType, animation, w, h):
        self.name = name
        self.stats = stats
        self.moveType = moveType
        self.interactionType = interactionType
        self.animation = animation
        self.dir = 'r'
        self.x, self.y = 0, 0
        self.rect = pygame.Rect(self.x, self.y, w, h)

        self.setAnimation()

    def update(self):
        if self.interactionType == 1:
            pass
        if self.interactionType == 2:
            pass
        
        if self.moveType == 1:
            pass
        if self.moveType == 0:
            pass

        pass
    
    def move(self):
        pass

    def setAnimation(self):
        setAnimations = self.animation[self.dir]
        self.image = setAnimations[0]
        pass


def goblin():
    gobImage = pygame.image.load('sample_assets/sampleGoblin.png')
    return npc('goblin', {'str': 11, 'dex': 12, 'wis': 9}, 1, 2, {'u': [gobImage], 'd': [gobImage], 'l': [gobImage], 'r': [gobImage], 'fullArt': gobImage}, 64, 64)

#class enemy:
#      def __init__(self, name):
#             self.name = name   
#
#def goblin():
#   return enemy('goblin')
#
#gob1 = goblin()
#