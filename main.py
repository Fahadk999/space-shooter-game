import pygame
from random import choice
from player import Player
from bullet import Bullet
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys
from text import Text
from button import ImageButton, TextButton
from imageloader import loadImage
from gamestates.menustate import MenuState
from gamestates.playstate import PlayState

def main():
    # Screen Resolution
    WIDTH, HEIGHT = 1080, 1080
    GAMEWIDTH, GAMEHEIGHT = 720, 1080
    pygame.init()

    # Game states
    STATEMENU = "MENU"
    STATEPLAY = "PLAYING"
    STATEOVER = "GAMEOVER"
    STATEUPGRADE = "UPGRADE"
    gameState = STATEMENU

    # Initializing Basic Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    gameScreen = pygame.Surface((GAMEWIDTH, GAMEHEIGHT))
    gameScreenPosX, gameScreenPosY = 0, 0
    clock = pygame.time.Clock()
    running = True

    # Variables being used
    score = 0
    statPoints = 0
    mobTypes = (Enemy, Fasts, Heavys)

    # --- Entities and Text classes ---
    # For Menu State
    menuState = MenuState(WIDTH, HEIGHT, 0, 0)

    # For Playing State
    playState = PlayState(GAMEWIDTH, GAMEHEIGHT, gameScreenPosX, gameScreenPosY)

    # For Gameover State
    # gameOverImage = loadImage("assets/texts/gameover.png", scaleFactor, WIDTH // 2, HEIGHT // 3)
    # finalScore = Text(f"Score: {score}", WIDTH // 2, startPromptImage.rect.y + 90)
    # returnMenuImage = loadImage("assets/texts/pressLshift.png", scaleFactor, WIDTH // 2, HEIGHT - 100)

    # Reset Game
    # def resetGame():
        # nonlocal reloadTime, score, spawnInterval, lastSpawnTime, lastDifficultyTime
        # reloadTime = player.reload
        # player.resetHealth()
        # score = 0
        # spawnInterval = 3000
        # lastSpawnTime = pygame.time.get_ticks()
        # lastDifficultyTime = pygame.time.get_ticks()
        # enemies.clear()
        # bullets.clear()
    def updateStat (stat, changeValue) -> int:
        return stat + changeValue

    # Game loop
    while running:
        currentTime = pygame.time.get_ticks()
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if gameState == STATEPLAY:
                    if event.key == pygame.K_LSHIFT:
                        gameState = STATEMENU  

                elif gameState == STATEMENU:
                    if event.key == pygame.K_SPACE:
                        # resetGame() 
                        gameState = STATEPLAY

                elif gameState == STATEOVER:
                    if event.key == pygame.K_SPACE:
                        # resetGame()
                        gameState = STATEPLAY
                    elif event.key == pygame.K_LSHIFT:
                        # resetGame()
                        gameState = STATEMENU
            # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # if gameState == STATEMENU:
                    # if upgradeLogo.inner.rect.collidepoint(event.pos):
                        # gameState = STATEUPGRADE
                        # player.maxHealth = upgradeLogo.onClick(updateStat, player.maxHealth, 100)

        screen.fill("white")
        gameScreen.fill("black")
        screen.blit(gameScreen, (gameScreenPosX, gameScreenPosY))

        # --- PLAYING STATE ---
        if gameState == STATEPLAY:
            keys = pygame.key.get_pressed()
            playState.update(keys, dt)
            playState.draw(screen)

        # --- MENU STATE ---
        elif gameState == STATEMENU:
            menuState.update(dt, mobTypes)
            menuState.draw(screen)

        # --- GAME OVER STATE ---
        # elif gameState == STATEOVER:
            # gameOverImage.draw(screen)
            # startPromptImage.draw(screen)
            # finalScore.draw(screen)
            # returnMenuImage.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()