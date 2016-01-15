# -*- coding:utf-8 -*-

import pygame as pg
import numpy as np
import weakref

import sys

CONDUCTOR = 0
HEAD = 1
TAIL = 2

CONDUCTOR_COLOR = (255, 170, 170)
HEAD_COLOR = (85, 0, 0)
TAIL_COLOR = (128, 21, 21)
EMPTY_COLOR = (0, 0, 0)

WIDTH = 50
HEIGHT = 50
SCALE = 10


def init():
    global matrix, conductors, DISPLAYSURF
    pg.init()
    DISPLAYSURF = pg.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    pg.display.set_caption("Wireworld")

    matrix = []
    conductors = []

    for j in range(HEIGHT):
        matrix.append([])
        matrix[j] = [None] * WIDTH
    matrix = np.array(matrix)


def compute(cell):
    global matrix
    cell = cell()
    if cell is not None:
        if cell.current == HEAD:
            cell.next = TAIL
        elif cell.current == TAIL:
            cell.next = CONDUCTOR
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
            else:
                cell.next = CONDUCTOR
        # print("(%d, %d) : %d -> %d" % (cell.x, cell.y, cell.current, cell.next))


def evolve(cell):
    global DISPLAYSURF
    cell = cell()
    if cell is not None and cell.current != cell.next:
        if cell.next == HEAD:
            color = HEAD_COLOR
        elif cell.next == TAIL:
            color = TAIL_COLOR
        else:
            color = CONDUCTOR_COLOR
        cell.current = cell.next
        pg.draw.rect(DISPLAYSURF, color, (cell.x*SCALE, cell.y*SCALE, SCALE, SCALE), 0)


def set_cell(x, y, status=CONDUCTOR):
    global matrix, conductors, DISPLAYSURF

    class Cell:
        def __init__(self, x, y, status=CONDUCTOR):
            self.current = status
            self.next = CONDUCTOR
            self.x, self.y = x, y

    if matrix[y, x] is None:
        cell = Cell(x, y, status)
        matrix[y, x] = cell
        conductors.append(weakref.ref(cell))
        pg.draw.rect(DISPLAYSURF, CONDUCTOR_COLOR, (cell.x*SCALE, cell.y*SCALE, SCALE, SCALE), 0)
        pg.display.flip()


def remove_cell(x, y):
    global matrix, conductors, DISPLAYSURF
    if matrix[y, x] is not None:
        conductors.remove(weakref.ref(matrix[y, x]))
        matrix[y, x] = None
        pg.draw.rect(DISPLAYSURF, EMPTY_COLOR, (x*SCALE, y*SCALE, SCALE, SCALE), 0)
        pg.display.flip()


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
    global conductors
    # show_console(matrix)

    # map(compute, objs)
    # map(evolve, objs)
    compute(conductors)
    evolve(conductors)
    # pg.time.delay(30)


def main():

    init()
    # Set below default state
    set_cell(1, 2)
    set_cell(2, 3, TAIL)
    set_cell(2, 1)
    set_cell(3, 2, HEAD)
    set_cell(4, 2)
    set_cell(5, 2)
    set_cell(6, 2)
    set_cell(7, 2)

    set_cell(8, 1)
    set_cell(8, 2)
    set_cell(8, 3)
    set_cell(9, 1)
    set_cell(9, 3)

    set_cell(10, 2)
    set_cell(11, 2)
    set_cell(12, 2)
    set_cell(13, 2)

    clock = pg.time.Clock()
    mouse_pressed = False
    paused = False

    while True:
        clock.tick(10)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                print(pg.mouse.get_pressed())
                mouse_pressed = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    paused = not paused

        while mouse_pressed:
            if pg.mouse.get_pressed() == (1, 0, 0):
                x, y = pg.mouse.get_pos()[0]//SCALE, pg.mouse.get_pos()[1]//SCALE
                set_cell(x, y)
            elif pg.mouse.get_pressed() == (0, 0, 1):
                x, y = pg.mouse.get_pos()[0]//SCALE, pg.mouse.get_pos()[1]//SCALE
                remove_cell(x, y)
            elif pg.mouse.get_pressed() == (0, 0, 0):
                mouse_pressed = False

            for event in pg.event.get():
                if mouse_pressed is True and event.type == pg.MOUSEBUTTONUP:
                    mouse_pressed = False

        if not paused:
            run()

        pg.display.flip()


if __name__ == '__main__':
    main()
