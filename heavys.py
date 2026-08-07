from enemy import Enemy

class Heavys(Enemy):
    def __init__(self, screenWidth):
        self.baseSpeed = 1
        self.health = 150
        self.width = 90
        self.height = 90
        self.color = "purple"
        self.points = 100

        super().__init__(screenWidth)