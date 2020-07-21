import time
import random 

import pygame
import pytmx

import settings

pygame.init()

width, height = 1024, 768
win = pygame.display.set_mode((width, height))
winRect = pygame.Rect(0, 0, width, height)

class TiledMap:
    def __init__(self, filename, tileProportion):
        tiledMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.tileWidth = tiledMap.tilewidth
        self.tileHeight = tiledMap.tileheight
        print(tileProportion)
        print(self.tileWidth)
        self.scale = int(tileProportion / self.tileWidth)
        self.tmxdata = tiledMap
        self.width = (tiledMap.width * self.scale) * tiledMap.tilewidth
        self.height = (tiledMap.height * self.scale) * tiledMap.tileheight
        
        

    def render(self, surface):
        global winRect
        
        tile = self.tmxdata.get_tile_image_by_gid

        #self.offsetX = offsetX
        #self.offsetY = offsetY
        
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    if tile:
                        if not tileImage is None:
                            tileRect = pygame.Rect(x * (self.tmxdata.tilewidth * self.scale), y * (self.tmxdata.tileheight * self.scale),self.tileWidth, self.tileHeight)
                            tileImage = pygame.transform.scale(tileImage, (self.tmxdata.tilewidth * self.scale, self.tmxdata.tileheight * self.scale)).convert()
                            surface.blit(tileImage, (x * (self.tmxdata.tilewidth * self.scale), y * (self.tmxdata.tileheight * self.scale)))

    def makeMap(self):
        tempSurface = pygame.Surface((self.width, self.height)).convert()
        self.render(tempSurface)
        self.mapImage = tempSurface.convert()
        #return tempSurface
                        


def mainLoop():
    vroomX, vroomY = 0, 0
    testMap = TiledMap("dungeonTest.tmx" , settings.tileSize)
    testMap.makeMap()
    renderedMap = testMap.mapImage
    while True:
        time.sleep(0.05)
        win.fill(settings.black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.blit(renderedMap, (vroomX, vroomY))
        vroomX += random.randint(0,1)
        vroomY +=randok
        pygame.display.update()
mainLoop()
