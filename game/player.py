import os
import pygame

from .config import *

#Genero 
class Player(pygame.sprite.Sprite):
#Ejecuto método __init__ de la clase padre
    def __init__(self, left, bottom, dir_images):
        pygame.sprite.Sprite.__init__(self)

        self.images = (
            pygame.image.load( os.path.join(dir_images, 'player1.png') ),
            pygame.image.load( os.path.join(dir_images, 'jump.png') ),
        )

        self.image = self.images[0]

        self.rect = self.image.get_rect()
        #Les asigno posición al jugador
        self.rect.left = left
        self.rect.bottom = bottom

        self.pos_y = self.rect.bottom
        self.vel_y = 0

        self.can_jump = False
#Habilita saltar
        self.playing = True

    def collide_with(self, sprites):
		#Detecto coliciones entre el jugador y resto de los elementos
		#Los parámetros son sprite a evaluar (jugador), segundo la lista de sprites, tercero queda falso
		#Capturo objetos con los que colicionó
        objects = pygame.sprite.spritecollide(self, sprites, False)
        #Devuelvo que objeto fue contra el que colicionó
        if objects:
            return objects[0]

    def collide_bottom(self, wall):
        return self.rect.colliderect(wall.rect_top)
#me permite caminar y saltar desde arriba de la pared
    def skid(self, wall):
        self.pos_y = wall.rect.top
        self.vel_y = 0
        self.can_jump = True
#Vuelvo a la imagen origina cuando coliciono arriba
        self.image = self.images[0]

    def validate_platform(self, platform):
		#Verifico coliciones con el jugador
        result = pygame.sprite.collide_rect(self, platform)
        if result:
            self.vel_y = 0
            self.pos_y = platform.rect.top
            #Permito que vuelva a saltar
            self.can_jump = True
#Vuelvo a la imagen origina cuando coliciono 
            self.image = self.images[0]

    def jump(self):
		#Actualizo la acsceleración del jugador
        if self.can_jump:
            self.vel_y = -23
            #Imposibilito que vuelva a saltar 
            self.can_jump = False
#cambio la imagen al saltar
            self.image = self.images[1]

    def update_pos(self):
		#Asceleración en Y del jugador
        self.vel_y += PLAYER_GRAV
        self.pos_y += self.vel_y + 0.5 * PLAYER_GRAV

    def update(self):
		#actualiza posición solamente si no colicionó
        if self.playing:
            self.update_pos()
#ACTUALIZO la posición en Y en pantalla del jugados
            self.rect.bottom = self.pos_y

    def stop(self):
#No me deja volver a saltar si colicionó con pared
        self.playing = False
