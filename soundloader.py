import pygame
from utils import resource_path

class LoadSound:
    def __init__(self, path, vol=1.0) -> None:
        self.fullPath = resource_path(path)
        self.soundSfx = pygame.mixer.Sound(self.fullPath)
        self.soundSfx.set_volume(vol)

    def play(self):
        self.soundSfx.play()

    def setVolume(self, vol):
        self.soundSfx.set_volume(vol)

class LoadMusic:
    def __init__(self, path, vol=0.3) -> None:
        self.fullPath = resource_path(path)
        self.vol = vol

    def play(self, loops=-1):
        pygame.mixer.music.load(self.fullPath)
        pygame.mixer.music.set_volume(self.vol)
        pygame.mixer.music.play(loops=loops)

    def stop(self):
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()