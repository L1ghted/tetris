import pygame
import random, time, sys

fps = 60
width, height = 600, 500
cell_size, surf_w, surf_h = 20, 20, 10


class Board:
    # создание поля
    def __init__(self):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 200
        self.top = 50
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self):
        self.left = 200
        self.top = 100
        self.cell_size = cell_size

    def render(self):
        pygame.draw.rect(screen, 'WHITE', (self.left, self.top, 20 * 10, 20 * 20 - 5), 1)

    def get_cell(self, mouse_pos):
        if (mouse_pos[0] < self.left) or (
                mouse_pos[0] > self.left + self.width * self.cell_size) \
                or (mouse_pos[1] < self.top) or (
                mouse_pos[1] > self.top + self.height * self.cell_size):
            return None
        return (mouse_pos[0] - self.left) // self.cell_size, (
                mouse_pos[1] - self.top) // self.cell_size

    def on_click(self, cell_coords):
        print(cell_coords)


if __name__ == '__main__':
    # поле 5 на 7
    pygame.init()
    size = width, height = 600, 500
    screen = pygame.display.set_mode(size)
    board = Board()
    board.set_view()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
    pygame.quit()
