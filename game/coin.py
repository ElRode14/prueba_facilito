import os
import pygame

from .config import *

class Coin(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, dir_images):
		#ejecuto clase __init__ del padre
        pygame.sprite.Sprite.__init__(self)
#Genero la moneda
        self.image = pygame.image.load( os.path.join(dir_images, 'coin.png') )
#Obtengo el rectangulo de la imagen
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.vel_x = SPEED

    def update(self):
		#actualizo posición en x
        self.rect.left -= self.vel_x

    def stop(self):
        self.vel_x = 0
