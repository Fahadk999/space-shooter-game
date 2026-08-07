import pygame

class StaticHealthBar:
    def __init__(self, width, height, posX, posY):
        self.width = width 
        self.height = height
        self.fillRect = pygame.Rect(
            posX,
            posY,
            self.width,
            self.height
        )
        self.rect = pygame.Rect(
            posX,
            posY,
            self.width,
            self.height
        )
        self.fillColor = "orange"
        self.color = "maroon"
        
    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.fillColor, self.fillRect)

    def update (self, other):
        # the damage done
        self.fillRect.width = (other.health/other.maxHealth) * self.width 