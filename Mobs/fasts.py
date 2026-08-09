from Mobs.enemy import Enemy

class Fasts(Enemy):
    def __init__(self, screenWidth, screenPosX, screenPosY):
        self.baseSpeed = 4
        self.health = 35
        self.points = 50
        self.width = 30
        self.height = 30
        self.color = "red"

        super().__init__(screenWidth, screenPosX, screenPosY)
