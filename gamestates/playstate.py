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
from soundloader import LoadSound

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
        self.reloadRateDec = 200
        self.bltSpdRateInc = 1
        self.bltDmgInc = 0
        self.bltSpdInc = 0
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY
        self.enemyHealthBuffs = 0
        self.healthLvl = 0
        self.reloadLvl = 0
        self.bulletDmgLvl = 0
        self.bulletSpeedLvl = 0
        self.regenLvl = 0

        # Objects For Gamescreen
        self.creditString = f"credit: {self.credit}"
        self.scoreString = f"score: {int(self.score)}"
        self.player = Player(self.screenWidth, self.screenHeight)
        self.bullets = []
        self.playerHealth = Text(self.player.health, 90, 30)
        self.creditDisplay = Text(self.creditString, screenWidth-100, 30)

        # Sound Effects
        self.laserSound = LoadSound("audio/laserSmall.wav", 0.3)
        self.enemyHitSound = LoadSound("audio/explosion.wav", 0.1)
        self.upgradeSound = LoadSound("audio/upgrade.wav", 0.1)
        self.playerHitSound = LoadSound("audio/explosion2.wav", 0.1)

        self.enemies = []
        self.mobTypes = (Enemy, Fasts, Heavys)
        
        # Objects For Upgrade Side
        offsetBtn = -55
        offsetLvl = -15
        self.costTxt = Text(f"Cost: {self.cost}", screenWidth+85, 20)
        self.scoreTxt = Text(self.scoreString, screenWidth//2, 30)
        self.healthUpTxt = Text("Health", screenWidth+65, 60)
        self.healthUpBtn = TextButton("+", mainScreenWidth+offsetBtn, 60)
        self.healthLvlTxt = Text(str(self.healthLvl), mainScreenWidth+offsetLvl, 62)

        self.reloadUpTxt = Text("Reload", screenWidth+66, 100)
        self.reloadUpBtn = TextButton("+", mainScreenWidth+offsetBtn, 100)
        self.reloadLvlTxt = Text(str(self.reloadLvl), mainScreenWidth+offsetLvl, 102)

        self.bulletDmgTxt = Text("Bullet Damage", screenWidth+127, 140)
        self.bulletDmgBtn = TextButton("+", mainScreenWidth+offsetBtn, 140)
        self.bulletDmgLvlTxt = Text(str(self.bulletDmgLvl), mainScreenWidth+offsetLvl, 142)

        self.bulletSpdTxt = Text("Bullet Speed", screenWidth+112, 180)
        self.bulletSpdBtn = TextButton("+", mainScreenWidth+offsetBtn, 180)
        self.bulletSpdLvlTxt = Text(str(self.bulletSpeedLvl), mainScreenWidth+offsetLvl, 182)

        self.guideTxt = Text("Use Buttons 1-4\nor click the + to\nupgrade your stats!", screenWidth+180, screenHeight-100)
        
        # Timers
        self.regenTimer = 0
        self.shootTime = 0
        self.spawnTime = 0
        self.difficultyTime = 0
        self.enemyStrongTimer = 0
        self.spawnInterval = 3000
        self.enemyStrongInterval = 15000
        self.regenInterval = 10000
        self.reloadTime = self.player.reload
        self.minReload = 50
        self.minSpawnInterval = 300
        self.difficultyInterval = 3000

    def applyUpgrade(self, incVal, lvl):
        self.credit -= self.cost
        self.cost = floor(self.cost * (self.rate + self.rateInc))
        self.costTxt.update(f"Cost: {self.cost}")
        self.upgradeSound.play()
        return incVal * (lvl + 1)

    def upgradeHealth(self):
        boost = self.applyUpgrade(100, self.healthLvl)
        self.player.maxHealth += boost
        self.player.health += boost
        self.healthLvl += 1
        self.healthLvlTxt.update(str(self.healthLvl))

    def upgradeReload(self):
        if self.reloadTime > self.minReload:
            reduction = self.applyUpgrade(self.reloadRateDec, self.reloadLvl)
            self.reloadTime = max(self.minReload, self.reloadTime - reduction)
            self.player.reload = self.reloadTime
            self.reloadLvl += 1
            self.reloadLvlTxt.update(str(self.reloadLvl))

    def upgradeDamage(self):
        self.bltDmgInc += self.applyUpgrade(self.bltDmgRateInc, self.bulletDmgLvl)
        self.bulletDmgLvl += 1
        self.bulletDmgLvlTxt.update(str(self.bulletDmgLvl))

    def upgradeSpeed(self):
        self.bltSpdInc += self.applyUpgrade(self.bltSpdRateInc, self.bulletSpeedLvl)
        self.bulletSpeedLvl += 1
        self.bulletSpdLvlTxt.update(str(self.bulletSpeedLvl))

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
                )
            )
            self.laserSound.play()
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
                self.playerHitSound.play()
                self.regenTimer -= self.regenInterval
                self.credit += enemy.points
                self.score += enemy.points * 2 
                self.playerHealth.update(self.player.health)

        # Bullet-Enemy Collisions 
        for b in self.bullets:
            for enemy in self.enemies:
                if enemy.collide(b):
                    self.enemyHitSound.play()
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
            self.player.health = min(self.player.health + self.regenVal, self.player.maxHealth)
            self.regenTimer -= self.regenInterval

        creditString = f"credit: {self.credit}"
        self.creditDisplay.update(creditString)
        self.playerHealth.update(f"Health: {self.player.health}")

        # Upgrading Event Handling
        for event in events:
            if self.credit >= self.cost:
                # KEYBOARD SHORTCUTS
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.upgradeHealth()
                    elif event.key == pygame.K_2:
                        self.upgradeReload()
                    elif event.key == pygame.K_3:
                        self.upgradeDamage()
                    elif event.key == pygame.K_4:
                        self.upgradeSpeed()

                # MOUSE CLICKS
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.healthUpBtn.inner.rect.collidepoint(event.pos):
                        self.upgradeHealth()
                    elif self.reloadUpBtn.inner.rect.collidepoint(event.pos):
                        self.upgradeReload()
                    elif self.bulletDmgBtn.inner.rect.collidepoint(event.pos):
                        self.upgradeDamage()
                    elif self.bulletSpdBtn.inner.rect.collidepoint(event.pos):
                        self.upgradeSpeed()
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
        self.healthLvlTxt.draw(mainScreen)
        self.healthUpBtn.draw(mainScreen)
        self.reloadUpTxt.draw(mainScreen)
        self.reloadUpBtn.draw(mainScreen)
        self.reloadLvlTxt.draw(mainScreen)
        self.bulletDmgBtn.draw(mainScreen)
        self.bulletDmgTxt.draw(mainScreen)
        self.bulletDmgLvlTxt.draw(mainScreen)
        self.bulletSpdTxt.draw(mainScreen)
        self.bulletSpdBtn.draw(mainScreen)
        self.bulletSpdLvlTxt.draw(mainScreen)

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
        
        self.healthLvl = 0
        self.reloadLvl = 0
        self.bulletDmgLvl = 0
        self.bulletSpeedLvl = 0
        self.regenLvl = 0

        self.healthLvlTxt.update("0")
        self.reloadLvlTxt.update("0")
        self.bulletDmgLvlTxt.update("0")
        self.bulletSpdLvlTxt.update("0")