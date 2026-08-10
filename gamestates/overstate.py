from imageloader import loadImage
from text import Text

class OverState:
    def __init__(self, screenWidth, screenHeight, screenPosX, screenPosY) -> None:
        self.score = 0 # this is temp place holder
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.scaleFactor = 1
        self.gameOverImage = loadImage("assets/texts/gameover.png", self.scaleFactor, self.screenWidth // 2, self.screenHeight // 3)
        self.finalScore = Text(f"Score: {self.score}", screenWidth // 2, self.gameOverImage.rect.y + 130)
        self.returnMenuImage = loadImage("assets/texts/pressLshift.png", self.scaleFactor, self.screenHeight // 2, self.screenHeight - 100)
        self.startPromptImage = loadImage("assets/texts/pressSpace.png", self.scaleFactor, self.screenWidth // 2, self.screenHeight // 2)

    def draw (self, screen):
        self.gameOverImage.draw(screen)
        self.startPromptImage.draw(screen)
        self.finalScore.draw(screen)
        self.returnMenuImage.draw(screen)