# -*- coding:utf-8 -*-

from time import sleep
import pygame as pg
import numpy as np

EMPTY = 0
HEAD = 1
TAIL = 2
CONDUCTOR = 3

WIDTH = 250
HEIGHT = 250
SCALE = 4

pg.init()
screen = pg.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))


class Matrix:
    def __init__(self, width, height):
        super(Matrix, self).__init__()

        self.width = width
        self.height = height

        self.current_gen = np.zeros((height, width), dtype=np.int8)
        self.next_gen = np.zeros((height, width), dtype=np.int8)

    def compute(self):
        ny_list = [-1, -1, -1,  0,  0,  1,  1,  1]
        nx_list = [-1,  0,  1, -1,  1, -1,  0,  1]

        color = (0, 0, 0)

        for x in range(self.width):
            for y in range(self.height):

                if self.current_gen[y, x] == EMPTY:
                    self.next_gen[y, x] = EMPTY
                    color = (0, 0, 0)
                elif self.current_gen[y, x] == HEAD:
                    self.next_gen[y, x] = TAIL
                    color = (255, 0, 0)
                elif self.current_gen[y, x] == TAIL:
                    self.next_gen[y, x] = CONDUCTOR
                    color = (255, 255, 0)
                elif self.current_gen[y, x] == CONDUCTOR:
                    count = 0
                    for i in range(8):
                        nx = x + nx_list[i]
                        ny = y + ny_list[i]
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.current_gen[ny, nx] == HEAD:
                                count += 1
                    if count == 1 or count == 2:
                        self.next_gen[y, x] = HEAD
                        color = (0, 0, 255)
                    else:
                        self.next_gen[y, x] = CONDUCTOR
                        color = (255, 255, 0)
                pg.draw.rect(screen, color, (x*SCALE, y*SCALE, SCALE, SCALE), 0)
        pg.display.update()
        self.current_gen = self.next_gen.copy()

    def set_cell(self, x, y, status):
        self.current_gen[y, x] = status

    def run(self):
        while True:
            self.compute()
            # sleep(0.1)


def main():

    matrix = Matrix(WIDTH, HEIGHT)

    # Set below default state
    matrix.set_cell(1, 2, CONDUCTOR)
    matrix.set_cell(2, 3, TAIL)
    matrix.set_cell(2, 1, CONDUCTOR)
    matrix.set_cell(3, 2, HEAD)
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
