import pygame

pygame.font.init()

blue = (0, 0, 128)
black = (0,0,0)
white = (255,255,255)
shadow = (192, 192, 192)
white = (255, 255, 255)
lightGreen = (0, 255, 0)
green = (0, 200, 0)
blue = (0, 0, 128)
lightBlue = (0, 0, 255)
red = (200, 0, 0 )
lightRed = (255, 100, 100)
purple = (102, 0, 102)

winWidth, winHeight = 1024, 768
centerX, centerY = winWidth/2, winHeight/2
winTitle = "RPG Engine v2.5"
bgColor = blue

tileSize = 64
gridWidth = winWidth / tileSize
gridHeight = winHeight / tileSize

fps = 120
buffer = 1/fps

dialogueBox1 = pygame.image.load('sample_assets/dialogueBox.png')


interactionBtn = pygame.K_z

font1 = pygame.font.Font('freesansbold.ttf', 24)

defText = "Hi"

class ticker:
    def __init__(self, buffer):
        self.buffer = buffer
        self.done = False
        self.ticks = 0

        self.lock = False

    def tick(self):
        if self.done:
            if self.lock:
                pass
            else:
                self.done = False
        else:
            self.ticks += 1
            if self.ticks > self.buffer - 1:
                self.ticks = 0
                self.done = True
    
    def reset(self):
        self.done = False
        self.ticks = 0
        #if self.done = False:

        #while x < self.buffer:
        #    X += 1
#goblinAnimationSet = {'u': [charImage], 'd': [charImage], 'l': [charImage], 'r': [charImage], 'fullArt': charImage}