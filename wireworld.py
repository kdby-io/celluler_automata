# -*- coding:utf-8 -*-

import time
import pygame as pg
import numpy as np
import weakref

CONDUCTOR = 0
HEAD = 1
TAIL = 2

WIDTH = 15
HEIGHT = 5
SCALE = 10

pg.init()
screen = pg.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))


class Cell:
    def __init__(self, x, y, status=CONDUCTOR):
        self.current = status
        self.next = CONDUCTOR
        self.x, self.y = x, y

matrix = []
for j in range(HEIGHT):
    matrix.append([])
    matrix[j] = [None] * WIDTH
matrix = np.array(matrix)

objs = []


def compute(cell):
    cell = cell()
    if cell is not None:
        color = (0, 0, 0)
        if cell.current == HEAD:
            cell.next = TAIL
            color = (255, 0, 0)
        elif cell.current == TAIL:
            cell.next = CONDUCTOR
            color = (255, 255, 0)
        elif cell.current == CONDUCTOR:
            count = 0
            ny_list = (-1, -1, -1,  0,  0,  1,  1,  1)
            nx_list = (-1,  0,  1, -1,  1, -1,  0,  1)
            for z in range(8):
                nx, ny = cell.x + nx_list[z], cell.y + ny_list[z]
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and matrix[ny, nx] is not None:
                    if matrix[ny, nx].current == HEAD:
                        count += 1
            if count == 1 or count == 2:
                cell.next = HEAD
                color = (0, 0, 255)
            else:
                cell.next = CONDUCTOR
                color = (255, 255, 0)
        pg.draw.rect(screen, color, (cell.x*SCALE, cell.y*SCALE, SCALE, SCALE), 0)
        # print("(%d, %d) : %d -> %d" % (cell.x, cell.y, cell.current, cell.next))


def evolve(cell):
    cell = cell()
    if cell is not None:
        cell.current = cell.next


def set_cell(x, y, status=CONDUCTOR):
    cell = Cell(x, y, status)
    matrix[y, x] = cell
    objs.append(weakref.ref(cell))


def remove_cell(x, y):
    objs.remove(weakref.ref(matrix[y, x]))
    matrix[y, x] = None


def show_console(m):
    for x in m:
        for cell in x:
            if cell is None:
                string = '.'
            elif cell.current == HEAD:
                string = 'O'
            elif cell.current == TAIL:
                string = 'o'
            else:
                string = '-'

            print(string, end=' ')
        print()


compute = np.vectorize(compute)
evolve = np.vectorize(evolve)
def run():
    while True:
        # show_console(matrix)

        t0 = time.time()
        compute(objs)
        evolve(objs)
        # map(compute, objs)
        # map(evolve, objs)
        t1 = time.time()
        pg.display.update()
        print(t1 - t0)

        time.sleep(0.01)


def main():

    # Set below default state
    set_cell(1, 2, CONDUCTOR)
    set_cell(2, 3, TAIL)
    set_cell(2, 1, CONDUCTOR)
    set_cell(3, 2, HEAD)
    set_cell(4, 2, CONDUCTOR)
    set_cell(5, 2, CONDUCTOR)
    set_cell(6, 2, CONDUCTOR)
    set_cell(7, 2, CONDUCTOR)

    set_cell(8, 1, CONDUCTOR)
    set_cell(8, 2, CONDUCTOR)
    set_cell(8, 3, CONDUCTOR)
    set_cell(9, 1, CONDUCTOR)
    set_cell(9, 3, CONDUCTOR)

    set_cell(10, 2, CONDUCTOR)
    set_cell(11, 2, CONDUCTOR)
    set_cell(12, 2, CONDUCTOR)
    set_cell(13, 2, CONDUCTOR)

    run()


if __name__ == '__main__':
    main()
