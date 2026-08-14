import pygame
from healthbar import StaticHealthBar

class Player:
    def __init__(self, screenWidth, screenHeight):
        self.name = "player"
        self.maxHealth = 30
        self.health = self.maxHealth
        self.reload = 1500
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.width = 100
        self.height = 100
        self.speed = 5
        self.rect = pygame.Rect(
            self.screenWidth//2 - self.width//2,
            self.screenHeight - self.height*2.5,
            self.width, 
            self.height
        )
        healthBarHeight = 20
        self.healthBar = StaticHealthBar(
            self.screenWidth,
            healthBarHeight,
            0,
            self.screenHeight-healthBarHeight
        )
        self.color = "white"

    def move (self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > -self.width/2: self.rect.x -= self.speed 
        if keys[pygame.K_RIGHT] and self.rect.x < self.screenWidth-self.width/2: self.rect.x += self.speed 
        if keys[pygame.K_UP] and self.rect.y > 0: self.rect.y -= self.speed 
        if keys[pygame.K_DOWN] and self.rect.y < self.screenHeight-self.height: self.rect.y += self.speed 

        self.healthBar.update(self)

    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.healthBar.draw(screen)

    def resetHealth (self):
        self.health = self.maxHealth

    def resetPlayer (self):
        self.resetHealth()
        self.rect.x = self.screenWidth//2 - self.width//2
        self.rect.y = self.screenHeight - self.height*2.5
        self.reload = 1500