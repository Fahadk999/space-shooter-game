import pygame
from random import choice
from imageloader import loadImage
from button import ImageButton

class MenuState():
    def __init__(self, screenWidth, screenHeight, screenPosX, screenPosY) -> None:
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY
        self.scaleFactor = 1
        self.titleImage = loadImage("assets/texts/title.png", self.scaleFactor, self.screenWidth // 2, self.screenHeight // 3)
        self.startPromptImage = loadImage("assets/texts/pressSpace.png", self.scaleFactor, self.screenWidth // 2, self.screenHeight // 2)
        self.prestigeButton = ImageButton("assets/logos/prestige.png", self.screenWidth//2, self.screenHeight - 100, 1)
        imgSize = 100
        self.prestigeButton.resizeImg(imgSize, imgSize)

        self.spawnTime = 0
        self.enemies = []
        self.spawnInterval = 500

    def update(self, dt, mobTypes, gameState, events):
        self.spawnTime += dt
        if self.spawnTime >= self.spawnInterval:
            chosenType = choice(mobTypes)
            chosenMob = chosenType(self.screenWidth, self.screenPosX, self.screenPosY)
            chosenMob.baseSpeed *= 3
            self.enemies.append(chosenMob)
            self.spawnTime -= self.spawnInterval

        for enemy in self.enemies:
            enemy.update()

        self.enemies = [e for e in self.enemies if e.rect.y < self.screenHeight and e.health > 0]

        for event in events:
             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.prestigeButton.inner.rect.collidepoint(event.pos):
                    gameState = "PRESTIGE"
                    return gameState

        return gameState

    def draw(self, screen):
            for enemy in self.enemies:
                enemy.draw(screen)
            self.titleImage.draw(screen)
            self.startPromptImage.draw(screen)
            self.prestigeButton.draw(screen)

