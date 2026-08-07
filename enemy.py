import pygame
from random import randint

class Enemy:
    def __init__(self, screenWidth):
        if not hasattr(self, 'health'): self.health = 75
        if not hasattr(self, 'points'): self.points = 30
        if not hasattr(self, 'width'): self.width = 55
        if not hasattr(self, 'height'): self.height = 55
        if not hasattr(self, 'baseSpeed'): self.baseSpeed = 2
        if not hasattr(self, 'color'): self.color = "orange"

        self.rect = pygame.Rect(
            randint(0, screenWidth-self.width),
            -self.height,
            self.width,
            self.height,
        )

    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collide (self, other) -> bool: 
        if self.health > 0 and other.health > 0 and self.rect.colliderect(other.rect):
            selfDmg = self.health
            otherDmg = other.health 

            self.health = max(0, self.health - otherDmg)
            other.health = max(0, other.health - selfDmg)

            if self.health == 0:
                return True

        return False

    def update (self):
        self.rect.y += self.baseSpeed

