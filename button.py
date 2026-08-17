import pygame
from imageloader import loadImage
from text import Text

class Button:
    def __init__(self, posX, posY, width=30, height=30) -> None:
        self.rect = pygame.Rect(
            posX,
            posY,
            width,
            height
        )
        self.color = "blue"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def onClick (self, func, *args):
        return func(*args)

    def resize (self, width, height):
        self.rect.width = width
        self.rect.height = height

class TextButton(Button):
    def __init__(self, text, posX, posY):
        super().__init__(posX, posY)
        self.inner = Text(text, posX, posY)

    def draw (self, screen):
        self.inner.draw(screen)

class ImageButton(Button):
    def __init__(self, path, posX, posY, scale = 2):
        super().__init__(posX, posY)
        self.inner = loadImage(path, scale, posX, posY)

    def draw (self, screen):
        self.inner.draw(screen)

    def resizeImg(self, width, height):
        self.inner.resize(width, height)