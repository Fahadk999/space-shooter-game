import pygame

class Bullet:
    def __init__(self, playerX, playerY, playerWidth, incBy=0):
        self.name = "bullet"
        self.defaultSpeed = 7
        self.speed = self.defaultSpeed
        self.defaultHealth = 33
        self.health = self.defaultHealth + incBy
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

    def resetBullet (self):
        self.speed = self.defaultSpeed
        self.health = self.defaultHealth