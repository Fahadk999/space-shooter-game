import pygame
from imageloader import loadImage
from text import Text

class TextButton:
    def __init__(self, text, posX, posY):
        self.inner = Text(text, posX, posY)

    def draw (self, screen):
        self.inner.draw(screen)

    def onClick (self, function):
        function()

class ImageButton:
    def __init__(self, path, posX, posY):
        self.inner = loadImage(path, 2, posX, posY)

    def draw (self, screen):
        self.inner.draw(screen)

    def onClick (self, function):
        function()



