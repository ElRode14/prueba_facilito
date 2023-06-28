import os
import pygame

from .config import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, left, bottom, dir_images):
		#Ejecuto __init__ de calse padre en clase
        pygame.sprite.Sprite.__init__(self)
#Cargo imagen
        self.image = pygame.image.load( os.path.join(dir_images, 'wall.png') )
#Capturo rectángulo de imagen
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

        self.vel_x = SPEED
#rectangulo para evitar que se detenga al chocar arriba
        self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)

    def update(self):
		#Le doy movimiento a la pared para simular el avance del jugador
        self.rect.left -= self.vel_x
#Le doy movimiento a la pared para simular el avance del jugador para el rectanulo de arriba
        self.rect_top.x = self.rect.x

    def stop(self):
        self.vel_x = 0
