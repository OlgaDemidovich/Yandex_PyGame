import os
import random
import pygame
import sys
import time


def level(level, screen):
    pygame.font.init()

    font = pygame.font.Font(None, 70)

    back_sprites = pygame.sprite.Group()
    BackGround(0, back_sprites)
    BackGround(1290, back_sprites)

    car_sprite = pygame.sprite.Group()
    car = Car(car_sprite)

    life_sprite = pygame.sprite.Group()
    Life(1120, life_sprite)
    Life(1060, life_sprite)
    Life(1000, life_sprite)

    running = True
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    car_sprite.update(-190)
                elif event.key == pygame.K_DOWN:
                    car_sprite.update(190)

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

        pygame.display.flip()

    pygame.display.flip()

    return running, points


def ok(points, screen, running):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 70)
    playing = True
    text1 = font.render(f'Набрано очков: {points}', True,
                        (0, 0, 0))
    screen.blit(text1, (400, 200))
    while running and playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                playing = False
        pygame.display.flip()
    return running


def task_creation(level):
    a, b = str(random.randrange(10, 100)), str(random.randrange(1, 100))
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


class BackGround(pygame.sprite.Sprite):
    image = load_image("road.png")

    def __init__(self, x, *group):
        super().__init__(*group)
        self.image = BackGround.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 0

    def update(self, *args):
        if self.rect.x <= -1290:
            self.rect.x = 1290
        self.rect = self.rect.move(-2, self.rect.y)


if __name__ == '__main__':
    size = 1200, 696
    screen = pygame.display.set_mode(size)
    running, points = level('-', screen)
    ok(points, screen, running)
    pygame.quit()