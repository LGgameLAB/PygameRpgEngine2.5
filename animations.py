import pygame
import time
import settings as stgs


class animation:

    def __init__(self, ImgSheet, dir, buffer, startFrame):
        self.ImgSheet = ImgSheet
        self.startFrame = startFrame * stgs.tileSize
        self.framex = self.startFrame
        self.frame = pygame.Rect(self.framex, 0, stgs.tileSize, stgs.tileSize)
        self.buffer = buffer
        self.cycle = False
        self.dir = dir

    def update(self, par1, dir):
        self.dir = dir
        if par1:
            if self.cycle:
                if self.framex == self.ImgSheet[self.dir].get_width() - stgs.tileSize:
                    self.framex = 0
                else:
                    self.framex += stgs.tileSize

            else:
                self.cycle = True

        else:
            self.cycle = False
            self.framex = self.startFrame

        self.frame = pygame.Rect(self.framex, 0, stgs.tileSize, stgs.tileSize)

    def GetFrame(self):
        return self.frame

    def GetImg(self):
        return self.ImgSheet[self.dir]
