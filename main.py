import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from bullets import Bullet
from asteroids import Asteroids

### создаем часики для грамотной работы fps 
clock = pygame.time.Clock()

### главная функция игры
def run_game():
    pygame.init()
    ### объявляем старт игры, чтобы у нас шло начальное изображение с заставкой и тд
    sa_settings.start_game = True
    ### делаем экран и подпись к игре
    screen = pygame.display.set_mode((sa_settings.screen_width, sa_settings.screen_height))
    pygame.display.set_caption("Space Adventures")

    ### создаем кораблик
    ship = Ship(sa_settings, screen)

    ### и пульки с астероидами
    bullets = Group()
    asteroids = Group()

    ### не забываем про звуки взрывов
    sound1 = sa_settings.explosion_sound1
    sound2 = sa_settings.explosion_sound2

    ### и объявление количества очков и жизней
    text_score = myfont.render('Score: ' + str(ship.score),False, (255, 255, 255))
    lifes_text = myfont.render('Lifes: ' + str(ship.lifes),False, (255, 255, 255))
    
    ### создаем астероиды, которые будут лететь влево со определенной скоростью
    for i in range(sa_settings.as_amount):
        new_as = Asteroids(sa_settings, screen, ship.score, 1, [1,0], bol = True)
        asteroids.add(new_as)

    ### проверяем на начало игры
    while sa_settings.start_game:

        ### проверяем что творится, если мы тыкнули на заставочку или на кнопочки отключения звука
        gf.check_events_start_game(sa_settings, screen)

        ### изменяет экран чтобы астероиды летели звук отключался и включался
        gf.update_screen(sa_settings, screen, ship, bullets, asteroids, [])
        asteroids.update()

        ### рисуем заставку и текст поверх всего
        screen.blit(sa_settings.zastavka, sa_settings.zastavka_rect)

        screen.blit(lifes_text,(sa_settings.screen_width-200,10))
        screen.blit(text_score,(50,10))
        ### обновляем экран
        pygame.display.flip()

    ### вышли из цикла и удаляем все астероиды
    for aster in asteroids.copy():
            asteroids.remove(aster)

    ### добавляем астероиды в рандомных местах с рандомной скоростью и рандомным направлением
    for i in range(sa_settings.as_amount):
        new_as = Asteroids(sa_settings, screen, ship.score, bol = True)
        asteroids.add(new_as)
    
    ### основной цикл игры идет пока у корабля есть жизни
    while ship.lifes != 0:
        ### ставим часы чтоб работал fps
        clock.tick(sa_settings.fps)

        ### создаем массив точек взрыва
        sp = []

        ### проверяем события клавиатуры и мыши
        gf.check_events(sa_settings, screen, ship, bullets)
        ### обновляем положение корабля, пулек и астероидов
        ship.update()
        bullets.update()
        asteroids.update()
        ### объявляем количество убитых астероидов
        k = 0
        ### проверяем пересечение астероидов с кораблем и пульками
        for aster in asteroids.copy():
            ### сначала с пульками
            for bullet in bullets.copy():
                ### проверка на пересечение
                if aster.rect.colliderect(bullet.rect): 
                    ### проверка на звук, если откл то не проигрываем
                    if sa_settings.sound_on_bool:
                        sound2.play()
                    ### увеличиваем очки корабля
                    ship.score += 1
                    ### добавляем место взрыва астероида
                    sp.append([aster.rect.centerx, aster.rect.centery])
                    ### удаляем астероид из списка астероидов и пульку из списка пулек
                    asteroids.remove(aster)
                    bullets.remove(bullet)
                    ### добавляем 1 к потерям
                    k += 1

            ### если можно взорвать корабль
            if ship.on_Damage:
                ### то проверяем находится ли астероид в поле корабля
                if ship.rect.colliderect(aster.rect):
                    ### проверяем доступен ли звук
                    if sa_settings.sound_on_bool:
                        sound1.play()
                    ### забираем жизнь у корабля
                    ship.lifes -= 1
                    ### добавляем место взрыва астероида в список
                    sp.append([aster.rect.centerx, aster.rect.centery])
                    ### удаляем астероид
                    asteroids.remove(aster)
                    ### смещаем корабль в центр
                    ship.rect.centerx = sa_settings.screen_width/2
                    ship.rect.centery = sa_settings.screen_height/2

                    ship.center = sa_settings.screen_width/2
                    ship.centery = sa_settings.screen_height/2
                    ### говорим что корабль нельзя убивать и объявляем таймер
                    ship.on_Damage = False
                    ship.sec = 3000
                    ### добавляем 1 к потерям
                    k += 1
            else:
                ### если корабль нельзя повредить, то уменьшаем таймер
                ship.sec -= 1
                ### как только таймер станет меньше 0 
                if ship.sec < 0:
                    ### корабль снова может быть поврежден
                    ship.on_Damage = True

        ### восстанавливаем потери, добавляем количество убитых астероидов
        for i in range(k):
            new_as = Asteroids(sa_settings, screen, ship.score)
            asteroids.add(new_as)

        ### удаляем пульки если их линия жизни равна 0
        for bullet in bullets.copy():
            if bullet.timeline <= 0:
                bullets.remove(bullet)

        ### пересоздаем текст, поскольку очки и жизни корабля изменились
        text_score = myfont.render('Score: ' + str(ship.score),False, (255, 255, 255))
        lifes_text = myfont.render('Lifes: ' + str(ship.lifes),False, (255, 255, 255))
        
        ### обновляем экран, передаем туда наш массив мест смерти астероидов
        gf.update_screen(sa_settings, screen, ship, bullets, asteroids, sp)

        ### выводим текст
        screen.blit(lifes_text,(sa_settings.screen_width-200,10))
        screen.blit(text_score,(50,10))

        ### обновляем экран
        pygame.display.flip()

    ### снова говорим что у нас начало игры, потому что конец от начала мало чем отличается
    sa_settings.start_game = True

    ### удаляем все пульки и астероиды
    for aster in asteroids.copy():
        asteroids.remove(aster)
    for bullet in bullets.copy():
        bullets.remove(bullet)
    
    ### начинаем финальный цикл нашей игры где выводим количество очков человека
    while sa_settings.start_game:
        ### все еще проверяем события и обновляем экран
        gf.check_events_start_game(sa_settings, screen)
        gf.update_screen(sa_settings, screen, ship, bullets, asteroids, [])
        
        ### рисуем текст и заставку
        screen.blit(sa_settings.zastavka, sa_settings.zastavka_rect)
        screen.blit(lifes_text,(sa_settings.screen_width-200,10))
        screen.blit(text_score,(50,10))
        
        ### обновляем экран
        pygame.display.flip()
    



### для шрифтов
pygame.font.init() 
### шрифт
myfont = pygame.font.SysFont('Comic Sans MS', 30)
### для музыки
pygame.mixer.init()
### музыка)

sa_settings = Settings()

music = sa_settings.music
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(1)
### проигрываем музыку и зацикливаем ее, чтобы она была всегда
pygame.mixer.music.play(-1)

while True:
    run_game()

