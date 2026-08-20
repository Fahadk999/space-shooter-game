import pygame
from random import randint

class Enemy:
    def __init__(self, screenWidth, screenPosX, screenPosY):
        if not hasattr(self, 'maxHealth'): self.maxHealth = 75
        if not hasattr(self, 'health'): self.health = self.maxHealth
        if not hasattr(self, 'points'): self.points = 30
        if not hasattr(self, 'width'): self.width = 55
        if not hasattr(self, 'height'): self.height = 55
        if not hasattr(self, 'baseSpeed'): self.baseSpeed = 2
        if not hasattr(self, 'color'): self.color = pygame.Color("orange")
        if not hasattr(self, 'baseColor'): self.baseColor = self.color 
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY

        self.rect = pygame.Rect(
            randint(self.screenPosX, screenWidth-self.width),
            self.screenPosY-self.height,
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
        self.colorDarkens()

    def healthUp (self):
        self.health += int(self.health * 0.05)

    def colorDarkens(self):
        # Get health percentage (0.0 to 1.0)
        health_pct = self.health / self.maxHealth

        if health_pct <= 0.15:
            self.color = self.baseColor.correct_gamma(0.2)
        elif health_pct <= 0.45:
            self.color = self.baseColor.correct_gamma(0.5)
        elif health_pct <= 0.75:
            self.color = self.baseColor.correct_gamma(0.7)
        else:
            self.color = self.color