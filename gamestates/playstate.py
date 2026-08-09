import pygame
from random import choice
from player import Player
from bullet import Bullet
from text import Text
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys

class PlayState:
    def __init__(self, screenWidth, screenHeight, screenPosX, screenPosY) -> None:
        self.score = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY
        self.scoreText = f"Score: {self.score}"
        self.player = Player(self.screenWidth, self.screenHeight)
        self.bullets = []
        self.playerHealth = Text(self.player.health, 30, 30)
        self.scoreDisplay = Text(self.scoreText, 100, 100)
        self.enemies = []
        self.mobTypes = (Enemy, Fasts, Heavys)
        self.shootTime = 0
        self.spawnTime = 0
        self.difficultyTime = 0
        self.spawnInterval = 3000
        self.reloadTime = self.player.reload
        self.spawnInterval = 700
        self.difficultyInterval = 7000

    def update (self, keys, dt):
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
            spawnInterval = max(self.spawnInterval, self.spawnInterval)
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
#         if self.player.health <= 0:
#             # finalScore.update(f"Score: {score}")
#             currState = STATEOVER

        scoreText = f"Score: {self.score}"
        self.scoreDisplay.update(scoreText)
        self.playerHealth.update(f"Health: {self.player.health}")


    def draw (self, screen):
        # Draw Game Objects
        for enemy in self.enemies:
            enemy.draw(screen)
        for b in self.bullets:
            b.draw(screen)

        self.player.draw(screen)

        self.playerHealth.draw(screen)
        self.scoreDisplay.draw(screen)
