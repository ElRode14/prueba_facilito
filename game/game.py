import os
import sys
import pygame
import random

from .config import * #Importo configuracinoes de archivo config.py
from .platform import Platform #importo la plataforme desde archivo platform.py
from .player import Player
from .wall import Wall
from .coin import Coin

#Clase principal
class Game:
    def __init__(self):
        pygame.init()
        #Genero la pantalla
        self.surface = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE) #Tittulo

        #Autoejecuta
        self.running = True

        self.clock = pygame.time.Clock()
#cargo fuentes para mostrar el score
        self.font = pygame.font.match_font(FONT)
#obtengo las rutas donde se encuentran los archivos
        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, 'sources/sounds')
        self.dir_images = os.path.join(self.dir, 'sources/sprites')

    def start(self):
		#Cuando arranco el juego muestro el menú
        self.menu()
        self.new()

    def new(self):
		#Puntuador
        self.score = 0
        #Nivel inicial
        self.level = 0
#Permito que salte y corran actualizaciones de posición
        self.playing = True
        self.background = pygame.image.load( os.path.join(self.dir_images, 'background.png') )

        self.generate_elements()
        self.run()

    def generate_elements(self):
		#genero la plataforma
        self.platform = Platform()
        #Ubico al jugador sobre la plataforma
        self.player = Player(100, self.platform.rect.top - 200, self.dir_images)

        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        #Genero monedas
        self.coins = pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.player)
#Vuelcvo a generar paredes cuando no hay más en pantalla
        self.generate_walls()

    def generate_walls(self):
#Posición mínima 
        last_position = WIDTH + 100
#si no existen paredes las creo
        if not len(self.walls) > 0:
#Cantidad de paredes que generaré
            for w in range(0, MAX_WALLS):
#Le asigno posición aleatorea a la posición X
                left = random.randrange(last_position + 200, last_position + 400)
                wall = Wall(left, self.platform.rect.top, self.dir_images)
#actualizo la posición de la pared
                last_position = wall.rect.right
#Agrego las paredes al sprite
                self.sprites.add(wall)
                self.walls.add(wall)
#Aumento el nivel y genero más moneras
            self.level += 1
            self.generate_coins()
#Función para generar monedas
    def generate_coins(self):
        last_position = WIDTH + 100

        for c in range(0, MAX_COINS):
            pos_x = random.randrange(last_position + 180, last_position + 300)

            coin = Coin(pos_x, 100, self.dir_images)

            last_position = coin.rect.right

            self.sprites.add(coin)
            self.coins.add(coin)

    def run(self):
		#Verifico que esté corriendo y eventos
        while self.running:
			#Frames por segundo del juego (velocidad)
            self.clock.tick(FPS)
            self.events()
            self.update()
#Me aseguro que draw esté al final para que no queden "ocultos" los textos
            self.draw()

    def events(self):
		#Capturo los diferentes eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
#Controlo la presión de teclas
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
			#Ejecuto la actualización de asceleración
            self.player.jump()
#Si presiono la tecla R y ya perdí ejecuta el juego de nuevo
        if key[pygame.K_r] and not self.playing:
            self.new()

    def draw(self):
#Le asigno a la superficie un color de fondo
        self.surface.blit(self.background, (0, 0))

        self.draw_text()
#Dibujo los sprites en la superficie de la pantalla
        self.sprites.draw(self.surface)

        pygame.display.flip()

    def update(self):
        if not self.playing:
            return
#Ejecuto metodo para verificar control de colición
        wall = self.player.collide_with(self.walls)
#Evaluo resultado de metodo colición con pared
        if wall:
			#Evaluo si la colición fue de frente o base del jugador
            if self.player.collide_bottom(wall):
                self.player.skid(wall)
            else:
                self.stop()

        coin = self.player.collide_with(self.coins)
        if coin:
			#Sumo 1 al score y elinino la moneda al colicionar
            self.score += 1
            coin.kill()
#Reproduzco sonido al colicionar con una moneda
            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'coin.wav'))
            sound.play()

        self.sprites.update()
#Actualizo control de coliciones del jugador y plataforma
        self.player.validate_platform(self.platform)
#actualizo los elemenotes (paredes) que no se visualizan
        self.update_elements(self.walls)
#actualizo los elemenotes (monedas) que no se pudieron tomar
        self.update_elements(self.coins)
#Vuelcvo a generar paredes cuando no hay más en pantalla
        self.generate_walls()

    def update_elements(self, elements):
        for element in elements:
			#Chequeo si los elementos (paredes) son visibles
            if not element.rect.right > 0:
                element.kill()

    def stop(self):
#Reproduzco sonido al colicionar con una pared
        sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'lose.wav'))
        sound.play()

        self.player.stop()
        self.stop_elements(self.walls)

        self.playing = False

    def stop_elements(self, elements):
#Detengo todos los elementos si hubo colición, todos los elementos deben tener el método stop
        for element in elements:
            element.stop()
#Formateo textos de score y niveles
    def score_format(self):
        return 'Score : {}'.format(self.score)

    def level_format(self):
        return 'Level : {}'.format(self.level)

#Dibujo texto en pantalla
    def draw_text(self):
        self.display_text(self.score_format(), 36, BLACK, WIDTH // 2, TEXT_POSY)
        self.display_text(self.level_format(), 36, BLACK, 60, TEXT_POSY)

        if not self.playing:
            self.display_text('Perdiste', 60, BLACK, WIDTH // 2, HEIGHT // 2)
            self.display_text('Presiona r para comenzar de nuevo', 30, BLACK, WIDTH // 2, 50)

    def display_text(self, text, size, color, pos_x, pos_y):
        font = pygame.font.Font(self.font, size)

        text = font.render(text, True, color)
        rect = text.get_rect()
        #mantengo el texto centrado en pantalla
        rect.midtop = (pos_x, pos_y)
#impacto texto en superficie
        self.surface.blit(text, rect)
#Genero un menu de opciones para el inicio del juego
    def menu(self):
        self.surface.fill(GREEN_LIGHT)
        self.display_text('Presiona una tecla para comenzar', 36, BLACK, WIDTH // 2, 10)
#Actualizo la pantalla
        pygame.display.flip()

        self.wait()
#Genero un método para que espere en el menu hasta que presione una letra
    def wait(self):
        wait = True

        while wait:
            self.clock.tick(FPS)
#Verifico que es lo que presiono, si es quit salgo, otra tecla comienzo a jugar
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    wait = False
                    self.running = False
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    wait = False
