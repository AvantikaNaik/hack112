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
    elif(event.key == 'Down'):
        app.goDown = True
        app.rotationAngle = 270
    elif(event.key == 'Left'):
        app.goLeft = True
        app.rotationAngle = 180
    elif(event.key == 'Right'):
        app.goRight = True
        app.rotationAngle = 0

def moveGhost(app):
    if app.pX > app.ghostX:
        app.ghostX += 1
    else:
        app.ghostX -= 1
    if app.pY > app.ghostY:
        app.ghostY += 1
    else:
        app.ghostY -= 1

def isDead(app):
    if ((app.pX -app.ghostX) ** 2 + (app.pY - app.ghostY) ** 2) ** 0.5 < 5:
        return True
        
def timerFired(app):
    nearLines = getNearLines(app)
    moveGhost(app)
    if isDead(app):
        app.gameOver = True
    for line in nearLines:
        l_x0, l_y0, l_x1, l_y1 = line
        if(collisionRectLine(app.pX - app.pR, app.pY - app.pR, app.pX + app.pR, app.pY + app.pR,
                            l_x0, l_y0, l_x1, l_y1)):
                                print(f'rect = {app.pX - app.pR}, {app.pY - app.pR}, {app.pX + app.pR}, {app.pY + app.pR}')
                                print(f'line = {l_x0}, {l_y0}, {l_x1}, {l_y1}')

    if(app.goUp):
        legal = True
        for line in nearLines:
            l_x0, l_y0, l_x1, l_y1 = line
            if(collisionRectLine(app.pX - app.pR - 6, app.pY - app.pR - 6, app.pX + app.pR - 6, app.pY + app.pR - 6,
                                    l_x0, l_y0, l_x1, l_y1)):
                                        legal = False
        if(legal):
            app.dy += 6
        

    if(app.goDown):
        legal = True
        for line in nearLines:
            l_x0, l_y0, l_x1, l_y1 = line
            if(collisionRectLine(app.pX - app.pR + 6, app.pY - app.pR + 6, app.pX + app.pR + 6, app.pY + app.pR + 6,
                                    l_x0, l_y0, l_x1, l_y1)):
                                        app.dy += 7
        if(legal):
            app.dy -= 6
        

    if(app.goLeft):
        legal = True
        for line in nearLines:
            l_x0, l_y0, l_x1, l_y1 = line
            if(collisionRectLine(app.pX - app.pR - 6, app.pY - app.pR - 6, app.pX + app.pR - 6, app.pY + app.pR - 6,
                                    l_x0, l_y0, l_x1, l_y1)):
                                        legal = False
        if(legal):
            app.dx += 6
       

    if(app.goRight):
        legal = True
        for line in nearLines:
            l_x0, l_y0, l_x1, l_y1 = line
            if(collisionRectLine(app.pX - app.pR + 6, app.pY - app.pR + 6, app.pX + app.pR + 6, app.pY + app.pR + 6,
                                    l_x0, l_y0, l_x1, l_y1)):
                                        legal = False
        if(legal):
            app.dx -= 6


def keyReleased(app, event):
    if(event.key == 'Up'):
        app.goUp = False
    elif(event.key == 'Down'):
        app.goDown = False
    elif(event.key == 'Left'):
        app.goLeft = False
    elif(event.key == 'Right'):
        app.goRight = False
        
def getNearCells(app):
    nearCells = dict()
    rowC, colC = getCell(app, app.pX, app.pY)

    nearCells['center'] = (rowC, colC)
    nearCells['up'] = (rowC - 1, colC)
    nearCells['down'] = (rowC + 1, colC)
    nearCells['left'] = (rowC, colC - 1)
    nearCells['right'] = (rowC, colC + 1)

    return nearCells

def getNearLines(app):
    nearCells = getNearCells(app)
    nearLines = []
    for c in nearCells:
        x0, y0, x1, y1 = getCellBounds(app, nearCells[c][0], nearCells[c][1])
        row = nearCells[c][0]
        col = nearCells[c][1]
        cell = app.cells[row - 5][col - 5]
        if cell.top:
            nearLines.append((x0, y0, x1, y0))
        if cell.left:
            nearLines.append((x0, y0, x0, y1))
        if cell.right:
            nearLines.append((x1, y0, x1, y1))
        if cell.bottom:
            nearLines.append((x0, y1, x1, y1))
    return nearLines

def collisionRectLine(r_x0, r_y0, r_x1, r_y1, l_x0, l_y0, l_x1, l_y1):
    topRight = (r_x1, r_y0)
    topLeft = (r_x0, r_y0)
    botLeft = (r_x0, r_y1)
    botRight = (r_x1, r_y1)

    if(topRight[0] < l_x0):
        return False
    if(botLeft[0] > l_x1):
        return False
    if(botLeft[1] > l_y0 and topRight[1] < l_y1):
        return True

    return False

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
    drawPortal(app, canvas)
    drawPlayer(app, canvas)
    drawGhost(app, canvas)
    drawStartScreen(app, canvas)
    drawGameOver(app, canvas)

if __name__ == '__main__':
    runApp(width=620, height=620)
