import pygame
import time
import settings as stgs


class animation:

    def __init__(self, ImgSheet, dir, buffer):
        self.ImgSheet = ImgSheet
        self.framex = 0
        self.frame = pygame.Rect(self.framex, 0, 64, 64)
        self.buffer = buffer
        self.cycle = False
        self.dir = dir

    def update(self, par1, dir):
        self.dir = dir
        if par1:
            if self.cycle:
                if self.framex == self.ImgSheet[self.dir].get_width() - 64:
                    self.framex = 0
                else:
                    self.framex += 64

            else:
                self.cycle = True

        else:
            self.cycle = False
            self.framex = 0

        self.frame = pygame.Rect(self.framex, 0, 64, 64)

    def GetFrame(self):
        return self.frame

    def GetImg(self):
        return self.ImgSheet[self.dir]
