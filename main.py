import pygame
import copy
from random import choice, randrange
import sys

fps = 60
cell_size, width, height = 25, 10, 20

pygame.init()
screen = pygame.display.set_mode((450, 540))
pygame.display.set_caption('Tetris')
game_screen = pygame.Surface((cell_size * width, cell_size * height))
clock = pygame.time.Clock()
running = True
pygame.mixer.music.load("data/tetris_theme.mp3")
pygame.mixer.music.set_volume(0.05)
gameover = pygame.mixer.Sound('data/game_over.mp3')
end = False


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Tetris", "",
                  "Управление стрелками",
                  "Нажмите, чтобы начать"]

    fon = pygame.transform.scale(pygame.image.load('data/fon.jpg'), (450, 540))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.y = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


grid = []  # сетка игрового поля
for x in range(width):
    for y in range(height):
        grid.append(pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],  # координаты клеток фигуры
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, 1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + width // 2, y + 1, 1, 1) for x, y in f_pos] for f_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, cell_size - 2, cell_size - 2)


def create_field():
    field = []
    line_field = []
    for _ in range(height):
        for _ in range(width):
            line_field.append(0)
        field.append(line_field.copy())
        line_field.clear()
    return field


game_field = create_field()
a_count, a_speed, a_limit = 0, 60, 2000
figure, next_figure = copy.deepcopy(choice(figures)), copy.deepcopy(choice(figures))

font = pygame.font.Font('data/font.ttf', 35)
end_font = pygame.font.Font('data/font.ttf', 25)
title = font.render('TETRIS', True, pygame.Color('green'))
score_title = font.render('score:', True, pygame.Color('LightBlue'))
record_title = font.render('record:', True, 'purple')
game_over_title = end_font.render('GAME OVER', True, 'red')
score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def rand_color():
    return randrange(50, 256), randrange(50, 256), randrange(50, 256)


color, next_color = rand_color(), rand_color()


def col_borders():  # столкновение с границами
    if figure[i].x < 0 or figure[i].x > width - 1:
        return True
    elif figure[i].y > height - 1 or game_field[figure[i].y][figure[i].x]:
        return True
    return False


def get_record():
    with open('data/records.txt') as f:
        rec = f.readline()
        if not rec:
            return 0
        return rec


def set_record(record, score):
    with open('data/records.txt', 'w') as f:
        f.write(str(max(int(record), score)))


start_screen()
pygame.mixer.music.play(-1)
while running:

    record = get_record()
    rotate = False
    dx = 0
    screen.fill((0, 0, 0))
    screen.blit(game_screen, (20, 20))
    screen.blit(title, (290, 20))
    screen.blit(score_title, (290, 425))
    screen.blit(font.render(str(score), True, 'white'), (290, 460))
    screen.blit(record_title, (290, 300))
    screen.blit(font.render(record, True, pygame.Color('white')), (290, 340))
    game_screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            if event.key == pygame.K_DOWN:
                a_limit = 400
            if event.key == pygame.K_UP:
                rotate = True

    fig_copy = copy.deepcopy(figure)  # движение фигуры по х
    for i in range(4):
        figure[i].x += dx
        if col_borders():
            figure = copy.deepcopy(fig_copy)
            break

    a_count += a_speed  # движение фигуры по y
    if a_count > a_limit:
        a_count = 0
        fig_copy = copy.deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if col_borders():
                for j in range(4):
                    game_field[fig_copy[j].y][fig_copy[j].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = copy.deepcopy(choice(figures)), rand_color()
                a_limit = 2000
                break

    center = figure[0]  # поворот фигуры
    fig_copy = copy.deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if col_borders():
                figure = copy.deepcopy(fig_copy)
                break

    line, lines = height - 1, 0
    for row in range(height - 1, -1, -1):
        count = 0
        for i in range(width):
            if game_field[row][i]:
                count += 1
            game_field[line][i] = game_field[row][i]
        if count < width:
            line -= 1
        else:
            a_speed += 3
            lines += 1
    score += scores[lines]

    for cell in grid:
        pygame.draw.rect(game_screen, (30, 30, 30), cell, 1)  # отрисовка сетки игрового поля

    for i in range(4):  # отрисовка фигуры
        figure_rect.x = figure[i].x * cell_size
        figure_rect.y = figure[i].y * cell_size
        pygame.draw.rect(game_screen, color, figure_rect)

    pygame.draw.rect(screen, 'white', (290, 80, 140, 130), 2)
    for i in range(4):
        figure_rect.x = next_figure[i].x * cell_size + 240
        figure_rect.y = next_figure[i].y * cell_size + 110
        pygame.draw.rect(screen, next_color, figure_rect)

    for y, raw in enumerate(game_field):  # отрисовка всех фигур с игрового поля
        for x, col in enumerate(raw):
            if col:
                figure_rect.x = x * cell_size
                figure_rect.y = y * cell_size
                pygame.draw.rect(game_screen, col, figure_rect)

    for i in range(width):  # перезапуск игры
        if game_field[0][i]:
            pygame.mixer.music.stop()
            gameover.play()
            gameover.set_volume(0.05)
            set_record(record, score)
            game_field = create_field()
            a_count, a_speed, a_limit = 0, 60, 2000
            score = 0
            for rect in grid:
                screen.blit(game_over_title, (290, 250))
                pygame.draw.rect(game_screen, color, rect)
                screen.blit(game_screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)
            while True:
                if end:
                    break
                end = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        end = True
                pygame.display.flip()
                clock.tick(fps)
            pygame.mixer.music.play()
    pygame.display.flip()
    clock.tick(fps)
