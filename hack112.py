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
    s = make_maze(app, app.rows, app.cols)
    app.listOfCells = make2dList(app.rows, app.cols, 0)
    for row in app.rows:
        for col in app.cols:
            newCell = Cell(left=True, top=True, right=True, bottom=True, \
                            row=row, col=col )
            app.listOfCells[row][col] = newCell

       
def make2dList(rows, cols, fill):
    return [ ([fill] * cols) for row in range(rows) ]


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
    visited = [[False] * w + [True] for _ in range(h)] + [[True] * (w + 1)]
    #vertical = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    #horizontal = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        visited[y][x] = 1
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (x2, y2) in d:
            if visited[y2][x2]: continue
            if x2 == x: 
                app.listOfCells[max(y, y2)][x].top = False
                print("hi")
            if x2 == x: 
                app.listOfCells[min(y, y2)][x].bottom = False
                print("hi")
            if y2 == y: 
                print("hi3")
                pass
                #app.listOfCells[y][max(x, x2)].left = False
            if y2 == y: 
                app.listOfCells[y][min(x, x2)].right = False

            walk(x2, y2)
 
    walk(randrange(w), randrange(h))
 
    #s = ""
    #for (a, b) in zip(horizontal, vertical):
    #    s += ''.join(a + ['\n'] + b + ['\n'])
    
    
    
 

def redrawAll(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, x1, y0, y1) = getCellBounds(app, row, col)
            cell = app.listOfCells[row][col]
            if cell.top:
                canvas.create_line(x0, y0, x1, y0)
            if cell.left:
                canvas.create_line(x0, y0, x0, y1)
            if cell.right:
                canvas.create_line(x1, y0, x1, y1)
            if cell.bottom:
                canvas.create_line(x0, y1, x1, y1)

            
            
    



def main():
    runApp(width=600, height=600)

if __name__ == '__main__':
    main()
