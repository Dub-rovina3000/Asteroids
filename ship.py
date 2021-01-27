import pygame
import random
import math
import sys
import game_functions as gf

class Ship():
    ### создаем корабль
    def __init__(self, sa_settings, screen):
        
        self.screen = screen
        self.sa_settings = sa_settings

        self.lifes = 3
        self.score = 0
        ### можем ли мы вредить кораблю
        self.on_Damage = True
        ### индекс изображения корабля
        self.im = 0
        ### таймер смены изображения
        self.sec = 0
        ### скорость корабля, угол, и изображения
        self.speed = 0
        self.angle = 0
        self.images = self.sa_settings.ship_imgs
        ### копируем изображение по индексу (первое изображение будет 0)
        self.copy_image = self.images[self.im].copy()
        ### получаем объект rect 
        self.rect = self.copy_image.get_rect()
        self.screen_rect = screen.get_rect()
        
        ### ставим корабль на середину поля
        self.rect.centerx = self.sa_settings.screen_width/2
        self.rect.centery = self.sa_settings.screen_height/2

        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        ### флаги перемещения
        self.moving = False
        self.moving_right = False
        self.moving_left = False
        

    def update(self):
        ### изменяем угол поворота корабля
        if self.moving_right:
            self.angle -= self.sa_settings.ship_angle_change
        if self.moving_left:
            self.angle += self.sa_settings.ship_angle_change
        
        ### проверяем движение и выставляем индекс изображения относительно таймера
        if self.moving:
            if self.sec > 2000:
                self.im = 7
            elif self.sec > 1000:
                self.im = 6
            elif self.sec > 0:
                self.im = 5
            else:
                self.im = 1
        else:
            if self.sec > 2000:
                self.im = 4
            elif self.sec > 1000:
                self.im = 3
            elif self.sec > 0:
                self.im = 2
            else:
                self.im = 0
        
        ### передаем новое повернутое на угол angle изображение в copy_image 
        self.copy_image = pygame.transform.rotate(self.images[self.im], self.angle)
        ### берем объект rect для последующего изменения положения изображения
        self.rect = self.copy_image.get_rect()
        
        ### если движемся то скорость берем из sa_settings, иначе плавно уменьшаем скорость до 0
        if self.moving:
            self.speed = self.sa_settings.ship_speed_factor
        else:
            if self.speed < 0.25:
                self.speed = 0
            else:
                self.speed *= 0.99

        ### задаем направление движения корабля
        self.direction = [-math.sin(self.angle*math.pi / 180), -math.cos(self.angle*math.pi / 180)]

        ### перемещаем центр изображения по х и по у
        self.center += self.speed*self.direction[0]
        self.centery += self.speed*self.direction[1]

        ### проверяем на выход за границы экрана и возвращаем на экран с другой стороны
        self.center = gf.return_to_view(self.center, self.rect.width, self.direction[0], self.sa_settings.screen_width)
        self.centery = gf.return_to_view(self.centery, self.rect.height, self.direction[1], self.sa_settings.screen_height, 1.5)
        
        ### смещаем объект
        self.rect.centerx = self.center
        self.rect.centery = self.centery

    ### рисуем кораблик с новым изображением в новом месте
    def blitme(self):
        self.screen.blit(self.copy_image, self.rect)
        