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
dialogueBox1 = 'sample_assets/dialogueBox.png'
optionBox1 = 'sample_assets/optionBox.png'

fightSceneOverlay1 = 'sample_assets/fightSceneOverlay1.jpg'

globalBtnSet = {'u' : pygame.K_UP, 'd' : pygame.K_DOWN, 'l' : pygame.K_LEFT, 'r' : pygame.K_RIGHT, 'interactionBtn' : pygame.K_z,
     'scrollUpBtn' : pygame.K_UP, 'scrollDownBtn' : pygame.K_DOWN, 'menusBtn' : pygame.K_z, 'menusBack' : pygame.K_x}

#interactionBtn = pygame.K_z

##scrollDownBtn = pygame.K_DOWN
#menusBtn = pygame.K_z

font1 = pygame.font.Font('freesansbold.ttf', 24)

defText = "Hi"

fightOptions = ['Attack', 'Items', 'Run']

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

statFormat = {"Health": '', "Level": '', "Experience": 0, "Power": 10, "Cunning": 10}


class attack:
    def __init__(self, damage, type):
        self.damage = damage
        self.type = type

class item:
    def __init__(self, name, id):
        pass

class weapon:
    def __init__(self, damage, type, name):
        self.attack = attack(damage, type)
        self.id = 'weapon'
        self.name = name

class inventory:
    def __init__(self):
        self.items = []
    
    def addItems(self, *args):
        for arg in args:
            self.items.append(arg)

class stats:
    def __init__(self, *args):
        global statFormat

        self.stats = {}
        x = 0
        for k in statFormat:
            self.stats[k] = args[x]
            x += 1

        self.attackList = []
    
    def addInventory(self, *args):
        self.inventory = inventory()
        if len(args) > 0:
            for arg in args:
                self.inventory.addItems(arg)

    def addAttacks(self, *args):
        for arg in args:
            self.attackList.append(arg)

def basicSword():
    return weapon(6, 'slash', 'Basic Sword')