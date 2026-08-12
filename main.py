import pygame
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys
from gamestates.menustate import MenuState
from gamestates.playstate import PlayState
from gamestates.overstate import OverState

def main():
    # Screen Resolution
    WIDTH, HEIGHT = 1080, 1080
    GAMEWIDTH, GAMEHEIGHT = 720, 1080
    pygame.init()

    # Game states
    STATEMENU = "MENU"
    STATEPLAY = "PLAY"
    STATEOVER = "OVER"
    # STATEUPGRADE = "UPGRADE"
    gameState = STATEMENU

    # Initializing Basic Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    gameScreen = pygame.Surface((GAMEWIDTH, GAMEHEIGHT))
    gameScreenPosX, gameScreenPosY = 0, 0
    clock = pygame.time.Clock()
    running = True

    # Variables being used
    mobTypes = (Enemy, Fasts, Heavys)

    # --- Entities and Text classes ---
    # For Menu State
    menuState = MenuState(WIDTH, HEIGHT, 0, 0)

    # For Playing State
    playState = PlayState(GAMEWIDTH, GAMEHEIGHT, gameScreenPosX, gameScreenPosY)

    # For Gameover State
    overState = OverState(GAMEWIDTH, GAMEHEIGHT, gameScreenPosX, gameScreenPosY)

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

    # Game loop
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if gameState == STATEPLAY:
                    if event.key == pygame.K_LSHIFT:
                        playState.resetPlay()
                        gameState = STATEMENU  
                elif gameState == STATEMENU:
                    if event.key == pygame.K_SPACE:
                        gameState = STATEPLAY
                elif gameState == STATEOVER:
                    if event.key == pygame.K_SPACE:
                        gameState = STATEPLAY
                    elif event.key == pygame.K_LSHIFT:
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
        elif gameState == STATEOVER:
            overState.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()