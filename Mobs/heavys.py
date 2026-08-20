import pygame
from Mobs.enemy import Enemy

class Heavys(Enemy):
    def __init__(self, screenWidth, screenPosX, screenPosY):
        self.baseSpeed = 1
        self.maxHealth = 150
        self.health = self.maxHealth
        self.width = 90
        self.height = 90
        self.color = pygame.Color("purple")
        self.points = 100

        super().__init__(screenWidth, screenPosX, screenPosY)