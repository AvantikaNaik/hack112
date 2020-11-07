################################
# avantikn, aamanis, amohidee, dvalmyr

################################

from random import shuffle, randrange
from cmu_112_graphics import *

from dataclasses import make_dataclass

Cell = make_dataclass('Cell', ['left', 'top', 'right', 'bottom', 'row', 'col'])

def appStarted(app):
    app.rows = 16
    app.cols = 16
    app.margin = 5
    app.cells = [([None] * app.cols) for i in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            newCell = Cell(left=True, top=True, right=True, bottom=True, \
                            row=row, col=col )
            app.cells[row][col] = newCell
    make_maze(app, 16, 16)


def getCellBounds(app, row, col):
    gridWidth = app.width - 2 * app.margin
    gridHeight = app.height - 2 * app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + (col * cellWidth)
    x1 = app.margin + ((col + 1) * cellWidth)
    y0 = app.margin + (row * cellHeight)
    y1 = app.margin + ((row + 1)* cellHeight)
    return (x0, x1, y0, y1)


def make_maze(app, w, h):
    visited = [[False] * w + [True] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        visited[y][x] = True
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (x2, y2) in d:
            if visited[y2][x2]: continue
            if x2 == x: 
                app.cells[max(y, y2)][x].top = False
                print("hi")
            if x2 == x: 
                app.cells[min(y, y2)][x].bottom = False
                print("hi")
            if y2 == y: 
                print("hi3")
                app.cells[y][max(x, x2)].left = False
            if y2 == y: 
                app.cells[y][min(x, x2)].right = False

            walk(x2, y2)
 
    walk(randrange(app.cols), randrange(app.rows))
 

def redrawAll(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, x1, y0, y1) = getCellBounds(app, row, col)
            cell = app.cells[row][col]
            if cell.top:
                canvas.create_line(x0, y0, x1, y0)
            if cell.left:
                canvas.create_line(x0, y0, x0, y1)
            if cell.right:
                canvas.create_line(x1, y0, x1, y1)
            if cell.bottom:
                canvas.create_line(x0, y1, x1, y1)


if __name__ == '__main__':
    runApp(width=600, height=600)
