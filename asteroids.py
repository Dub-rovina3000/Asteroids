import random
import pygame
from pygame.sprite import Sprite
import sys
import game_functions as gf

class Asteroids(Sprite):
    
    ### создаем астероид 
    def __init__(self, sa_settings, screen, score, speed = 0, direction = [], bol = False):
        super(Asteroids, self).__init__()
        
        self.screen = screen
        self.sa_settings = sa_settings

        ### объявляем скорость астероидов относительно счета игрока, чем выше счет тем больше скорость
        if score < 20:
            score = 0
        elif score < 40:
            score = 10
        elif score < 50:
            score = 20
        elif score < 70:
            score = 50
        elif score < 100:
            score = 70
        elif score < 150:
            score = 100
        else:
            score = 200

        ### проверка для первого экрана с равномерным движением астероидов по экрану в одну сторону
        if speed == 0:
            ### задаем рандомную скорость и умножаем ее на 110 , 120 , 150 , 170 , 200 или 400 процентов в зависимости от сложности игры 
            self.speed = random.randint(3, 7)*random.random()
            self.speed += self.speed*score/100
        else:
            self.speed = speed
        
        ### проверка для первого экрана с равномерным движением астероидов по экрану в одну сторону
        if direction == []:
            ### задаем направление астероидом относительно х и у, для этого берем рандомное число и домножаем его на + или - 1
            self.direction = [random.random()*random.choice((-1,1)), random.random()*random.choice((-1,1))]
        else:
            self.direction = direction

        ### создаем изображение астероида, извлекаем из него объект класса Rect для последующего определения местоположения астероида
        self.image = self.sa_settings.asteroid
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        ### проверка на создание астероидов для первого экрана или впервые, в этом случае они могут быть созданы в пределах экрана, иначе они создаются за пределами экрана
        if bol:
            ### рандомное местоположение вне квадрата корабля
            self.rect.centerx = random.choice(list(range(-10,round(sa_settings.screen_width/2)-100)) + list(range(round(sa_settings.screen_width/2)+100, sa_settings.screen_width+10)))
            self.rect.centery = random.choice(list(range(-10,round(sa_settings.screen_height/2)-100, 40)) + list(range(round(sa_settings.screen_height/2)+100, sa_settings.screen_height+10, 40)))
        else:
            ### рандомный х
            self.rect.centerx = random.randint(-10, sa_settings.screen_width+10)
            ### если х за пределами поля, то у может быть любым, иначе у должен быть вне пределов игрового экрана
            if self.rect.centerx < 0 or self.rect.centerx > sa_settings.screen_width:
                self.rect.centery = random.randint(-10, sa_settings.screen_height+10)
            else:
                ### выбираем у из промежутков от -высоты астероида-10 до -10 или от высоты экрана + высота астероида до высота экрана+ высота астероида + 20
                self.rect.centery = random.choice(list(range(-self.rect.height-10, -10)) + list(range(sa_settings.screen_height + self.rect.height, sa_settings.screen_height+self.rect.height + 20)))
        
        ### создаем координать центра, которые будем менять в последствии
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def update(self):
        ### берем центр по х и добавляем к нему скорость*направление
        self.center += self.speed*self.direction[0]
        ### определяем выход за границы экрана и возвращаем в пределы экрана
        self.center = gf.return_to_view(self.center, self.rect.width, self.direction[0], self.sa_settings.screen_width)
        ### перемещаем rect по х
        self.rect.centerx = self.center
        ### смещаем у на скорость*направление
        self.centery += self.speed*self.direction[1]
        ### определяем выход за границы экрана и возвращаем в пределы экрана
        self.centery = gf.return_to_view(self.centery, self.rect.height, self.direction[1], self.sa_settings.screen_height, 1.5)
        ### перемещаем rect по у
        self.rect.centery = self.centery

    ### выводим на экран
    def blitme(self):
        self.screen.blit(self.image, self.rect)