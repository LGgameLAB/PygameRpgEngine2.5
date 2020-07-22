import pygame
import pytmx
import settings
import time
import sys
import npc


class player:

    def __init__(self, startX, startY, startDir, animations, moveBuffer, speed, animationBuffer):
        self.animations = animations
        self.x = int(startX)
        self.y = int(startY)
        self.moveBuffer = moveBuffer/100
        #self.animationSpeed = animationSpeed
        self.dir = startDir
        self.vel = speed
        self.width, self.height = settings.tileSize, settings.tileSize
        self.rect = pygame.Rect(
            self.x, self.y, settings.tileSize,  settings.tileSize)
        self.fullArt = self.animations['fullArt']
        self.framed = False
        self.moveTick = settings.ticker(moveBuffer)
        self.moveTick.done = False
        self.animationTick = settings.ticker(animationBuffer)

        self.setAnimation()

    def move(self, walls):
        keys = pygame.key.get_pressed()

        clicked = False
        #if self.moveTick.done:
        if keys[pygame.K_UP]:
            self.y -= self.vel
            self.dir = 'u'
            self.checkCollide(walls)
            clicked = True
        if keys[pygame.K_DOWN]:
            self.y += self.vel
            self.dir = 'd'
            self.checkCollide(walls)
            clicked = True
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.dir = 'r'
            self.checkCollide(walls)
            clicked = True
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.dir = 'l'
            self.checkCollide(walls)
            clicked = True

        #else:
            #self.moveTick.tick()

        #if clicked:
        #    self.moveTick.tick()
            #time.sleep(self.moveBuffer)

        self.x = int(self.x)
        self.y = int(self.y)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        #print(str(self.x) + " " + str(self.y))

    def update(self, walls):
        self.move(walls)
        
        if self.animationTick.done:
            self.setAnimation()

        
        self.animationTick.tick()

    def checkCollide(self, walls):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if wall.colliderect(self.rect):
                if self.dir == 'l':
                    self.x += self.vel
                elif self.dir == 'r':
                    self.x -= self.vel
                elif self.dir == 'u':
                    self.y += self.vel
                else:
                    self.y -= self.vel

    def setAnimation(self):
        setAnimations = self.animations[self.dir]

        if len(setAnimations) > 1:
            pass
        else:
            self.image = setAnimations[0]  # .convert()\
            #win.blit(self.image, (self.x, self.y))


class room:

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
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.framed = False

        self.walls = []
        self.sprites = []

        # self.fullArt =

        self.image = pygame.Surface((self.width, self.height))
        self.load()
        self.image.convert()

        self.x = 0
        self.y = 0

    def load(self):
        tile = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    # if tile:
                    if not tileImage is None:
                        #tileRect = pygame.Rect(x * (self.tmxdata.tilewidth * self.scale), y * (self.tmxdata.tileheight * self.scale),self.tileWidth, self.tileHeight)
                        tileImage = pygame.transform.scale(
                            tileImage, (self.tmxdata.tilewidth * self.scale, self.tmxdata.tileheight * self.scale)).convert()
                        self.image.blit(tileImage, (x * (self.tmxdata.tilewidth *
                                                         self.scale), y * (self.tmxdata.tileheight * self.scale)))

        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'player':
                self.pStartX, self.pStartY = int(
                    tile_object.x*self.scale), int(tile_object.y*self.scale)

            if tile_object.name == 'wall' or tile_object.name == 'void':
                self.walls.append(pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                                              int(tile_object.width*self.scale), int(tile_object.height*self.scale)))

            # if tile_object.name == 'void':
            #    self.walls.append(pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale), int(tile_object.width*self.scale), int(tile_object.height*self.scale)))

    def wallOffset(self, offset):
        print(self.walls)
        for wall in self.walls:
            wall = wall.move(offset)

    def loadSprites(self, *args):
        for arg in args:
            self.sprites.append(arg)

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    # def render(self, win):
    #    win.blit(self.tempSurface, (self.x, self.y))

    # def makeMap(self):
    #    tempSurface = pygame.Surface((self.width, self.height)).convert()
    #    self.render(tempSurface)
    #    self.mapImage = tempSurface.convert()


class roomGroup:
    def __init__(self):
        self.rooms = []
        self.roomIndex = 0
        #self.room = self.rooms[self.roomIndex]

    def addRooms(self, *args):

        for arg in args:
            self.rooms.append(arg)

        self.update()

    def update(self):
        self.room = self.rooms[self.roomIndex]


class cam:

    def __init__(self, width, height, limit):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.limit = limit

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(settings.winWidth / 2)
        y = -target.rect.centery + int(settings.winHeight / 2)

        # limit scrolling to map size
        if self.limit:
            x = min(0, x)  # left
            y = min(0, y)  # top
            x = max(-(self.width - settings.winWidth), x)  # right
            y = max(-(self.height - settings.winHeight), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)


class game:

    def __init__(self, buffer):
        self.buffer = (buffer / 1000)
        self.useCam = True
        self.camLayers = [1]
        self.fightSceneBool = False
        self.new()

    def new(self):
        self.win = pygame.display.set_mode(
            (settings.winWidth, settings.winHeight))
        self.map = roomGroup()
        room1 = room("dungeonTest.tmx", settings.tileSize)
        room2 = room("farm1.4.tmx", settings.tileSize)
        self.map.addRooms(room1, room2)
        charImagePath = 'LukeDaWizard.png'
        charImage = pygame.image.load(charImagePath)
        charAnimation = {'u': [charImage], 'd': [charImage], 'l': [
            charImage], 'r': [charImage], 'fullArt': charImage}
        self.player = player(
            self.map.room.pStartX, self.map.room.pStartY, 'r', charAnimation, 4, 1, 10)
        gob1 = npc.goblin()
        self.map.room.loadSprites(gob1)
        self.cam = cam(self.map.room.width, self.map.room.height, True)
        pygame.display.set_caption(settings.winTitle)

    def events(self):
        self.map.update()
        self.map.room.update()
        pass

    def fightScene(self):
        self.useCam = False
        self.fightSceneBool = True
        while self.fightSceneBool:

            pass

    def rendScreen(self, *args):
        self.win.fill(settings.bgColor)
        x = 0
        for arg in args:
            x += 1

            if (x in self.camLayers):
                for item in arg:
                    if item.framed:
                        self.win.blit(
                            item.image, self.cam.apply(item), item.frame)
                    else:
                        self.win.blit(item.image, self.cam.apply(item))
            else:
                for item in arg:
                    if self.fightSceneBool:
                        self.win.blit(item.fullArt, item.rect)
                    else:
                        if item.framed:
                            self.win.blit(item.image, item.rect, item.frame)
                        else:
                            self.win.blit(item.image, item.rect)

    def mainloop(self):

        run = True

        while run:
            time.sleep(self.buffer)

            # Window exit checker

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.events()
            self.player.move(self.map.room.walls)
            # self.room.wallOffset(self.cam.camera.topleft)
            self.cam.update(self.player)
            self.rendScreen([self.map.room, self.player] +
                            self.map.room.sprites)
            pygame.display.update()


pygame.init()


game1 = game(1)
game1.mainloop()

pygame.quit()
