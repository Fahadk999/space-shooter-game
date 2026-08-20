import pygame
from Mobs.enemy import Enemy

class Fasts(Enemy):
    def __init__(self, screenWidth, screenPosX, screenPosY):
        self.baseSpeed = 4
        self.maxHealth = 35
        self.health = self.maxHealth
        self.points = 50
        self.width = 30
        self.height = 30
        self.color = pygame.Color("cyan")

        super().__init__(screenWidth, screenPosX, screenPosY)
