import pygame
from random import choice
from player import Player
from bullet import Bullet
from enemy import Enemy
from fasts import Fasts
from heavys import Heavys
from text import Text
from button import TextButton
from imageloader import loadImage

def main():
    # Screen Resolution
    WIDTH, HEIGHT = 720, 1080
    pygame.init()

    # Game states
    STATEMENU = "MENU"
    STATEPLAYING = "PLAYING"
    STATEGAMEOVER = "GAMEOVER"
    gameState = STATEMENU

    # Initializing Basic Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    running = True

    # Variables being used
    score = 0
    scoreText = f"Score: {score}"
    spawnInterval = 3000
    minSpawnInterval = 700
    difficultyInterval = 7000
    lastSpawnTime = pygame.time.get_ticks()
    lastDifficultyTime = pygame.time.get_ticks()
    scaleFactor = 1

    # --- Entities and Text classes ---
    # For Menu State
    titleImage = loadImage("assets/texts/title.png", scaleFactor, WIDTH // 2, HEIGHT // 3)
    startPromptImage = loadImage("assets/texts/pressSpace.png", scaleFactor, WIDTH // 2, HEIGHT // 2)
    # upgradeLogo = loadImage("assets/logos/upgradelogo.png", scaleFactor, WIDTH//2, HEIGHT - 100)
    upgradeLogo = TextButton("Upgrade", WIDTH//2, HEIGHT - 100)

    # For Playing State
    player = Player(WIDTH, HEIGHT)
    bullets = []
    playerHealth = Text(player.health, 30, 30)
    scoreDisplay = Text(scoreText, 100, 100)
    enemies = []
    mobTypes = (Enemy, Fasts, Heavys)

    # For Gameover State
    gameOverImage = loadImage("assets/texts/gameover.png", scaleFactor, WIDTH // 2, HEIGHT // 3)
    finalScore = Text(f"Score: {score}", WIDTH // 2, startPromptImage.rect.y + 90)
    returnMenuImage = loadImage("assets/texts/pressLshift.png", scaleFactor, WIDTH // 2, HEIGHT - 100)

    # Reset Game
    def resetGame():
        nonlocal score, spawnInterval, lastSpawnTime, lastDifficultyTime
        player.health = 100
        score = 0
        spawnInterval = 3000
        lastSpawnTime = pygame.time.get_ticks()
        lastDifficultyTime = pygame.time.get_ticks()
        enemies.clear()
        bullets.clear()

    # Game loop
    while running:
        currentTime = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if gameState == STATEPLAYING:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(player.rect.x, player.rect.y, player.width))
                    if event.key == pygame.K_LSHIFT:
                        gameState = STATEMENU  

                elif gameState == STATEMENU:
                    if event.key == pygame.K_SPACE:
                        resetGame() 
                        gameState = STATEPLAYING

                elif gameState == STATEGAMEOVER:
                    if event.key == pygame.K_SPACE:
                        resetGame()
                        gameState = STATEPLAYING
                    elif event.key == pygame.K_LSHIFT:
                        resetGame()
                        gameState = STATEMENU
            upgradeLogo.onClick(event)

        screen.fill("black")

        # --- PLAYING STATE ---
        if gameState == STATEPLAYING:
            keys = pygame.key.get_pressed()
            player.move(keys)

            # Enemy Spawning
            if currentTime - lastSpawnTime >= spawnInterval:
                chosenType = choice(mobTypes)
                enemies.append(chosenType(WIDTH))
                lastSpawnTime = currentTime

            # Difficulty Scaling
            if currentTime - lastDifficultyTime >= difficultyInterval and spawnInterval >= minSpawnInterval:
                spawnInterval -= 100
                spawnInterval = max(minSpawnInterval, spawnInterval)
                lastDifficultyTime = currentTime

            # Movement Updates
            for b in bullets:
                b.move()

            for enemy in enemies:
                enemy.update()
                if enemy.collide(player):
                    playerHealth.update(player.health)

            # Bullet-Enemy Collisions
            for b in bullets:
                for enemy in enemies:
                    if enemy.collide(b):
                        score += enemy.points

            # Clean Up Offscreen/Dead Entities
            bullets = [b for b in bullets if b.rect.y + b.height >= 0 and b.health > 0]
            enemies = [e for e in enemies if e.rect.y < HEIGHT and e.health > 0]

            # Check Game Over State
            if player.health <= 0:
                finalScore.update(f"Score: {score}")
                gameState = STATEGAMEOVER

            # Draw Game Objects
            for enemy in enemies:
                enemy.draw(screen)
            for b in bullets:
                b.draw(screen)

            player.draw(screen)

            # Update and Draw HUD
            scoreText = f"Score: {score}"
            scoreDisplay.update(scoreText)
            playerHealth.update(f"Health: {player.health}")

            playerHealth.draw(screen)
            scoreDisplay.draw(screen)

        # --- MENU STATE ---
        elif gameState == STATEMENU:
            menuSpawnInterval = 500
            if currentTime - lastSpawnTime >= menuSpawnInterval:
                chosenType = choice(mobTypes)
                chosenMob = chosenType(WIDTH)
                chosenMob.baseSpeed *= 3
                enemies.append(chosenMob)
                lastSpawnTime = currentTime

            for enemy in enemies:
                enemy.update()
                enemy.draw(screen)

            titleImage.draw(screen)
            startPromptImage.draw(screen)
            upgradeLogo.draw(screen)
            enemies = [e for e in enemies if e.rect.y < HEIGHT and e.health > 0]

        # --- GAME OVER STATE ---
        elif gameState == STATEGAMEOVER:
            gameOverImage.draw(screen)
            startPromptImage.draw(screen)
            finalScore.draw(screen)
            returnMenuImage.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()