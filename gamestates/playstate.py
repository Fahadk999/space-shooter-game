import pygame
from random import choice
from player import Player
from bullet import Bullet
from text import Text
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys
from button import TextButton


class PlayState:
    def __init__(self, screenWidth, screenHeight, screenPosX, screenPosY) -> None:
        self.score = 0
        self.gameState = "PLAY"
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY

        # Objects For Gamescreen
        self.scoreText = f"Score: {self.score}"
        self.player = Player(self.screenWidth, self.screenHeight)
        self.bullets = []
        self.playerHealth = Text(self.player.health, 30, 30)
        self.scoreDisplay = Text(self.scoreText, 100, 100)
        self.enemies = []
        self.mobTypes = (Enemy, Fasts, Heavys)
        # Objects For Upgrade Side
        self.healthUpTxt = Text("Health", 65+screenWidth, 50)
        self.healthUpBtn = TextButton("+", screenWidth+150, 50)
        # Timers
        self.shootTime = 0
        self.spawnTime = 0
        self.difficultyTime = 0
        self.spawnInterval = 3000
        self.reloadTime = self.player.reload
        self.spawnInterval = 1000
        self.difficultyInterval = 7000

    def update (self, keys, dt, gameState):
        self.spawnTime += dt
        self.shootTime += dt
        self.difficultyTime += dt
        self.player.move(keys)

        # Shooting
        if self.shootTime >= self.reloadTime:
            if keys[pygame.K_SPACE]:
                self.bullets.append(Bullet(self.player.rect.x, self.player.rect.y, self.player.width))
                self.shootTime -= self.reloadTime

        # Enemy Spawning
        if self.spawnTime >= self.spawnInterval:
            chosenType = choice(self.mobTypes)
            self.enemies.append(chosenType(self.screenWidth, self.screenPosX, self.screenPosY))
            self.spawnTime -= self.spawnInterval

        # Difficulty Scaling
        if self.difficultyTime >= self.difficultyInterval:
            self.spawnInterval -= 100
            self.spawnInterval = max(self.spawnInterval, self.spawnInterval)
            self.difficultyTime -= self.difficultyInterval

        # Movement Updates
        for b in self.bullets:
            b.move()

        for enemy in self.enemies:
            enemy.update()
            if enemy.collide(self.player):
                self.playerHealth.update(self.player.health)
                self.score += enemy.points

        # Bullet-Enemy Collisions
        for b in self.bullets:
            for enemy in self.enemies:
                if enemy.collide(b):
                    self.score += enemy.points

        # Clean Up Offscreen/Dead Entities
        self.bullets = [b for b in self.bullets if b.rect.y + b.height >= 0 and b.health > 0]
        self.enemies = [e for e in self.enemies if e.rect.y < self.screenHeight and e.health > 0]

        # Check Game Over State
        if self.player.health <= 0:
            gameState = "OVER"
            return gameState

        scoreText = f"Score: {self.score}"
        self.scoreDisplay.update(scoreText)
        self.playerHealth.update(f"Health: {self.player.health}")
        return gameState


    def draw (self, gameScreen, mainScreen):
        # Draw Game Objects
        for enemy in self.enemies:
            enemy.draw(gameScreen)
        for b in self.bullets:
            b.draw(gameScreen)

        self.player.draw(gameScreen)

        self.playerHealth.draw(gameScreen)
        self.scoreDisplay.draw(gameScreen)
        # Drawing Update Objects
        self.healthUpTxt.draw(mainScreen)
        self.healthUpBtn.draw(mainScreen)

    def resetPlay (self):
        self.player.resetPlayer()
        self.score = 0
        self.shootTime = 0
        self.spawnTime = 0
        self.difficultyTime = 0
        self.spawnInterval = 3000
        self.reloadTime = self.player.reload
        self.spawnInterval = 700
        self.difficultyInterval = 17000
        self.enemies.clear()
        self.bullets.clear()
