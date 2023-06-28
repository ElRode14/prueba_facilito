import pygame

from .config import *

#Defino clase que hereda de Sprite de Pygame
class Platform(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
#Genero una superficie y le asigno color verde
        self.image = pygame.Surface( (WIDTH, 40) )
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - 40
