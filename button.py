import pygame
from imageloader import loadImage
from text import Text

class TextButton:
    def __init__(self, text, posX, posY):
        self.text = Text(text, posX, posY)

    def draw (self, screen):
        self.text.draw(screen)

    def onClick (self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.text.rect.collidepoint(event.pos):
                print("clicked")
            print("clicked outside") 



