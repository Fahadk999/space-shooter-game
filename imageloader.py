import pygame

class loadImage:
    def __init__(self, path, scale, posX, posY):

        self.rawImage = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.rawImage, scale
        )
        self.rect = self.image.get_rect(center=(posX, posY))

    def draw (self, screen):
        screen.blit(self.image, self.rect)

    def resize (self, width, height):
        prevCenter = self.rect.center
        self.image = pygame.transform.scale(
            self.rawImage, (width, height)
        )
        self.rect = self.image.get_rect(center=prevCenter)
