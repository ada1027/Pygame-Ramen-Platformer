import pygame

platforms = []
screen = pygame.display.set_mode((720, 360))

class Platform:
    def __init__(self):
        self.image = pygame.image.load('images/platform.png')

    
    def draw(self, x, y, length):
          for blocks in range(0, length):
              x_real = x + blocks * 16
              
              platforms.append((x_real,y))
              screen.blit(self.image, (x_real, y))