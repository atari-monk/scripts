import time
import sys
sys.stdout = open("NUL", "w")
import pygame
sys.stdout = sys.__stdout__

class SoundPlayer:
    def __init__(self, sound):
        self.sound = sound

    def play(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play()
        time.sleep(10)
        pygame.mixer.music.stop()