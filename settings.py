import pygame
import sys
class Settings():

    def __init__(self):

        ### параметры экрана
        self.screen_width = 1560
        self.screen_height = 800

        ### скорость корабля
        self.ship_speed_factor = 5
        self.ship_angle_change = 2

        ### скорость пульки
        self.bullet_speed_factor = 10

        ### fps
        self.fps = 60
        
        ### количество астероидов на экране
        self.as_amount = 20

        ### начало игры и звук
        self.start_game = True
        self.sound_on_bool = True

        ### заставка
        self.zastavka = pygame.image.load(sys.path[0]+"\\pictures\\zastavka.png")
        self.zastavka_rect = self.zastavka.get_rect()
        self.zastavka_rect.centerx = self.screen_width / 2
        self.zastavka_rect.centery = self.screen_height / 2

        ### картиночка для звука
        self.sound_on = pygame.image.load(sys.path[0]+"\\pictures\\sound_on.png")
        self.sound_off = pygame.image.load(sys.path[0]+"\\pictures\\sound_off.png")
        self.sound_on_rect = self.sound_on.get_rect()
        self.sound_on_rect.centerx = self.screen_width - 255
        self.sound_on_rect.centery = 33

        ### астероид, задний план, картинки взрыва, корабля и пули
        self.asteroid = pygame.image.load(sys.path[0]+"\\pictures\\asteroid.png")
        self.background = pygame.image.load(sys.path[0]+"\\pictures\\bg.jpg")
        self.images = [
            pygame.image.load(sys.path[0]+"\\pictures\\explosion1.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\explosion2.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\explosion3.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\explosion4.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\explosion5.png")
            ]

        self.ship_imgs = [
            pygame.image.load(sys.path[0]+"\\pictures\\ship1.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\ship2.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\ship_shield1.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\ship_shield2.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\ship_shield3.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\engine_shield1.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\engine_shield2.png"), 
            pygame.image.load(sys.path[0]+"\\pictures\\engine_shield3.png")
            ] 

        self.bullet_image = pygame.image.load(sys.path[0]+"\\pictures\\fire.png")

        ### звук взрывов, музыка, выстрелы
        self.explosion_sound1 = pygame.mixer.Sound(sys.path[0] + '\\sound\\explosion1.mp3')
        self.explosion_sound1.set_volume(0.05)
        self.explosion_sound2 = pygame.mixer.Sound(sys.path[0] + '\\sound\\explosion2.mp3')
        self.explosion_sound2.set_volume(0.4)

        self.music = sys.path[0] + '\\sound\\music.mp3'
       
        self.shoot_sound = pygame.mixer.Sound(sys.path[0] + '\\sound\\shoot.mp3')
