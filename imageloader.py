import pygame

class loadImage:
    def __init__(self, path, scale, posX, posY):

        self.rawImage = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.rawImage, scale
        )
        self.rect = self.image.get_rect(center=(posX, posY))

        # For Idle Y aka up down idle
        self.idleYTimer = 0
        self.idleYUpDir = True
        self.origY = self.rect.y
        self.maxY = self.rect.y+5
        self.minY = self.rect.y-5

    def draw (self, screen):
        screen.blit(self.image, self.rect)

    def resize (self, width, height):
        prevCenter = self.rect.center
        self.image = pygame.transform.scale(
            self.rawImage, (width, height)
        )
        self.rect = self.image.get_rect(center=prevCenter)


    def idleAnimationY (self, dt, speed, interval):
        self.idleYTimer += dt
        if self.idleYTimer >= interval:
            if self.idleYUpDir: # if true
                self.rect.y += -speed
            else:
                self.rect.y += speed
            self.idleYTimer -= interval

        if abs(speed) == speed:
            if self.rect.y >= self.maxY:
                self.idleYUpDir = True
            if self.rect.y <= self.minY:
                self.idleYUpDir = False
        else:
            if self.rect.y >= self.maxY:
                self.idleYUpDir = False
            if self.rect.y <= self.minY:
                self.idleYUpDir = True



        


