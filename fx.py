import pygame
import settings as stgs 
import random

class fadeIn:
    def __init__(self, speed):
        self.active = True
        self.rect = pygame.Rect(0, 0, stgs.winWidth, stgs.winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.alpha = 255
        self.speed = speed

    def update(self):
        if self.active:
            if not self.alpha < 1:
                self.alpha -= self.speed
            else:
                self.active = False

            self.image.set_alpha(self.alpha)

class fadeOut:
    def __init__(self, speed):
        self.active = True
        self.rect = pygame.Rect(0, 0, stgs.winWidth, stgs.winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.alpha = 0
        self.speed = speed

    def update(self):
        if self.active:
            if not self.alpha > 250:
                self.alpha += self.speed
            else:
                self.active = False

            self.image.set_alpha(self.alpha)

class rectOut:
    def __init__(self):
        self.width, self.height = 20, 20
        self.rect = pygame.Rect(stgs.winWidth/2, stgs.winHeight/2, self.width, self.height)
        self.ogImage = pygame.surface.Surface((self.width*2, self.height*2))
        self.active = True
        self.limWidth = stgs.winWidth
        self.scale = 1
        self.angle = 0

        self.ogImage.fill(stgs.black)

        pygame.draw.rect(self.ogImage, stgs.white, (0, 0, self.width, self.height))
    
    def render(self):
        pass

    def update(self):
        if self.active:
            if self.width < self.limWidth:
                self.image = pygame.transform.rotate(self.ogImage, self.angle)
                #self.image = self.ogImage
                self.angle += 1 % 360  # Value will reapeat after 359. This prevents angle to overflow.
                x, y = self.rect.center  # Save its current center.
                self.rect = self.image.get_rect()  # Replace old rect with new rect.
                self.rect.center = (x, y)
                
            else:
                self.active = False #gonna test this now
    
class squareOut:
    def __init__(self):
        pass
    
class flash:
    def __init__(self, color, times, secondsBetween):
        self.active = True
        self.rect = pygame.Rect(0, 0, stgs.winWidth, stgs.winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        self.color = color
        self.image.fill(self.color)
        self.times = times
        self.alpha = 255
        self.between = secondsBetween
        self.bufferTime = stgs.buffer
        self.between2 = self.between
        
        
    def update(self):
        if self.active:
            if self.times > 0:
                if self.between2 < 0:
                    if self.alpha == 0:
                        self.alpha = 255
                        self.image.set_alpha(self.alpha)
                        self.between2 = self.between
                    elif self.alpha == 255:
                        self.alpha = 0
                        self.image.set_alpha(self.alpha)
                        self.between2 = self.between
                        self.times = self.times - 1
                else:
                    self.between2 = self.between2 - self.bufferTime
            else:
                self.alpha = 0
                self.image.set_alpha(self.alpha)
                self.active = False