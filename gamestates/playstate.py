import pygame
from math import floor
from random import choice
from player import Player
from bullet import Bullet
from text import Text
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys
from button import TextButton

# adding rounds next, every round is 20 sec, then boss fight

class PlayState:
    def __init__(
            self,
            screenWidth,
            screenHeight,
            screenPosX,
            screenPosY,
            mainScreenWidth,
        ) -> None:
        self.credit = 0
        self.score = 0
        self.scoreMultiplier = 10 
        self.cost = 100
        self.regenVal = 15
        self.rate = 1
        self.rateInc = 0.25
        self.bltDmgRateInc = 20
        self.bltSpdRateInc = 1
        self.bltDmgInc = 0
        self.bltSpdInc = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY

        self.enemyHealthBuffs = 0

        # Objects For Gamescreen
        self.creditString = f"credit: {self.credit}"
        self.scoreString = f"score: {int(self.score)}"
        self.player = Player(self.screenWidth, self.screenHeight)
        self.bullets = []
        self.playerHealth = Text(self.player.health, 90, 30)
        self.creditDisplay = Text(self.creditString, screenWidth-100, 30)

        self.enemies = []
        self.mobTypes = (Enemy, Fasts, Heavys)
        
        # Objects For Upgrade Side
        offsetBtn = -25
        self.costTxt = Text(f"Cost: {self.cost}", screenWidth+85, 20)
        self.scoreTxt = Text(self.scoreString, screenWidth//2, 30)
        self.healthUpTxt = Text("Health", screenWidth+65, 60)
        self.healthUpBtn = TextButton("+", mainScreenWidth+offsetBtn, 60)
        self.reloadUpTxt = Text("Reload", screenWidth+66, 100)
        self.reloadUpBtn = TextButton("+", mainScreenWidth+offsetBtn, 100)
        self.bulletDmgTxt = Text("Bullet Damage", screenWidth+127, 140)
        self.bulletDmgBtn = TextButton("+", mainScreenWidth+offsetBtn, 140)
        self.bulletSpdTxt = Text("Bullet Speed", screenWidth+112, 180)
        self.bulletSpdBtn = TextButton("+", mainScreenWidth+offsetBtn, 180)
        self.guideTxt = Text("Use Buttons 1-4\nor click the + to\nupgrade your stats!", screenWidth+180, screenHeight-100)
        
        # Timers
        self.regenTimer = 0
        self.shootTime = 0
        self.spawnTime = 0
        self.difficultyTime = 0
        self.enemyStrongTimer = 0
        self.spawnInterval = 3000
        self.enemyStrongInterval = 10000
        self.regenInterval = 5000
        self.reloadTime = self.player.reload
        self.minReload = 50
        self.minSpawnInterval = 300
        self.difficultyInterval = 3000

    def update(self, keys, dt, gameState, events):
        self.score += (dt / 1000) * self.scoreMultiplier
        self.scoreTxt.update(f"score: {int(self.score)}")

        self.spawnTime += dt
        self.shootTime += dt
        self.difficultyTime += dt
        self.enemyStrongTimer += dt  
        self.regenTimer += dt

        if self.shootTime > self.reloadTime:
            self.shootTime = self.reloadTime
        self.player.move(keys)

        # Shooting
        if self.shootTime >= self.reloadTime:
            self.bullets.append(
                Bullet(
                    self.player.rect.x,
                    self.player.rect.y,
                    self.player.width,
                    self.bltDmgInc,
                    self.bltSpdInc
                ))
            self.shootTime = 0

        # Enemy Strength Up 
        if self.enemyStrongTimer >= self.enemyStrongInterval:
            self.enemyStrongTimer -= self.enemyStrongInterval
            self.enemyHealthBuffs += 1  

            for e in self.enemies:
                e.healthUp()

        # Enemy Spawning
        if self.spawnTime >= self.spawnInterval:
            chosenType = choice(self.mobTypes)
            newEnemy = chosenType(self.screenWidth, self.screenPosX, self.screenPosY)

            for _ in range(self.enemyHealthBuffs):
                newEnemy.healthUp()

            self.enemies.append(newEnemy)
            self.spawnTime -= self.spawnInterval

        # Difficulty Scaling
        if self.difficultyTime >= self.difficultyInterval:
            self.spawnInterval -= 100
            self.spawnInterval = max(self.minSpawnInterval, self.spawnInterval)
            self.difficultyTime -= self.difficultyInterval

        # Movement Updates
        for b in self.bullets:
            b.move()

        for enemy in self.enemies:
            enemy.update()
            if enemy.collide(self.player):
                self.credit += enemy.points
                self.score += enemy.points * 2 
                self.playerHealth.update(self.player.health)

        # Bullet-Enemy Collisions 
        for b in self.bullets:
            for enemy in self.enemies:
                if enemy.collide(b):
                    self.credit += enemy.points
                    self.score += enemy.points * 2 

        # Clean Up Offscreen/Dead Entities
        self.bullets = [b for b in self.bullets if b.rect.y + b.height >= 0 and b.health > 0]
        self.enemies = [e for e in self.enemies if e.rect.y < self.screenHeight and e.health > 0]

        # Check Game Over State
        if self.player.health <= 0:
            gameState = "OVER"
            return gameState

        # Player Health Regen
        if self.regenTimer >= self.regenInterval:
            self.player.health = min(self.player.health+self.regenVal, self.player.maxHealth)
            self.regenTimer -= self.regenInterval



        creditString = f"credit: {self.credit}"
        self.creditDisplay.update(creditString)
        self.playerHealth.update(f"Health: {self.player.health}")

        # Upgrading
        def applyUpgrade(incVal):
            self.credit -= self.cost
            self.cost = floor(self.cost * (self.rate + self.rateInc))
            self.costTxt.update(f"Cost: {self.cost}")
            return incVal

        for event in events:
            if self.credit >= self.cost:
                # KEYBOARD SHORTCUTS
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player.maxHealth += applyUpgrade(100)
                        self.player.health += 100
                    elif event.key == pygame.K_2 and self.reloadTime > self.minReload:
                        self.reloadTime = max(self.minReload, self.reloadTime - applyUpgrade(100))
                        self.player.reload = self.reloadTime
                    elif event.key == pygame.K_3:
                        self.bltDmgInc += applyUpgrade(self.bltDmgRateInc)
                    elif event.key == pygame.K_4:
                        self.bltSpdInc += applyUpgrade(self.bltSpdRateInc)

                # MOUSE CLICKS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.healthUpBtn.inner.rect.collidepoint(event.pos):
                        self.player.maxHealth += applyUpgrade(100)
                        self.player.health += 100
                    elif self.reloadUpBtn.inner.rect.collidepoint(event.pos) and self.reloadTime > self.minReload:
                        self.reloadTime = max(self.minReload, self.reloadTime - applyUpgrade(100))
                        self.player.reload = self.reloadTime
                    elif event.bulletDmgBtn.inner.rect.collidepoint(event.pos) if hasattr(event, 'bulletDmgBtn') else self.bulletDmgBtn.inner.rect.collidepoint(event.pos):
                        self.bltDmgInc += applyUpgrade(self.bltDmgRateInc)
                    elif self.bulletSpdBtn.inner.rect.collidepoint(event.pos):
                        self.bltSpdInc += applyUpgrade(self.bltSpdRateInc)
        return gameState

    def draw(self, gameScreen, mainScreen):
        # Draw Game Objects
        for enemy in self.enemies:
            enemy.draw(gameScreen)
        for b in self.bullets:
            b.draw(gameScreen)

        self.player.draw(gameScreen)

        self.playerHealth.draw(gameScreen)
        self.creditDisplay.draw(gameScreen)
        self.scoreTxt.draw(gameScreen)

        # Drawing Update Objects
        self.costTxt.draw(mainScreen)
        self.healthUpTxt.draw(mainScreen)
        self.healthUpBtn.draw(mainScreen)
        self.reloadUpTxt.draw(mainScreen)
        self.reloadUpBtn.draw(mainScreen)
        self.bulletDmgBtn.draw(mainScreen)
        self.bulletDmgTxt.draw(mainScreen)
        self.bulletSpdTxt.draw(mainScreen)
        self.bulletSpdBtn.draw(mainScreen)

        self.guideTxt.draw(mainScreen)

    def resetPlay(self):
        self.player.resetPlayer()
        self.credit = 0
        self.score = 0
        self.shootTime = 0
        self.spawnTime = 0
        self.bltDmgInc = 0
        self.bltSpdInc = 0
        self.difficultyTime = 0
        self.enemyStrongTimer = 0
        self.regenTimer = 0
        self.enemyHealthBuffs = 0 
        self.spawnInterval = 3000
        self.reloadTime = self.player.reload
        self.difficultyInterval = 3000
        self.enemies.clear()
        self.bullets.clear()
        self.cost = 100
        self.costTxt.update(f"Cost: {self.cost}")
        self.scoreTxt.update("score: 0")