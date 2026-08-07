import pygame

class Bullet:
    def __init__(self, playerX, playerY, playerWidth):
        self.name = "bullet"
        self.speed = 7
        self.health = 33
        self.color = "blue"
        self.width = 15
        self.height = 45
        self.rect = pygame.Rect(
            playerX + playerWidth/2 - self.width/2,
            playerY,
            self.width,
            self.height
        )

    def move (self):
        self.rect.y -= self.speed

    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)