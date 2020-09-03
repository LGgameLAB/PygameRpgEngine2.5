import pygame

volume = .2
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

sfx = {
    "optionBox": "sounds/sfx/interact.wav",
    "dialogue": "sounds/sfx/interact2.wav",
    "trigger": "sounds/sfx/interact2.wav"
    }
music = {
    "intro": "sounds/music/intro.wav"
    }

class mixer:
    def __init__(self):
        global sfx
        self.sfx = sfx
        self.playedLast = False
        pygame.mixer.music.set_volume(volume)
        #print("Volume = " + volume)

    def update(self, events):
        global sfx

        if self.playedLast:
            if len(events) < 1:
                self.playedLast = False
                
        if events != False:
            eventList = []
            for k in sfx:
                eventList.append(k)
            
            for event in events:
                if event.id in eventList:
                    self.playFx(event.id)
    
    def music(self, song, repeat):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(0)
    
    def changeVolume(self, setVolume):
        #insert new volume as float that is < 1
        volume = setVolume
        if volume < 1:
            pygame.mixer.music.set_volume(volume)
        else:
            print("That volume is too high")

    def stop(self):
        pygame.mixer.music.stop()
    
    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()
    
    def changePosition(self, position):
        self.position = position
        pygame.mixer.music.play(0, self.position)
        #Sets music position in seconds

    def playFx(self, event):
        if not self.playedLast:
            global sfx

            self.loadSound = sfx[event]
            self.sound = pygame.mixer.Sound(self.loadSound)
            self.sound.play()

            self.playedLast = True
    
    def playMusic(self, song, repeat):
        self.loadSong = song
        self.repeat = repeat
        self.play = pygame.mixer.music.load(self.loadSong)
        pygame.mixer.music.play(self.repeat)
