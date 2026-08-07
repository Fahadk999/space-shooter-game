import pygame

class Text:
    def __init__(self, text, posX, posY):
        self.posX = posX
        self.posY = posY
        self.color = "white"
        self.font = pygame.font.Font(None, 48)
        self.surface = self.font.render(str(text), True, self.color)
        self.rect = self.surface.get_rect(center=(self.posX, self.posY))

    def draw (self, screen):
        screen.blit(self.surface, self.rect)

    def update (self, text):
        self.surface = self.font.render(str(text), True, self.color)
        self.rect = self.surface.get_rect(center=(self.posX, self.posY))