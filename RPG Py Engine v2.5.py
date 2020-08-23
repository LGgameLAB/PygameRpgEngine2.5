import pygame
import pytmx
import settings
import time
import sys
import npc
import fightScene as fs

pygame.init()

class player:

    def __init__(self, startX, startY, startDir, animations, speed, animationBuffer):
        self.animations = animations
        self.x = int(startX)
        self.y = int(startY)
        self.dir = startDir
        self.vel = speed
        self.width, self.height =  56, 64    #settings.tileSize, settings.tileSize
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height)
        self.fullArt = self.animations['fullArt']
        self.framed = False
        self.animationTick = settings.ticker(animationBuffer)
        
        self.setAnimation()

        self.stats = settings.stats(20, 20, 1, 0,)
        self.stats.inventory.addItems(settings.basicSword())
        self.stats.inventory.addItems(settings.basicJavelin())

    def move(self, walls):
        keys = pygame.key.get_pressed()

        clicked = False
        
        keySet = settings.globalBtnSet

        if keys[keySet['u']]:
            self.y -= self.vel
            self.dir = 'u'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['d']]:
            self.y += self.vel
            self.dir = 'd'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['r']]:
            self.x += self.vel
            self.dir = 'r'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['l']]:
            self.x -= self.vel
            self.dir = 'l'
            self.checkCollide(walls)
            clicked = True

        # else:
            # self.moveTick.tick()

        # if clicked:
        #    self.moveTick.tick()
            # time.sleep(self.moveBuffer)

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
        self.image#.convert()

        self.x = 0
        self.y = 0

        self.dialogue = False

        self.event = False

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

            if tile_object.name == 'goblin':
                try:
                    self.sprites.append(npc.goblin(tile_object.x * self.scale, tile_object.y * self.scale, tile_object.dialogue))
                except:
                    self.sprites.append(npc.goblin(tile_object.x * self.scale, tile_object.y * self.scale, settings.defText))
            
            if tile_object.name == 'goblin2':
                self.sprites.append(npc.goblin2(tile_object.x * self.scale, tile_object.y * self.scale))

                


    #def wallOffset(self, offset):
    #    print(self.walls)
    #    for wall in self.walls:
    #        wall = wall.move(offset)
    def returnCollision(self):
        spriteRects = []
        for sprite in self.sprites:
            spriteRects.append(sprite.rect)
        
        collision = self.walls + spriteRects
        return collision



    def loadSprites(self, *args):
        for arg in args:
            self.sprites.append(arg)

    def update(self, playerRect):
        pause = False
        allActivity = False

        for sprite in self.sprites:
            if self.event != False:
                if self.event.id == "dialogue":
                    pause = True

                if self.event.id == "optionBox":
                    pause = True

            sprite.update(self.walls, playerRect, pause)

            if sprite.dialogueBox.active:
                allActivity = True
                if self.event == False:
                    self.event = sprite.dialogueBox
            
            if sprite.optionBox.active:
                allActivity = True
                if self.event == False:
                    self.event = sprite.optionBox
            
            if sprite.fightActive:
                allActivity = True
                if self.event == False:
                    self.event = sprite
            
        
        if allActivity == False:
            self.event = False


    def returnEvent(self):
        return self.event


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

    def __init__(self):
        self.buffer = settings.buffer
        self.useCam = True
        self.mapLayer = []
        self.spriteLayer = []
        self.fightSceneLayer = []
        self.dialogueLayer = []
        self.fightSceneBool = False
        self.fightScene = False
        self.new()

    def new(self):
        self.win = pygame.display.set_mode(
            (settings.winWidth, settings.winHeight), pygame.RESIZABLE)
        self.map = roomGroup()
        room1 = room("dungeonTest.tmx", settings.tileSize)
        room2 = room("farm1.4.tmx", settings.tileSize)
        self.map.addRooms(room1, room2)
        #charImagePath = 'sample_assets/LukeDaWizard.png'
        charImagePath = 'sample_assets/LukeDaKnight.png'
        charFullArtPath = 'sample_assets/knightFullArt.png'
        charImage = pygame.image.load(charImagePath)
        charFullArt = pygame.image.load(charFullArtPath)
        charAnimation = {'u': [charImage], 'd': [charImage], 'l': [
            charImage], 'r': [charImage], 'fullArt': charFullArt}
        self.player = player(
            self.map.room.pStartX, self.map.room.pStartY, 'r', charAnimation, 4, 10)

        self.cam = cam(self.map.room.width, self.map.room.height, True)
        self.mapLayer.append(self.map.room)
        self.spriteLayer.append(self.player)


        for sprite in self.map.room.sprites:
            self.spriteLayer.append(sprite)

    def events(self):
        self.map.update()
        self.map.room.update(self.player.rect)
        event = self.map.room.returnEvent()
        self.dialogueLayer.clear()
        self.fightSceneLayer.clear()
        if event != False:
            #This seems wierd but may add new layer for optionbox situations
            if event.id == "dialogue":
                self.dialogueLayer.append(event)

            if event.id == "optionBox":
                self.dialogueLayer.append(event)
                if event.subMenuActive:
                    for sprite in event.returnMenu():
                        self.dialogueLayer.append(sprite)

            if event.id == "battleSprite":
                if self.fightScene != False:
                    self.fightSceneLayer.append(self.fightScene)
                    self.fightScene.update()
                    self.dialogueLayer.append(self.fightScene.options)
                    if self.fightScene.options.subMenuActive:
                        for sprite in self.fightScene.options.returnMenu():
                            self.dialogueLayer.append(sprite)
                else:
                    self.fightScene = fs.fightScene(self.player, event)
                    self.fightSceneLayer.append(self.fightScene)
                    self.fightScene.update()
            else:
                self.fightScene = False
                    
        else:
            self.player.move(self.map.room.returnCollision())


        self.cam.update(self.player)

        pass


    def rendScreen(self):
        self.win.fill(settings.bgColor)

        for item in self.mapLayer:
            self.win.blit(item.image, self.cam.apply(item))

        for item in self.spriteLayer:
            if item.framed:
                self.win.blit(item.image, self.cam.apply(item), item.frame)
            else:
                self.win.blit(item.image, self.cam.apply(item))

        for item in self.fightSceneLayer:
            #if item.framed:
            #    self.win.blit(item.image, item.fightRect, item.frame)
            #else:
            #    self.win.blit(item.image, item.fightRect)


            self.win.blit(item.image, item.rect)

        for item in self.dialogueLayer:
            self.win.blit(item.image, item.rect)

        
    def mainloop(self):
        pygame.display.set_caption(settings.winTitle)
        run = True

        
        while run:
            
            time.sleep(self.buffer)

            # Window exit checker

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.VIDEORESIZE:
                    self.win = pygame.display.set_mode((event.w, event.h),
                        pygame.RESIZABLE)
                    
                    settings.winWidth = event.w
                    settings.winHeight = event.h

            self.events()
            self.rendScreen()

            pygame.display.update()





game1 = game()
game1.mainloop()

pygame.quit()
