import os
import random
import pygame
import sys
import time
import sqlite3

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()
objects = []


def distributor():
    """Инициализация функций отрисовывающих экраны"""
    global func, arg
    while running:
        func(arg)


def screen_authorization(error):
    """Отрисовка экрана авторизации с возможностью вводить имя и пароль
    пользователя, обработка нажатия на кнопки для перехода в главное меню
    или экрана регистрации"""
    global name, password, func, arg, objects, running, playing, back_music
    password = ''
    playing = True
    pygame.display.flip()
    objects = []
    clock = pygame.time.Clock()
    image = load_image('back.png')

    base_font = pygame.font.Font(None, 32)
    font = pygame.font.Font(None, 50)
    font_big = pygame.font.Font(None, 80)

    person_name = pygame.Rect(525, 260, 150, 32)
    person_password = pygame.Rect(525, 310, 150, 32)
    Button(500, 400, 200, 50, 'Войти', authorization)
    Button(475, 460, 250, 40, 'Регистрация', screen_registration, 35)

    color_active = pygame.Color('#ffffff')
    color_passive = pygame.Color('#00a1b8')

    active_name = False
    active_password = False
    if not back_music:
        back.play(-1)
        back_music = True
    while running and playing:
        screen.blit(image, (0, 0))

        pygame.draw.rect(screen, '#01c9e3',
                         (380, 130, 440, 430))

        for obj in objects:
            obj.process()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break

                if person_name.collidepoint(event.pos):
                    active_name = True
                else:
                    active_name = False

                if person_password.collidepoint(event.pos):
                    active_password = True
                else:
                    active_password = False

            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) <= 9:
                        name += event.unicode

                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif len(password) <= 9:
                        password += event.unicode

        if active_name:
            color_name = color_active
        else:
            color_name = color_passive

        if active_password:
            color_password = color_active
        else:
            color_password = color_passive

        pygame.draw.rect(screen, color_name, person_name)
        pygame.draw.rect(screen, color_password, person_password)

        screen.blit(font_big.render('MathCar', True, (0, 0, 0)),
                    (480, 60))

        screen.blit(font.render('Вход', True, (0, 0, 0)),
                    (550, 180))
        screen.blit(base_font.render('Имя:', True, (0, 0, 0)),
                    (435, 265))
        screen.blit(base_font.render('Пароль:', True, (0, 0, 0)),
                    (400, 315))

        if error and not active_name and not active_password:
            screen.blit(base_font.render(error, True, (255, 0, 0)),
                        (300, 600))
        elif error:
            error = ''

        text_name = base_font.render(name, True, (0, 0, 0))

        screen.blit(text_name, (person_name.x + 5, person_name.y + 5))

        text_password = base_font.render('*' * len(password), True, (0, 0, 0))

        screen.blit(text_password,
                    (person_password.x + 5, person_password.y + 5))

        pygame.display.flip()

        clock.tick(600)

    pygame.display.flip()


def screen_registration(error):
    """Отрисовка экрана регистрации с возможностью вводить имя и пароль
    нового пользователя, обработка нажатия на кнопки для перехода в главное меню
    или экрана авторизации"""
    global name, password, password_2, func, arg, objects, running, playing
    playing = True
    pygame.display.flip()
    objects = []
    clock = pygame.time.Clock()
    image = load_image('back.png')

    base_font = pygame.font.Font(None, 32)
    font = pygame.font.Font(None, 50)
    font_big = pygame.font.Font(None, 80)

    person_name = pygame.Rect(615, 260, 150, 32)
    person_password = pygame.Rect(615, 310, 150, 32)
    person_password_2 = pygame.Rect(615, 360, 150, 32)

    Button(410, 430, 380, 50, 'Зарегистрироваться', registration)
    Button(500, 490, 200, 40, 'Вход', screen_authorization, 35)

    color_active = pygame.Color('#ffffff')
    color_passive = pygame.Color('#00a1b8')

    active_name = False
    active_password = False
    active_password_2 = False
    while running and playing:
        screen.blit(image, (0, 0))

        pygame.draw.rect(screen, '#01c9e3',
                         (380, 130, 440, 430))
        screen.blit(font_big.render('MathCar', True, (0, 0, 0)),
                    (480, 60))

        for obj in objects:
            obj.process()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break

                if person_name.collidepoint(event.pos):
                    active_name = True
                else:
                    active_name = False

                if person_password.collidepoint(event.pos):
                    active_password = True
                else:
                    active_password = False

                if person_password_2.collidepoint(event.pos):
                    active_password_2 = True
                else:
                    active_password_2 = False

            if event.type == pygame.KEYDOWN:
                if active_name:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) <= 9:
                        name += event.unicode

                elif active_password:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif len(password) <= 9:
                        password += event.unicode

                elif active_password_2:
                    if event.key == pygame.K_BACKSPACE:
                        password_2 = password_2[:-1]
                    elif len(password_2) <= 9:
                        password_2 += event.unicode

        if active_name:
            color_name = color_active
        else:
            color_name = color_passive

        if active_password:
            color_password = color_active
        else:
            color_password = color_passive

        if active_password_2:
            color_password_2 = color_active
        else:
            color_password_2 = color_passive

        pygame.draw.rect(screen, color_name, person_name)
        pygame.draw.rect(screen, color_password, person_password)
        pygame.draw.rect(screen, color_password_2, person_password_2)

        screen.blit(font.render('Регистрация', True, (0, 0, 0)),
                    (490, 180))
        screen.blit(base_font.render('Имя:', True, (0, 0, 0)),
                    (550, 265))
        screen.blit(base_font.render('Пароль:', True, (0, 0, 0)),
                    (515, 315))
        screen.blit(base_font.render('Повторите пароль:', True, (0, 0, 0)),
                    (400, 365))

        if error and not active_name and not active_password:
            screen.blit(base_font.render(error, True, (255, 0, 0)),
                        (300, 600))
        elif error:
            error = ''

        text_name = base_font.render(name, True, (0, 0, 0))

        screen.blit(text_name, (person_name.x + 5, person_name.y + 5))

        text_password = base_font.render('*' * len(password), True, (0, 0, 0))

        screen.blit(text_password,
                    (person_password.x + 5, person_password.y + 5))

        text_password_2 = base_font.render('*' * len(password_2), True,
                                           (0, 0, 0))

        screen.blit(text_password_2,
                    (person_password_2.x + 5, person_password_2.y + 5))

        pygame.display.flip()

        clock.tick(600)

    pygame.display.flip()


def authorization(*args):
    """Проверка существования пользователя и вывод ошибок на экран"""
    global func, arg

    if name == '' or password == '':
        func = screen_authorization
        arg = 'Пустые поля'
    else:
        con = sqlite3.connect('data/profile.db')
        cur = con.cursor()
        true_password = cur.execute(f"""SELECT password FROM profile 
                    WHERE name = '{name}'""").fetchone()

        if true_password and str(true_password[0]) == str(password):
            func = screen_menu
            arg = ()
        elif true_password is None:
            func = screen_authorization
            arg = 'Пользователя не существует'
        else:
            func = screen_authorization
            arg = 'Неверный пароль'


def registration(*args):
    """Проверка на новое имя пользователя и сходство паролей, добавление в
    БД информации о новом пользователе"""
    global func, arg
    con = sqlite3.connect('data/profile.db')
    cur = con.cursor()
    true_password = cur.execute(f"""SELECT password FROM profile 
                    WHERE name = '{name}'""").fetchone()

    if name == '' or password == '' or password_2 == '':
        func = screen_registration
        arg = 'Пустые поля'
    else:
        if true_password:
            func = screen_registration
            arg = 'Пользователь уже существует'
        elif password != password_2:
            func = screen_registration
            arg = 'Пароли не совпадают'
        elif true_password is None:
            cur.execute(f"""INSERT INTO profile(name, password, point) 
                            VALUES('{name}', '{password}', 0)""")
            con.commit()
            func = screen_menu


def screen_menu(*args):
    """Отрисовка главного меню, обработка нажатия на кнопки для перехода на
    экран выбора уровней, рейтинга или аворизации"""
    global objects, running, playing, back_music
    playing = True
    pygame.display.flip()
    objects = []
    image = load_image('back.png')
    font = pygame.font.Font(None, 50)
    font_big = pygame.font.Font(None, 80)

    con = sqlite3.connect('data/profile.db')
    cur = con.cursor()
    point = list(cur.execute(f"""SELECT point FROM profile 
                WHERE name = '{name}'""").fetchone())

    Button(400, 200, 400, 100, 'Играть', screen_level)
    Button(400, 350, 400, 100, 'Рейтинг', screen_rating)
    Button(400, 500, 400, 100, 'Сменить профиль', screen_authorization)
    if not back_music:
        back.play(-1)
        back_music = True
    while running and playing:
        screen.blit(image, (0, 0))
        screen.blit(font_big.render('MathCar', True, (0, 0, 0)),
                    (480, 60))
        for obj in objects:
            obj.process()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break
        screen.blit(font.render(f'{name}', True,
                                (0, 0, 0)), (10, 10))
        screen.blit(font.render(f'Очки: {point[0]}', True,
                                (0, 0, 0)), (10, 50))
        pygame.display.flip()

    pygame.display.flip()


def screen_rating(*args):
    """Отрисовка экрана рейтинга"""
    global objects, running, playing
    objects = []
    font = pygame.font.Font(None, 50)
    image = load_image('back.png')
    playing = True
    con = sqlite3.connect('data/profile.db')
    cur = con.cursor()
    info = list(cur.execute(f"""SELECT point, name FROM profile""").fetchall())
    info = sorted(info, key=lambda x: x[0], reverse=True)
    Button(10, 10, 150, 60, 'Назад', screen_menu)
    while running and playing:
        for obj in objects:
            obj.process()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break

        pygame.draw.rect(screen, '#00a1b8', (380, 80, 440, 460))
        i = 100
        screen.blit(font.render('Имя', True,
                                (0, 0, 0)), (400, i - 10))
        screen.blit(font.render('Очки', True,
                                (0, 0, 0)), (700, i - 10))
        for point, name_person in info:
            i += 40
            screen.blit(font.render(str(name_person), True,
                                    (0, 0, 0)), (400, i))
            screen.blit(font.render(str(point), True,
                                    (0, 0, 0)), (700, i))
            if i == 500:
                break
        pygame.display.flip()
        screen.blit(image, (0, 0))

    pygame.display.flip()


def screen_level(*args):
    """Отрисовка экрана выбора уровней, обработка нажатия на кнопки для
    перехода в главное меню или на экран игры определённого уровня
    в зависимости от нажатой кнопки"""
    global objects, running, playing, back_music
    pygame.display.flip()
    objects = []
    image = load_image('back.png')
    playing = True
    Button(10, 10, 150, 60, 'Назад', screen_menu)
    Button(50, 300, 300, 100, 'Сложение', screen_play, 50, '+')
    Button(450, 300, 300, 100, 'Вычитание', screen_play, 50, '-')
    Button(850, 300, 300, 100, 'Умножение', screen_play, 50, '*')
    if not back_music:
        back.play(-1)
        back_music = True
    while running and playing:
        for obj in objects:
            obj.process()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break

        pygame.display.flip()
        screen.blit(image, (0, 0))

    pygame.display.flip()


def screen_play(level):
    """Отрисовка экрана игры, обработка нажатия на кнопку, возвращающую на
    экран с выбором уровня. Возможность перемещать машину вверх и вниз
    соответствующими клавишами, отрисовка математических примеров и ответов,
    проверка их корректности. Начисление очков или уменьшение жизней в
    зависимости от правильности выбранного ответа"""
    global objects, running, playing, func, arg, back_music
    level = level[0]
    objects = []
    answer_road = -1
    answer_x = 1050
    count_task = 0
    playing = True
    points = 0

    font = pygame.font.Font(None, 70)
    font1 = pygame.font.Font(None, 40)

    back_sprites = pygame.sprite.Group()
    Road(0, back_sprites)
    Road(1290, back_sprites)

    car_sprite = pygame.sprite.Group()
    car = Car(car_sprite)

    life_sprite = pygame.sprite.Group()
    Life(1000, life_sprite)
    Life(1060, life_sprite)
    Life(1120, life_sprite)

    Button(10, 10, 150, 60, 'Назад', screen_level)

    t_start = time.monotonic() - 7
    text = font.render('', True,
                       (255, 255, 255))
    answer_1 = font.render('', True,
                           (255, 255, 255))
    answer_2 = font.render('', True,
                           (255, 255, 255))
    answer_3 = font.render('', True,
                           (255, 255, 255))
    back.stop()
    back_music = False
    drive.play(-1)
    while running and playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    car_sprite.update(-190)
                elif event.key == pygame.K_DOWN:
                    car_sprite.update(190)
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in objects:
                    obj.pressed()
                    if not playing:
                        break

        screen.fill((255, 255, 255))

        back_sprites.draw(screen)
        back_sprites.update()

        life_sprite.draw(screen)
        timer = time.monotonic() - t_start
        if timer >= 3:
            answer_x -= 2

        if timer >= 9:
            count_task += 1
            if count_task == 11:
                playing = False
            answer_x = 1050
            if car.road != answer_road and answer_road != -1:
                for enemy in life_sprite:
                    life_sprite.remove(enemy)
                    break
                if not life_sprite:
                    level_end_bad.play()
                    playing = False
                else:
                    point_down.play()
            elif car.road == answer_road:
                if level == '+':
                    points += 1
                if level == '-':
                    points += 2
                if level == '*':
                    points += 3
                if count_task != 11:
                    point_up.play()
            if not playing:
                continue
            t_start = time.monotonic()
            task, answers = task_creation(level)

            text = font.render(task, True,
                               (255, 255, 255))

            answer_road = random.randrange(3)
            answer = answers.pop(0)
            answers.insert(answer_road, answer)

            answer_1 = font.render(answers[0], True,
                                   (255, 255, 255))
            answer_2 = font.render(answers[1], True,
                                   (255, 255, 255))
            answer_3 = font.render(answers[2], True,
                                   (255, 255, 255))

        screen.blit(text, (500, 20))

        screen.blit(answer_1, (answer_x, 160))
        screen.blit(answer_2, (answer_x, 350))
        screen.blit(answer_3, (answer_x, 540))

        car_sprite.draw(screen)
        car_sprite.update(0)

        for obj in objects:
            obj.process()

        text_point = font1.render(f'Очки: {points}', True,
                                  (255, 255, 255))
        screen.blit(text_point, (200, 30))

        pygame.display.flip()
    pygame.display.flip()
    if running and (count_task == 11 or not life_sprite):
        func = screen_result
        if not life_sprite:
            arg = ''
        else:
            level_end_good.play()
            arg = points
    elif running:
        func = screen_level
        arg = ()
    drive.stop()


def screen_result(points):
    """Отрисовка экрана окончания уровня с комментарием о набранных очках
    или законченности жизней"""
    global running, objects, playing, func, arg, name
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 70)
    playing = True
    image = load_image('back.png')

    con = sqlite3.connect('data/profile.db')
    cur = con.cursor()
    info = list(cur.execute(f"""SELECT point FROM profile 
            WHERE name = '{name}'""").fetchone())
    screen.blit(image, (0, 0))
    if type(points) is int:
        text = font.render(f'Набрано очков: {points}', True,
                           (0, 0, 0))
        cur.execute(f"""UPDATE profile SET 
                    point = '{points + int(info[0])}'
                    WHERE name = '{name}'""")
        con.commit()
        screen.blit(text, (400, 200))
    else:
        text = font.render(f'Упс, кончились жизни', True,
                           (0, 0, 0))
        screen.blit(text, (340, 200))
    while running and playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                playing = False
        pygame.display.flip()
    func = screen_level
    arg = ()
    level_end_good.stop()
    level_end_bad.stop()


def task_creation(level):
    """Генерация математического примера и ответов, среди которых один верный"""
    a, b = str(random.randrange(10, 100)), str(random.randrange(10, 100))
    if level == '-' and b >= a:
        a, b = b, a
    answer = eval(a + level + b)
    answers = [str(answer)] + [str(answer + i) for i in
                               random.sample([-10, 10, 20], k=2)]
    return f'{a} {level} {b}', answers


def load_image(name_file, colorkey=None):
    """Подгрузка изображения"""
    fullname = os.path.join('data', name_file)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


class Life(pygame.sprite.Sprite):
    """Класс для создания спрайтов жизней для игры"""
    image = load_image("life.png")

    def __init__(self, x, *group):
        super().__init__(*group)
        self.image = Life.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 20


class Car(pygame.sprite.Sprite):
    """Класс для создания спрайта машины для игры
        Метод:
            update() - перемещение машины между полосами дороги"""
    image = load_image("car.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Car.image
        self.rect = self.image.get_rect()
        self.roads_restrictions = {0: [96, 116], 1: [286, 306], 2: [476, 496]}
        self.rect.x = 5
        self.rect.y = 106
        self.road = 0
        self.j = -2
        self.i = -1

    def update(self, *args):
        """Перемещение машины между полосами дороги"""
        i = args[0]
        if i < 0 and self.rect.y > 116 or i > 0 and self.rect.y < 476:
            self.road += i // 190
            self.rect = self.rect.move(0, i)
        if self.rect.y <= self.roads_restrictions[self.road][0]:
            self.j = 2
        elif self.rect.y >= self.roads_restrictions[self.road][1]:
            self.j = -2
        self.i = random.randrange(0, 3) // self.j
        self.rect = self.rect.move(0, self.i)


class Road(pygame.sprite.Sprite):
    """Класс для создания спрайта дороги для игры
            Метод:
                update() - перемещение дороги влево по экрану"""
    image = load_image("road.png")

    def __init__(self, x, *group):
        super().__init__(*group)
        self.image = Road.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self, *args):
        """Перемещение дороги влево по экрану"""
        if self.rect.x <= -1290:
            self.rect.x = 1290
        self.rect = self.rect.move(-2, self.rect.y)


class Button:
    """Класс для создания кнопки
            Методы:
                process() - отрисовка кнопки в зависимости от её состояния:
            покоится, нажата
                pressed() - при нажатии переписание функции,
            отображающей экран"""

    def __init__(self, x, y, width, height, button_text,
                 onclick_function=None, size_text=50, *args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.args = args
        self.onclickFunction = onclick_function

        self.fillColors = {
            'normal': '#00a1b8',
            'hover': '#017b93'
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        font = pygame.font.Font(None, size_text)
        self.buttonSurf = font.render(button_text, True, (0, 0, 0))
        objects.append(self)

    def process(self):
        """Отрисовка кнопки в зависимости от её состояния:
        покоится, нажата"""
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def pressed(self):
        """При нажатии изменение функции, отображающей экран"""
        global playing, func, arg
        playing = True
        mouse_pos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mouse_pos):
            playing = False
            func = self.onclickFunction
            arg = self.args


if __name__ == '__main__':
    point_up = pygame.mixer.Sound('data/point_up.wav')
    point_down = pygame.mixer.Sound('data/point_down.wav')
    level_end_bad = pygame.mixer.Sound('data/level_end_bad.wav')
    level_end_good = pygame.mixer.Sound('data/level_end_good.wav')
    back = pygame.mixer.Sound('data/back.wav')
    drive = pygame.mixer.Sound('data/drive.wav')
    back_music = False
    size = 1200, 696

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('MathCar')
    Icon = load_image('icon.ico')
    pygame.display.set_icon(Icon)

    running = True
    playing = True
    name = ''
    password = ''
    password_2 = ''
    arg = ()
    func = screen_authorization
    distributor()
    pygame.quit()
