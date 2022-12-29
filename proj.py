import os
import random
import pygame
import sys
import time
import sqlite3

pygame.font.init()
objects = []


def screen_menu():
    global objects, running
    pygame.display.flip()
    objects = []
    image = load_image('back.png')
    Button(400, 200, 400, 100, 'Играть', screen_level)
    Button(400, 400, 400, 100, 'Рейтинг', screen_rating)
    while running:
        for obj in objects:
            obj.process()
            if not running and running is not None:
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for obj in objects:
                    obj.pressed()

        pygame.display.flip()
        screen.blit(image, (0, 0))
    pygame.display.flip()


def screen_rating():
    global objects, running
    objects = []
    font = pygame.font.Font(None, 50)
    image = load_image('back.png')
    playing = True
    con = sqlite3.connect('profile.db')
    cur = con.cursor()
    info = list(cur.execute(f"""SELECT point, name FROM profile""").fetchall())
    print(info)
    info = sorted(info, key=lambda x: x[0], reverse=True)
    print(info)
    Button(10, 10, 150, 60, 'Назад')
    while running and playing:
        for obj in objects:
            obj.process()

        if not running:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for obj in objects:
                    obj.pressed()
                    if running is None:
                        objects = []
                        Button(400, 200, 400, 100, 'Играть', screen_level)
                        Button(400, 400, 400, 100, 'Рейтинг', screen_rating)
                        running = True
                        playing = False
                        break
                    if not running:
                        break

        pygame.draw.rect(screen, '#00a1b8',
                         (380, 80, 440, 460))
        i = 100
        screen.blit(font.render('Имя', True,
                                (0, 0, 0)), (400, i - 10))
        screen.blit(font.render('Очки', True,
                                (0, 0, 0)), (700, i - 10))
        for point, name in info:
            i += 40
            screen.blit(font.render(str(name), True,
                                    (0, 0, 0)), (400, i))
            screen.blit(font.render(str(point), True,
                                    (0, 0, 0)), (700, i))
            if i == 500:
                break

        pygame.display.flip()
        screen.blit(image, (0, 0))
    pygame.display.flip()
    print('rating END')


def screen_level():
    global objects, running
    objects = []
    image = load_image('back.png')
    playing = True
    Button(10, 10, 150, 60, 'Назад')
    Button(50, 300, 300, 100, 'Сложение', screen_play, '+')
    Button(450, 300, 300, 100, 'Вычитание', screen_play, '-')
    Button(850, 300, 300, 100, 'Умножение', screen_play, '*')
    while running and playing:
        for obj in objects:
            obj.process()

        if not running:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('level click')
                for obj in objects:
                    obj.pressed()
                    print('pr', running)
                    if running is None:
                        objects = []
                        Button(400, 200, 400, 100, 'Играть', screen_level)
                        Button(400, 400, 400, 100, 'Рейтинг', screen_rating)
                        running = True
                        playing = False
                        break
                    if not running:
                        break

        pygame.display.flip()
        screen.blit(image, (0, 0))

    pygame.display.flip()
    print('level END')


def screen_play(level):
    global objects, running
    objects = []
    font = pygame.font.Font(None, 70)
    font1 = pygame.font.Font(None, 40)

    back_sprites = pygame.sprite.Group()
    Road(0, back_sprites)
    Road(1290, back_sprites)

    car_sprite = pygame.sprite.Group()
    car = Car(car_sprite)

    life_sprite = pygame.sprite.Group()
    Life(1120, life_sprite)
    Life(1060, life_sprite)
    Life(1000, life_sprite)

    Button(10, 10, 150, 60, 'Назад')

    playing = True
    points = 0
    t_start = time.monotonic() - 7
    text = font.render('', True,
                       (255, 255, 255))
    answer_1 = font.render('', True,
                           (255, 255, 255))
    answer_2 = font.render('', True,
                           (255, 255, 255))
    answer_3 = font.render('', True,
                           (255, 255, 255))

    answer_road = -1
    answer_x = 1050
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
                    if running is None:
                        objects = []
                        Button(10, 10, 150, 60, 'Назад')
                        Button(50, 300, 300, 100, 'Сложение', screen_play, '+')
                        Button(450, 300, 300, 100, 'Вычитание', screen_play,
                               '-')
                        Button(850, 300, 300, 100, 'Умножение', screen_play,
                               '*')
                        running = True
                        playing = False
                        break

        if not running:
            break
        screen.fill((255, 255, 255))

        back_sprites.draw(screen)
        back_sprites.update()

        life_sprite.draw(screen)
        timer = time.monotonic() - t_start
        if timer >= 3:
            answer_x -= 2

        if timer >= 9:
            answer_x = 1050
            if car.road != answer_road != -1:
                for enemy in life_sprite:
                    life_sprite.remove(enemy)
                    break
                if not life_sprite:
                    playing = False
            else:
                points += 1
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
    if running:
        ok(points)


def ok(points):
    global running, objects
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 70)
    playing = True
    text = font.render(f'Набрано очков: {points}', True,
                       (0, 0, 0))
    screen.blit(text, (400, 200))
    while running and playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                playing = False
        pygame.display.flip()
    objects = []
    Button(10, 10, 150, 60, 'Назад')
    Button(50, 300, 300, 100, 'Сложение', screen_play, '+')
    Button(450, 300, 300, 100, 'Вычитание', screen_play, '-')
    Button(850, 300, 300, 100, 'Умножение', screen_play, '*')


def task_creation(level):
    a, b = str(random.randrange(10, 100)), str(random.randrange(10, 100))
    if level == '-' and b >= a:
        a, b = b, a
    answer = eval(a + level + b)
    answers = [str(answer)] + [str(answer + i) for i in
                               random.sample([-10, 10, 20], k=2)]
    return f'{a} {level} {b}', answers


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
    image = load_image("life.png")

    def __init__(self, x, *group):
        super().__init__(*group)
        self.image = Life.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 20

    def update(self, *args):
        if self.rect.x <= -1290:
            self.rect.x = 1290
        self.rect = self.rect.move(-2, self.rect.y)


class Car(pygame.sprite.Sprite):
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
    image = load_image("road.png")

    def __init__(self, x, *group):
        super().__init__(*group)
        self.image = Road.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self, *args):
        if self.rect.x <= -1290:
            self.rect.x = 1290
        self.rect = self.rect.move(-2, self.rect.y)


class Button:
    def __init__(self, x, y, width, height, button_text,
                 onclick_function=None, *args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.args = args
        self.onclickFunction = onclick_function
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#00a1b8',
            'hover': '#017b93'
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        font = pygame.font.Font(None, 50)
        self.buttonSurf = font.render(button_text, True, (0, 0, 0))
        objects.append(self)

    def process(self):
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
        global running
        running = True
        mouse_pos = pygame.mouse.get_pos()
        if self.buttonRect.collidepoint(mouse_pos):
            try:
                self.onclickFunction(*self.args)
                self.alreadyPressed = True
            except TypeError:
                running = None


if __name__ == '__main__':
    size = 1200, 696
    screen = pygame.display.set_mode(size)
    running = True
    screen_menu()
    pygame.quit()
