from imageloader import loadImage
from text import Text

class OverState:
    def __init__(
            self,
            screenWidth,
            screenHeight,
            screenPosX,
            screenPosY,
            score
        ) -> None:
        self.score = score
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenPosX = screenPosX
        self.screenPosY = screenPosY
        self.gameState = "GAMEOVER"
        self.scaleFactor = 1
        self.gameOverImage = loadImage(
            "assets/texts/gameover.png",
            self.scaleFactor,
            self.screenPosX + self.screenWidth // 2,
            self.screenPosY + self.screenHeight // 3
            )
        self.finalScore = Text(
            f"Score: {self.score}",
            self.screenWidth // 2,
            self.gameOverImage.rect.y + 130
            )
        self.startPromptImage = loadImage(
            "assets/texts/pressSpace.png",
            self.scaleFactor,
            self.screenWidth // 2,
            self.screenHeight // 2
            )
        self.lbHeader = Text(
            "---Top Scores---",
            self.screenWidth // 2,
            self.startPromptImage.rect.y + 70
        )
        self.lbTexts = []
        self.returnMenuImage = loadImage(
            "assets/texts/pressLshift.png",
            self.scaleFactor,
            self.screenWidth // 2,
            self.screenHeight - 100
            )

    def updateScore (self, newScore, topScores):
        self.score = newScore
        self.finalScore.update(f"Score: {newScore}")

        self.lbTexts.clear()
        startY = self.lbHeader.rect.y + 50
        lineSpacing = 35

        for i, (name, score) in enumerate(topScores):
            entryStr = f"{i+1}. {name} - {score}"
            entryY = startY + (i * lineSpacing)

            scoreTxt = Text(entryStr, self.screenWidth//2, entryY)
            self.lbTexts.append(scoreTxt)

    def draw (self, screen):
        self.gameOverImage.draw(screen)
        self.finalScore.draw(screen)
        self.lbHeader.draw(screen)

        for scoreTxt in self.lbTexts:
            scoreTxt.draw(screen)

        self.startPromptImage.draw(screen)
        self.returnMenuImage.draw(screen)
