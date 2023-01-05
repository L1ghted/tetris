import pygame
import copy

fps = 60
cell_size, width, height = 20, 10, 20

pygame.init()
screen = pygame.display.set_mode((cell_size * width, cell_size * height))
clock = pygame.time.Clock()
running = True

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
figure = copy.deepcopy(figures[0])  # тестовая фигура


def col_borders():  # столкновение с границами
    if figure[i].x < 0 or figure[i].x > width - 1:
        return True
    return False


while running:
    dx = 0
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
    fig_copy = copy.deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if col_borders():
            figure = copy.deepcopy(fig_copy)
            break

    for cell in grid:
        pygame.draw.rect(screen, (30, 30, 30), cell, 1)  # отрисовка сетки игрового поля

    for i in range(4):  # отрисовка фигуры
        figure_rect.x = figure[i].x * cell_size
        figure_rect.y = figure[i].y * cell_size
        pygame.draw.rect(screen, 'white', figure_rect)

    pygame.display.flip()
    clock.tick(fps)
