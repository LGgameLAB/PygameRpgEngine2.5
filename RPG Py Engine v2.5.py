import pygame
import pytmx
import settings
import time
import sys
import npc
import fightScene as fs
import fx
import sounds

pygame.init()

class player:

    def __init__(self, startX, startY, startDir, animations, speed, animationBuffer):
        self.animations = animations
        self.x = int(startX)
        self.y = int(startY)
        self.dir = startDir
        self.vel = speed
        self.width, self.height = 56, 64  # settings.tileSize, settings.tileSize
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
            self.image = setAnimations[0]#.convert()
            #win.blit(self.image, (self.x, self.y))

    def rotate(self, angle):
        self.image2 = self.fullArt
        self.image = pygame.transform.rotate(self.image2, angle)

class door:
    def __init__(self, name, rect, destinationName, outDir): 
        self.id = 'door'
        self.name = name
        self.rect = rect
        self.active = False
        if outDir == 'u':
            self.endRect = pygame.Rect(self.rect[0], self.rect[1] - 64, self.rect[2], self.rect[3])
        
        elif outDir == 'd':
            self.endRect = pygame.Rect(self.rect[0], self.rect[1] + 64, self.rect[2], self.rect[3])
        
        elif outDir == 'l':
            self.endRect = pygame.Rect(self.rect[0] + 64, self.rect[1], self.rect[2], self.rect[3])
        
        else:
            self.endRect = pygame.Rect(self.rect[0] - 64, self.rect[1], self.rect[2], self.rect[3])

        self.destName = destinationName

class trigger:
    def __init__(self, rect, type, value):
        self.id = "trigger"
        self.rect = rect
        self.type = type
        self.value = value
        self.active = False

    
class room:

    def __init__(self, filename, tileProportion):
        tiledMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.tileWidth = tiledMap.tilewidth
        self.tileHeight = tiledMap.tileheight
        print(tileProportion)
        print(self.tileWidth)
        self.scale = int(tileProportion / self.tileWidth)
        self.tmxdata = tiledMap
        try:
            self.id = tiledMap.properties['gameId']
            print(self.id)
        except:
            print("no Id")
        self.width = (tiledMap.width * self.scale) * tiledMap.tilewidth
        self.height = (tiledMap.height * self.scale) * tiledMap.tileheight
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.framed = False

        self.walls = []
        self.sprites = []
        self.doors = []
        self.triggers = []

        # self.fullArt =

        self.image = pygame.Surface((self.width, self.height))
        self.load()
        self.image  # .convert()

        self.x = 0
        self.y = 0

        self.dialogue = False

        self.events = []

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
                    self.sprites.append(npc.goblin(
                        tile_object.x * self.scale, tile_object.y * self.scale, tile_object.dialogue))
                except:
                    self.sprites.append(npc.goblin(
                        tile_object.x * self.scale, tile_object.y * self.scale, settings.defText))

            if tile_object.name == 'goblin2':
                self.sprites.append(npc.goblin2(
                    tile_object.x * self.scale, tile_object.y * self.scale))
            
            if tile_object.name == 'door':
                rect = pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                                              int(tile_object.width*self.scale), int(tile_object.height*self.scale))
                                            
                self.doors.append(door(tile_object.selfName, rect, tile_object.destName,  tile_object.outDir))

            if tile_object.name == 'trigger':
                    rect = pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                        int(tile_object.width*self.scale), int(tile_object.height*self.scale))
                    
                    self.triggers.append(trigger(rect, tile_object.functionType, tile_object.value))


    # def wallOffset(self, offset):
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

    def update(self, player):
        pause = False
        playerRect = player.rect

        for event in self.events:
            if event.active == False:
                self.events.remove(event)

        self.checkDoor(player)
        self.checkTrigger(player)
            

        for sprite in self.sprites:
            if self.checkEventslen():
                pause = True

            sprite.update(self.walls, playerRect, pause)

            if sprite.dialogueBox.active:
                if not sprite.dialogueBox in self.events:
                    self.events.append(sprite.dialogueBox)

            if sprite.optionBox.active:
                if not sprite.optionBox in self.events:
                    self.events.append(sprite.optionBox)

            if sprite.active:
                if not sprite in self.events:
                    self.events.append(sprite)


    def checkDoor(self, player):
        result = False
        for door in self.doors:
            if door.rect.colliderect(player.rect):

                self.events.append(door)
                result = True
                print("door")

        return result
    
    def checkTrigger(self, player):
        for trigger in self.triggers:
            if trigger.rect.colliderect(player.rect):
                self.events.append(trigger)
                #print("Trigger")
                #print("Pizza Ass")

    def returnEvent(self):
        return self.events

    def checkEventslen(self):
        if len(self.events) < 1:
            return False
        else:
            return True

class event:
    def __init__(self, id):
        self.id = id

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
    
    def switchRoom(self, destName):
        for room in self.rooms:
            for door in room.doors:
                if door.name == destName:
                    self.room = room 
                    self.roomIndex = self.rooms.index(self.room)

                    return door.endRect[0], door.endRect[1]
        


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
        self.fxLayer = []
        self.fx = []
        self.mixer = sounds.mixer()
        self.mixer.playMusic(sounds.music["intro"], -1)
        self.fightSceneBool = False
        self.fightScene = False
        self.fullScreen = False

        if settings.winResizeable:
            self.win = pygame.display.set_mode(
                (settings.winWidth, settings.winHeight), pygame.RESIZABLE)
        else:
            self.win = pygame.display.set_mode(
                (settings.winWidth, settings.winHeight))
        
        
        self.new()

    def new(self):
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
            self.map.room.pStartX, self.map.room.pStartY, 'r', charAnimation, 8, 10)

        self.cam = cam(self.map.room.width, self.map.room.height, True)
        self.mapLayer.append(self.map.room)
        self.spriteLayer.append(self.player)

        for sprite in self.map.room.sprites:
            self.spriteLayer.append(sprite)

    def events(self):
        self.map.update()
        self.map.room.update(self.player)
        events = self.map.room.returnEvent()
        self.dialogueLayer.clear()
        self.fightSceneLayer.clear()
        self.mapLayer.clear()
        self.spriteLayer.clear()

        movePause = False
        

        if len(events) > 0:
            # This seems wierd but may add new layer for optionbox situations
            for event in events: 
                if event.id == "dialogue":
                    self.dialogueLayer.append(event)
                    movePause = True

                if event.id == "optionBox":
                    self.dialogueLayer.append(event)
                    movePause = True
                    if event.subMenuActive:
                        for sprite in event.returnMenu():
                            self.dialogueLayer.append(sprite)

                if event.id == "door":
                    self.player.x, self.player.y = self.map.switchRoom(event.destName)
                    movePause = True
                
                if event.id == "trigger":
                    if event.type == "soundEdit":
                        self.mixer.changeVolume(event.value)

                if event.id == "battleSprite":
                    movePause = True
                    if self.fightScene != False:
                        self.fightSceneLayer.append(self.fightScene)
                        self.fightScene.update()
                        if self.fightScene.options != False:
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

        if not movePause:
            self.player.move(self.map.room.returnCollision())

        self.mixer.update(events)

        self.spriteLayer.append(self.player)

        for sprite in self.map.room.sprites:
            self.spriteLayer.append(sprite)

        for fx in self.fxLayer:
            fx.update()
            if fx.active == False:
                self.fxLayer.remove(fx)

        self.mapLayer.append(self.map.room)

        self.cam.update(self.player)

        

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
            # if item.framed:
            #    self.win.blit(item.image, item.fightRect, item.frame)
            # else:
            #    self.win.blit(item.image, item.fightRect)

            self.win.blit(item.image, item.rect)

        for item in self.dialogueLayer:
            self.win.blit(item.image, item.rect)
        
        print(len(self.fx))
        for item in self.fxLayer:
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

                if settings.winResizeable:
                    if event.type == pygame.VIDEORESIZE:
                        self.win = pygame.display.set_mode((event.w, event.h),
                                                        pygame.RESIZABLE)

                    settings.winWidth = event.w
                    settings.winHeight = event.h
                    settings.dialogueBoxSize = (event.w, int(event.h/4))

            self.getFullScreen()
            self.events()
            self.rendScreen()

            pygame.display.update()

    def getFullScreen(self):
        if settings.fullScreenActive:
            keys = pygame.key.get_pressed()
            if keys[settings.globalBtnSet['fullScreen']]:
                if self.fullScreen:
                    self.win = pygame.display.set_mode((settings.winWidth, settings.winHeight))
                    self.fullScreen = False
                else:
                    self.win = pygame.display.set_mode((settings.winWidth, settings.winHeight), pygame.FULLSCREEN)
                    self.fullScreen = True


game1 = game()
game1.mainloop()

pygame.quit()
