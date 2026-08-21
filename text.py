import pygame

class Text:
    def __init__(self, text, posX, posY):
        self.posX = posX
        self.posY = posY
        self.color = pygame.Color("white")
        self.text = str(text)
        self.font = pygame.font.Font(None, 48)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.posX, self.posY))
        self.glow = False
        self.glowTimer = 0
        self.glowInterval = 300

    def draw (self, screen):
        screen.blit(self.surface, self.rect)

    def enableGlow (self):
        self.glow = True

    def update (self, text):
        self.surface = self.font.render(str(text), True, self.color)
        self.rect = self.surface.get_rect(center=(self.posX, self.posY))

    def makeGlow (self, dt, glowColor="yellow"):
        if self.glow:
            if self.glowTimer <= self.glowInterval:
                self.glowTimer += dt
                self.color = pygame.Color(glowColor)
                self.surface = self.font.render(self.text, True, self.color)
            else:
                self.glowTimer = 0
                self.color = pygame.Color("white")
                self.surface = self.font.render(self.text, True, self.color)
                self.glow = False
