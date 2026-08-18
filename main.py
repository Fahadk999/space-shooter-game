import pygame
from Mobs.enemy import Enemy
from Mobs.fasts import Fasts
from Mobs.heavys import Heavys
from gamestates.menustate import MenuState
from gamestates.playstate import PlayState
from gamestates.overstate import OverState
from database import ScoreDatabase

def main():
    # Screen Resolution
    WIDTH, HEIGHT = 1080, 1080
    GAMEWIDTH, GAMEHEIGHT = 720, 1080
    pygame.init()

    # Game states
    STATEMENU = "MENU"
    STATEPLAY = "PLAY"
    STATEOVER = "OVER"
    gameState = STATEMENU

    # Initializing Basic Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    gameScreen = pygame.Surface((GAMEWIDTH, GAMEHEIGHT))
    gameScreenPosX, gameScreenPosY = 0, 0
    clock = pygame.time.Clock()
    running = True

    # Variables being used
    mobTypes = (Enemy, Fasts, Heavys)

    # State Classes
    # For Menu State
    menuState = MenuState(WIDTH, HEIGHT, 0, 0)
    # For Playing State
    playState = PlayState(GAMEWIDTH, GAMEHEIGHT, gameScreenPosX, gameScreenPosY, WIDTH)
    # For Gameover State
    overState = OverState(WIDTH, HEIGHT, 0, 0, playState.score)
    # Database init
    db = ScoreDatabase()

    # Game loop
    while running:
        dt = clock.tick(60)
        events = pygame.event.get()

        for event in events: 
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
                        playState.resetPlay()
                        gameState = STATEPLAY
                elif gameState == STATEOVER:
                    if event.key == pygame.K_SPACE:
                        playState.resetPlay()
                        gameState = STATEPLAY
                    elif event.key == pygame.K_LSHIFT:
                        gameState = STATEMENU

        screen.fill("grey")
        gameScreen.fill("black")

        # --- PLAYING STATE ---
        if gameState == STATEPLAY:
            keys = pygame.key.get_pressed()
            gameState = playState.update(keys, dt, gameState, events)
            if gameState == STATEOVER:
                db.addScore("PLAYER", playState.score)
                topScores = db.getTopScores(5)
                overState.updateScore(playState.score, topScores)

            playState.draw(gameScreen, screen)
            screen.blit(gameScreen, (gameScreenPosX, gameScreenPosY))
        # --- MENU STATE ---
        elif gameState == STATEMENU:
            gameState = menuState.update(dt, mobTypes)
            menuState.draw(screen)
        # --- GAME OVER STATE ---
        elif gameState == STATEOVER:
            overState.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()