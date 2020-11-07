################################
# avantikn, aamanis, amohidee, dvalmyr

################################

from random import shuffle, randrange
from cmu_112_graphics import *

def appStarted(app):
    app.rows = 16
    app.cols = 16



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


def make_maze(app):
    visited = [[False] * app.cols + [True] for _ in range(app.rows)] + [[1] * (w + 1)]
    vertical = [["|  "] * app.cols + ['|'] for _ in range(app.rows)] + [[]]
    horizontal = [["+--"] * app.cols + ['+'] for _ in range(app.rows + 1)]

    def walk(x, y):
        visited[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (dx, dy) in d:
            if visited[dy][dx]: continue
            if dx == x: horizontal[max(y, dy)][x] = "0  "
            if dy == y: vertical[y][max(x, dx)] = "   "
            walk(dx, dy)
 
    walk(randrange(app.cols), randrange(app.rows))
 
    s = ""
    for (a, b) in zip(horizontal, vertical):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s
 

def redrawAll(app, canvas):
    pass

if __name__ == '__main__':
    print(make_maze())