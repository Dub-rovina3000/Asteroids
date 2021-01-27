import pygame
from pygame.sprite import Sprite
import math
import sys
import game_functions as gf

### пульки
class Bullet(Sprite):
    
    ### создаем пульки
    def __init__(self, sa_settings, screen, ship, angle):
        super(Bullet, self).__init__()

        self.screen = screen
        self.angle = angle
        self.sa_settings = sa_settings

        ### берем скорость корабля
        self.speed = self.sa_settings.bullet_speed_factor

        ### сохраняем корабль
        self.ship = ship

        ### длина жизни пулек
        self.timeline = min(self.sa_settings.screen_height, self.sa_settings.screen_width) / self.sa_settings.bullet_speed_factor - 10
        
        ### загружаем изображение пульки и берем от него объект rect
        self.natural_image = self.sa_settings.bullet_image
        self.copy_image = self.natural_image.copy()
        self.rect = self.copy_image.get_rect()
        
        ### ставим пульку к носу корабля (в центр верхнего края)
        self.rect.centerx = (ship.rect.topright[0] + ship.rect.topleft[0]) /2
        self.rect.centery = ship.rect.centery
        
        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        ### moving отслеживает пару секунд движения вместе с кораблем
        self.moving = 0

    ### перемещаем пульку
    def update(self):
        ### уменьшаем время жизни пульки
        self.timeline -= 1

        ### если пулька еще в пределах корабля то она поворачивается вместе с ним
        if self.moving < 7:
            self.moving += 1
            if self.ship.moving_right:
                self.angle -= self.sa_settings.ship_angle_change
            if self.ship.moving_left:
                self.angle += self.sa_settings.ship_angle_change

        ### вращаем пульку и берем от повернутого изображения rect 
        self.copy_image = pygame.transform.rotate(self.natural_image, self.angle)
        self.rect = self.copy_image.get_rect()

        ### берем направление движения пульки
        self.direction = [-math.sin(self.angle*math.pi / 180), -math.cos(self.angle*math.pi / 180)]
        
        ### смещаем центр
        self.center += self.speed*self.direction[0]
        self.centery += self.speed*self.direction[1]

        ### проверяем на выход за границы экрана и возвращаем на экран с другой стороны
        self.center = gf.return_to_view(self.center, self.rect.width, self.direction[0], self.sa_settings.screen_width)
        self.centery = gf.return_to_view(self.centery, self.rect.height, self.direction[1], self.sa_settings.screen_height, 1.5)
        
        ### смещаем пульку
        self.rect.centerx = self.center
        self.rect.centery = self.centery

    ### рисуем пульку
    def draw_bullet(self):
        self.screen.blit(self.copy_image, self.rect)