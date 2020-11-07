################################
# avantikn, aamanis, amohidee, dvalmyr

################################

from random import shuffle, randrange
from cmu_112_graphics import *

from dataclasses import make_dataclass

Cell = make_dataclass('Cell', ['left', 'top', 'right', 'bottom', 'row', 'col'])

def appStarted(app):

    app.timerDelay = 15

    app.cellSize = 100

    app.rows = 16
    app.cols = 16
    app.margin = app.height / 2 - app.cellSize / 2
    app.r = 10
    app.pR = 15
    app.deadEnds = []
    app.newDE = []
    

    app.goUp = False
    app.goDown = False
    app.goLeft = False
    app.goRight = False

    app.dx = 0
    app.dy = 0
    
    app.keyImg = app.loadImage('key.gif')
    app.scaledImg = app.scaleImage(app.keyImg, 1/20)

    app.charImg = app.loadImage('character.gif')
    app.scaledChar = app.scaleImage(app.charImg, 2/5)

    app.rotationAngle = 0
    
    app.pX = app.width / 2
    app.pY = app.height / 2
    
    app.cells = [([None] * app.cols) for i in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            newCell = Cell(left=True, top=True, right=True, bottom=True, \
                            row=row, col=col )
            app.cells[row][col] = newCell
    make_maze(app, 16, 16)
    findDeadEnds(app)
    selectDeadEnds(app)


def getCellBounds(app, row, col):
    cellWidth = 100
    cellHeight = 100
    x0 = app.margin + (col * app.cellSize) + app.dx
    x1 = app.margin + ((col + 1) * app.cellSize) + app.dx
    y0 = app.margin + (row * app.cellSize) + app.dy
    y1 = app.margin + ((row + 1)* app.cellSize) + app.dy
    return (x0, y0, x1, y1)

def getCell(app, x, y):
    row = (y - app.dy - app.margin) // app.cellSize + 3
    col = (x - app.dx - app.margin) // app.cellSize + 3
    return (int(row), int(col))

def keyPressed(app, event):
    if(event.key == 'Up'):
        app.goUp = True
        app.rotationAngle = 90
    if(event.key == 'Down'):
        app.goDown = True
        app.rotationAngle = 270
    if(event.key == 'Left'):
        app.goLeft = True
        app.rotationAngle = 180
    if(event.key == 'Right'):
        app.goRight = True
        app.rotationAngle = 0

def timerFired(app):
    print(getCell(app, 0, 0))
    if(app.goUp):
        row, col = getCell(app, 0, 0)
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        if(app.cells[row][col].top and y0 > 290):
            app.dy += 6
        app.dy += 6
    if(app.goDown):
        row, col = getCell(app, 0, 0)
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        if(app.cells[row][col].bottom and y1 - app.margin < 67):
            app.dy += 6
        app.dy -= 6
    if(app.goLeft):
        row, col = getCell(app, 0, 0)
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        if(app.cells[row][col].left and x0 > 290):
            print(x0, y0, x1, y1)
            app.dx -= 6
        app.dx += 6
    if(app.goRight):
        row, col = getCell(app, 0, 0)
        x0, y0, x1, y1 = getCellBounds(app, row, col)
        if(app.cells[row][col].right and x1 - app.margin < 68):
            app.dx += 6
        app.dx -= 6


def keyReleased(app, event):
    if(event.key == 'Up'):
        app.goUp = False
    if(event.key == 'Down'):
        app.goDown = False
    if(event.key == 'Left'):
        app.goLeft = False
    if(event.key == 'Right'):
        app.goRight = False
        


def make_maze(app, w, h):
    visited = [[False] * w + [True] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        visited[y][x] = True
 
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (x2, y2) in d:
            if visited[y2][x2]: 
                continue
            if x2 == x: 
                app.cells[max(y, y2)][x].top = False
            if x2 == x: 
                app.cells[min(y, y2)][x].bottom = False
            if y2 == y: 
                app.cells[y][max(x, x2)].left = False
            if y2 == y: 
                app.cells[y][min(x, x2)].right = False

            walk(x2, y2) 
 
    walk(randrange(app.cols), randrange(app.rows))
    print(app.deadEnds)

def findDeadEnds(app):
    for row in range(app.rows):
        for col in range(app.cols):
            cell = app.cells[row][col]
            dE = 0
            if cell.top: dE += 1
            if cell.bottom: dE += 1
            if cell.left: dE += 1
            if cell.right: dE += 1
            if dE >= 3:
                app.deadEnds.append((row, col))

def selectDeadEnds(app):
    length = len(app.deadEnds)
    shuffle(app.deadEnds)
    for i in range(length//5):
        row = app.deadEnds[i][0]
        col = app.deadEnds[i][1]
        app.newDE.append((row, col))
    print(app.newDE)


def drawDeadEnds(app, canvas):
    for end in app.newDE:
        (x0, y0, x1, y1) = getCellBounds(app, end[0], end[1])
        canvas.create_image(x0 + 5*app.r, y0 + 5*app.r, image=ImageTk.PhotoImage(app.scaledImg))
    
def drawPlayer(app, canvas):
    canvas.create_image(app.pX, app.pY, image=ImageTk.PhotoImage(app.scaledChar.rotate(app.rotationAngle)))

def redrawAll(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            cell = app.cells[row][col]
            if cell.top:
                canvas.create_line(x0, y0, x1, y0)
            if cell.left:
                canvas.create_line(x0, y0, x0, y1)
            if cell.right:
                canvas.create_line(x1, y0, x1, y1)
            if cell.bottom:
                canvas.create_line(x0, y1, x1, y1)
    drawDeadEnds(app, canvas)
    drawPlayer(app, canvas)



if __name__ == '__main__':
    runApp(width=620, height=620)
