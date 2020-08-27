import pygame
import random
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
winResizeable = False
fullScreenActive = True

tileSize = 64
gridWidth = winWidth / tileSize
gridHeight = winHeight / tileSize

fps = 60
buffer = 1/fps

dialogueBox1 = 'sample_assets/dialogueBox.png'
dialogueBoxSize = (winWidth, int(winHeight/4))
retype = True

optionBox1 = 'sample_assets/optionBox.png'

fightSceneOverlay1 = 'sample_assets/fightSceneOverlay1.jpg'

globalBtnSet = {'u' : pygame.K_UP, 'd' : pygame.K_DOWN, 'l' : pygame.K_LEFT, 'r' : pygame.K_RIGHT, 'interactionBtn' : pygame.K_z,
     'scrollUpBtn' : pygame.K_UP, 'scrollDownBtn' : pygame.K_DOWN, 'menusBtn' : pygame.K_z, 'menusBack' : pygame.K_x, 'fullScreen' : pygame.K_f}

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
        self.ticks = buffer

        self.lock = False

    def tick(self):
        if self.done:
            if self.lock:
                pass
            else:
                self.done = False
        else:
            self.ticks -= 1
            if self.ticks < 1:
                self.ticks = self.buffer
                self.done = True
    
    def reset(self, *args):
        self.done = False

        if len(args) > 0:
            self.ticks = args[0]
        else:
            self.ticks = self.buffer

healthKey = "Health"
maxHpKey = "Max Hit Points"
levelKey = "Level"
expKey = "Experience"

statFormat = {maxHpKey: 0, healthKey: 0,levelKey: 0, expKey: 0}

class run:
    def __init__(self, *args):
        if len(args) > 0:
            self.msg = args[0]
        
        self.id = 'run'

class attack:
    def __init__(self, damage, type):
        self.damage = damage
        self.type = type
        self.id = 'attack'

class item:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    
    def getInfo(self):
        return self.name

class weapon:
    def __init__(self, damage, type, name):
        self.attack = attack(damage, type)
        self.id = 'weapon'
        self.name = name
    
    def getInfo(self):
        return self.name

#Weapons are part of items but to access them more easily they have a seperate list
class inventory:
    def __init__(self):
        self.items = []
        self.weapons = []

    def addItems(self, *args):
        for arg in args:
            self.items.append(arg)
        
        for item in self.items:
            if item.id == "weapon":
                self.weapons.append(item)

class stats:
    def __init__(self, *args):
        global statFormat

        self.stats = {}
        if len(args) == 1:
            if isinstance(args[0], list):
                x = 0
                for k in statFormat:
                    self.stats[k] = args[0][x]
                    x += 1
        else:
            x = 0
            for k in statFormat:
                self.stats[k] = args[x]
                x += 1

        self.attackList = []
        self.inventory = inventory()
        self.weakness = ''

    def addAttacks(self, *args):
        for arg in args:
            self.attackList.append(arg)
    
    def recvHit(self, hit):
        global healthKey

        if hit.type == "self.weakness":
            self.stats[healthKey] -= hit.damage*2
        else:
            self.stats[healthKey] -= hit.damage
    
    def randAttack(self):
        randVal = random.randint(0, len(self.inventory.weapons) - 1)
        
    


def basicSword():
    return weapon(6, 'slash', 'Basic Sword')

def basicJavelin():
    return weapon(8, 'piercing', 'Basic Javelin')