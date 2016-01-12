# -*- coding:utf-8 -*-

from time import sleep
import pygame

EMPTY = 0
HEAD = 1
TAIL = 2
CONDUCTOR = 3

WIDTH = 14
HEIGHT = 5
SCALE = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))


class Cell(object):
    def __init__(self, status=EMPTY):
        self.current_status = status
        self.next_status = status

    def evolve(self):
        self.current_status = self.next_status

    def __str__(self):
        if self.current_status == EMPTY:
            return ' '
        elif self.current_status == HEAD:
            return 'O'
        elif self.current_status == TAIL:
            return 'o'
        else:
            return '-'


class Matrix(list):
    def __init__(self, width, height):
        super(Matrix, self).__init__()

        self.width = width
        self.height = height

        for x in range(width):
            self.append([])
            self[x] = [Cell()] * height

    def compute(self):

        nx_list = [-1,  0,  1, -1,  1, -1,  0,  1]
        ny_list = [-1, -1, -1,  0,  0,  1,  1,  1]

        for x in range(self.width):
            for y in range(self.height):

                if self[x][y].current_status == EMPTY:
                    self[x][y].next_status = EMPTY
                elif self[x][y].current_status == HEAD:
                    self[x][y].next_status = TAIL
                elif self[x][y].current_status == TAIL:
                    self[x][y].next_status = CONDUCTOR
                elif self[x][y].current_status == CONDUCTOR:
                    count = 0
                    for i in range(8):
                        nx = x + nx_list[i]
                        ny = y + ny_list[i]
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self[nx][ny].current_status == HEAD:
                                count += 1
                    if count == 1 or count == 2:
                        self[x][y].next_status = HEAD
                    else:
                        self[x][y].next_status = CONDUCTOR

    def evolve(self):
        for x in range(self.width):
            for y in range(self.height):
                self[x][y].evolve()

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self[x][y], sep='', end='')
            print()

    def set_cell(self, x, y, status):
        self[x][y] = Cell(status)

    def run(self):
        while True:
            self.print()
            self.compute()
            self.evolve()
            display(self)
            sleep(0.2)


def display(matrix):
    color = (0, 0, 0)
    for x in range(matrix.width):
        for y in range(matrix.height):
            if matrix[x][y].current_status == EMPTY:
                color = (0, 0, 0)
            elif matrix[x][y].current_status == HEAD:
                color = (0, 0, 255)
            elif matrix[x][y].current_status == TAIL:
                color = (255, 0, 0)
            elif matrix[x][y].current_status == CONDUCTOR:
                color = (255, 255, 0)
            pygame.draw.rect(screen, color, (x*SCALE, y*SCALE, SCALE, SCALE), 0)
    pygame.display.update()


def main():

    matrix = Matrix(WIDTH, HEIGHT)

    # Set below default state
    matrix.set_cell(1, 2, TAIL)
    matrix.set_cell(2, 3, HEAD)
    matrix.set_cell(2, 1, CONDUCTOR)
    matrix.set_cell(3, 2, CONDUCTOR)
    matrix.set_cell(4, 2, CONDUCTOR)
    matrix.set_cell(5, 2, CONDUCTOR)
    matrix.set_cell(6, 2, CONDUCTOR)
    matrix.set_cell(7, 2, CONDUCTOR)

    matrix.set_cell(8, 1, CONDUCTOR)
    matrix.set_cell(8, 2, CONDUCTOR)
    matrix.set_cell(8, 3, CONDUCTOR)
    matrix.set_cell(9, 1, CONDUCTOR)
    matrix.set_cell(9, 3, CONDUCTOR)

    matrix.set_cell(10, 2, CONDUCTOR)
    matrix.set_cell(11, 2, CONDUCTOR)
    matrix.set_cell(12, 2, CONDUCTOR)
    matrix.set_cell(13, 2, CONDUCTOR)

    matrix.run()


if __name__ == '__main__':
    main()
