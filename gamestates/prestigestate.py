from text import Text

class PrestigeState:
    def __init__(self, width, height) -> None:
        self.bulletWidthTxt = Text("Bullet Width", 100, 100)
        self.tankSizeTxt = Text("Tank Size", 100, 150)

    def draw (self, mainScreen):
        self.bulletWidthTxt.draw(mainScreen)
        self.tankSizeTxt.draw(mainScreen)

    def update (self, dt, events):
        pass