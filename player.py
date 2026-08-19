import pygame
from healthbar import StaticHealthBar

class Player:
    def __init__(self, screenWidth, screenHeight):
        self.name = "player"
        self.defaultHealth = 30
        self.maxHealth = self.defaultHealth
        self.health = self.defaultHealth
        self.reload = 1500
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.width = 100
        self.height = 100
        self.speed = 5
        self.turrentWidth = 20
        self.turrentHeight = 20
        self.rect = pygame.Rect(
            self.screenWidth//2 - self.width//2,
            self.screenHeight - self.height*2.5,
            self.width, 
            self.height
        )
        self.turrentRect = pygame.Rect(
            self.rect.x + self.rect.width//2 - self.turrentWidth//2,
            self.rect.y + 5,
            self.turrentWidth,
            self.turrentHeight
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
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed

        dy = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy

        half_width = self.rect.width / 2
        half_height = self.rect.height / 2
        # idk how this min max works :/ chat gpt recommend
        self.rect.left = max(-half_width, self.rect.left)
        self.rect.right = min(self.screenWidth + half_width, self.rect.right)
        self.rect.top = max(-half_height, self.rect.top)
        self.rect.bottom = min(self.screenHeight + half_height, self.rect.bottom)
        self.turrentRect.x = self.rect.x + self.rect.width//2 - self.turrentWidth//2
        self.turrentRect.y = self.rect.y - 5
        self.healthBar.update(self)

    def draw (self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, "red", self.turrentRect)
        self.healthBar.draw(screen)

    def resetHealth (self):
        self.maxHealth = self.defaultHealth
        self.health = self.defaultHealth

    def resetPlayer (self):
        self.resetHealth()
        self.turrentRect.x = self.rect.x + self.rect.width//2 - self.turrentWidth//2
        self.turrentRect.y = self.rect.y - 5
        self.rect.x = self.screenWidth//2 - self.width//2
        self.rect.y = self.screenHeight - self.height*2.5
        self.reload = 1500