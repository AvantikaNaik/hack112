################################
# avantikn, aamanis, amohidee, dvalmyr

################################

from random import shuffle, randrange
from cmu_112_graphics import *
import random
import time
from dataclasses import make_dataclass

Cell = make_dataclass('Cell', ['left', 'top', 'right', 'bottom', 'row', 'col'])

def appStarted(app):
    app.start = time.time()
    app.gameOver = False
    app.score = 0
    app.endMaze = False

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

    makeGhost(app)

    app.keyImg = app.loadImage('key.gif')
    app.scaledImg = app.scaleImage(app.keyImg, 1/20)

    app.charImg = app.loadImage('character.gif')
    app.scaledChar = app.scaleImage(app.charImg, 2/5)

    app.ghostImg = app.loadImage('ghost.gif')
    app.scaledGhost = app.scaleImage(app.ghostImg, 1/6)

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

def makeGhost(app):
    app.ghostX = random.randint(800, 1600)
    app.ghostY = random.randint(800, 1600)

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

def moveGhost(app):
    if app.pX > app.ghostX:
        app.ghostX += 2
    else:
        app.ghostX -= 2
    if app.pY > app.ghostY:
        app.ghostY += 2
    else:
        app.ghostY -= 2

def isDead(app):
    if ((app.pX -app.ghostX) ** 2 + (app.pY - app.ghostY) ** 2) ** 0.5 < 5:
        return True
        
def timerFired(app):
    print(getCell(app, 0, 0))
    moveGhost(app)
    if isDead(app):
        app.gameOver = True
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

def drawGhost(app, canvas):
    canvas.create_image(app.ghostX, app.ghostY, image=ImageTk.PhotoImage(app.scaledGhost))

def drawDeadEnds(app, canvas):
    for end in app.newDE:
        (x0, y0, x1, y1) = getCellBounds(app, end[0], end[1])
        canvas.create_image(x0 + 5*app.r, y0 + 5*app.r, image=ImageTk.PhotoImage(app.scaledImg))
    
def drawPlayer(app, canvas):
    canvas.create_image(app.pX, app.pY, image=ImageTk.PhotoImage(app.scaledChar.rotate(app.rotationAngle)))

def drawStartScreen(app, canvas):
    if time.time() - app.start < 3:
        canvas.create_rectangle(0, 0, app.width, app.height, fill = 'grey')
        canvas.create_rectangle(0, app.height//2 - 100, app.width, app.height//2 + 100, fill = 'black')
        canvas.create_text(app.width //2, app.height//2, text='Start Game!', font='Arial 40 bold', fill='red')

def drawGameOver(app, canvas):
    if app.gameOver:
        canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
        canvas.create_text(app.width//2, app.height//2, text='Game Over', font='Arial 40 bold', fill='red')

def drawPortal(app,canvas):
    row = app.rows - 1
    col = app.cols - 1
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    canvas.create_rectangle(x0, y0, x1, y1, fill='lightsalmon')

def intersectPortal(app):
    row = app.rows - 1
    col = app.cols - 1
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    d = (((x0 + 50) - app.width//2)**2 + ((y0 + 50) - app.height//2)**2)**0.5
    if d < 0:
        app.score += 1
        appStarted(app)


def redrawAll(app, canvas):
    canvas.create_rectangle(0,0,app.height,app.width, fill = "black")
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            cell = app.cells[row][col]
            if cell.top:
                canvas.create_line(x0, y0, x1, y0, width = 3, fill="white")
            if cell.left:
                canvas.create_line(x0, y0, x0, y1, width = 3, fill="white")
            if cell.right:
                canvas.create_line(x1, y0, x1, y1, width = 3, fill="white")
            if cell.bottom:
                canvas.create_line(x0, y1, x1, y1, width = 3, fill="white")
    drawDeadEnds(app, canvas)
    drawPlayer(app, canvas)
    drawGhost(app, canvas)
    drawStartScreen(app, canvas)
    drawPortal(app, canvas)
    drawGameOver(app, canvas)

if __name__ == '__main__':
    runApp(width=620, height=620)
