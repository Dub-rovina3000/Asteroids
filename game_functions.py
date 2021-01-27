import sys
import pygame
from bullets import Bullet
import settings

### переменные для хранения параметров взрыва
sec = []
selp = []

### проверка нажатия клавиш
def check_keydown_events(event, sa_settings, screen, ship, bullets):
    ### если нажата d то двигаемся вправо
    if event.key == pygame.K_d:
        ship.moving_right = True
    ### если а то влево
    elif event.key == pygame.K_a:
        ship.moving_left = True
    ### если пробел то выпускаем пульку 
    elif event.key == pygame.K_SPACE:
        ### загружаем звук
        sound1 = sa_settings.shoot_sound
        sound1.set_volume(0.2)
        ### проверяем на звук
        if sa_settings.sound_on_bool:
            sound1.play()
        ### создаем новую пульку и добавляем ее в группку пулек
        new_bullet = Bullet(sa_settings, screen, ship, ship.angle)
        bullets.add(new_bullet)
    ### если w то движемся вперед
    elif event.key == pygame.K_w:
        ship.moving = True
        
### если кнопочки не нажаты, то убираем все перемещения
def check_keyup_events(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False
    if event.key == pygame.K_w:
        ship.moving = False
        
### проверяем что произошло, нажали мы на кнопочку, на выход или щелкнули мышкой
def check_events(sa_settings, screen, ship, bullets):
    for event in pygame.event.get():
        ### если мы выходим, значит выходим
        if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        ### если была нажата кнопочка, то проверяем какая и обрабатываем нажатие
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, sa_settings, screen, ship, bullets)
        ### если кнопочка была отпущена, то проверяем какая и обрабатываем
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        ### если мы тыкнули мышкой
        elif event.type == pygame.MOUSEBUTTONUP:
            ### то проверяем вдруг мы тыкнули на включение звука
            if sa_settings.sound_on_rect.collidepoint(event.pos):
                ### если да то мы либо выключаем звук и останавливаем музыку
                if sa_settings.sound_on_bool:
                    sa_settings.sound_on_bool = False
                    pygame.mixer.music.pause()
                ### либо включаем звук и продолжаем проигрывать музыку
                else:
                    sa_settings.sound_on_bool = True
                    pygame.mixer.music.unpause()
                
### обновляем экран и обрабатываем взрывы
def update_screen(sa_settings, screen, ship, bullets, asteroids, sp):
    global sec
    global selp
    ### основной фон
    background = sa_settings.background
    background_rect = background.get_rect()

    ### выводим фон, пульки и астероиды
    screen.blit(background, background_rect)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    for aster in asteroids.sprites():
        aster.blitme()  

    ### если это начало игры, то корабль выводить не надо
    if sa_settings.start_game:
        pass
    else:
        ship.blitme()
    
    ### изменяем количество псевдосекунд жизни для каждого уничтоженного астероида
    sec = [i - 1 for i in sec]
    ### проверяем если псевдосекунды стали равны 0 или меньше 0 то удаляем место уничтоженного астероида из массива
    selp = [selp[i] for i in range(len(selp)) if sec[i] > 0]
    ### удаляем все псевдосекунды меньше или равные нулю (по логике они не должны стать меньше 0, но всегда что-то может пойти не так)
    sec = [i for i in sec if i > 0]
    ### если у нас есть новые уничтоженные астероиды
    if sp != []:
        ### добавляем в массив псевдосекунд 15 единиц на каждое место взрыва
        sec += [50 for i in sp]
        ### добавляем в массив мест взрыва новые места взрыва из переданного массива
        selp += [i for i in sp]
    ### проигрываем взрыв для каждого элемента массива
    for i in range(len(selp)):
        explosion(sa_settings, screen, selp[i], sec[i])

    ### если звук включен, то вставляем картинку включенного звука
    if sa_settings.sound_on_bool:
        screen.blit(sa_settings.sound_on, sa_settings.sound_on_rect)
    ### если выключен, то выключенного
    else:
        screen.blit(sa_settings.sound_off, sa_settings.sound_on_rect)

### обрабатываем нажатия в момент начала игры
def check_events_start_game(sa_settings, screen):
    ### если у нас начало игры (хотя эта проверка бесполезна, ведь мы вызываем этот метод только когда у нас начало игры)
    if sa_settings.start_game:
        ### для каждого события проверяем
        for event in pygame.event.get():
            ### если это выход из игры
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            ### если это клик мышью
            elif event.type == pygame.MOUSEBUTTONUP:
                ### если мы кликаем по заставке то игра начинается
                if sa_settings.zastavka_rect.collidepoint(event.pos):
                    sa_settings.start_game = False
                ### если мы кликаем по иконке звука
                elif sa_settings.sound_on_rect.collidepoint(event.pos):
                    ### то нам надо проверить был ли звук включен до этого
                    if sa_settings.sound_on_bool:
                        ### если да то выключаем и останавливаем музыку
                        sa_settings.sound_on_bool = False
                        pygame.mixer.music.pause()
                    else:
                        ### если нет то включаем и запускаем музыку
                        sa_settings.sound_on_bool = True
                        pygame.mixer.music.unpause()

### функция обработки взрыва
def explosion(sa_settings, screen, pos, ie):
    ### загружаем изображения
    images = sa_settings.images
    ### выбираем какое именно изображение взрыва нам подходит в зависимости от того сколько псевдосекунд прошло с момента уничтожения астероида
    if ie > 40:
        i = 0
    elif ie > 30:
        i = 1
    elif ie > 20:
        i = 2
    elif ie > 10:
        i = 3
    else:
        i = 4
    ### загружаем это изображение в позицию взрыва астероида и показываем его
    rect = images[i].get_rect()
    rect.centerx = pos[0]
    rect.centery = pos[1]
    screen.blit(images[i], rect)
    
### функция проверяющая объекты на выход за пределы экрана и возвращающая их с другой стороны
def return_to_view(center, measure, direction, screen_measure, k = 1):
    ### если центр объекта по одной из осей и половина его измерения по этой оси меньше нуля и при этом у нас отрицательное направление это значит что мы вышли за пределы экрана слева или сверху и продолжаем двигаться еще дальше
    if center + measure/2 < 0 and direction < 0:
        ### то мы добавляем к центру объекта измерение экрана (ширину или высоту в зависимости от переданных параметров) и измерение объекта (ширину или высоту)
        center += screen_measure  + measure
    ### если центр объекта по одной из осей минус половина его измерения по этой оси больше измерения экрана и при этом у нас неотрицательное направление это значит что мы вышли за пределы экрана снизу или справа и продолжаем двигаться еще дальше
    if center - measure/2 > screen_measure and direction > 0:
        ### тогда мы вычитаем из центра объекта измерение экрана и измерение объекта домноженного на коэффициент k
        center += - screen_measure  - k*measure
    ### возвращаем центральную координату нашего объекта
    return center

    

