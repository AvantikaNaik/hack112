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
    
    app.counter = 0

    app.goUp = False
    app.goDown = False
    app.goLeft = False
    app.goRight = False

    app.dx = 0
    app.dy = 0

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
    row = (y - app.dy - app.margin) // app.cellSize
    col = (x - app.dx - app.margin) // app.cellSize
    return (int(row), int(col))

def keyPressed(app, event):
    if(event.key == 'Up'):
        app.goUp = True
    if(event.key == 'Down'):
        app.goDown = True
    if(event.key == 'Left'):
        app.goLeft = True
    if(event.key == 'Right'):
        app.goRight = True

def timerFired(app):
    nearLines = getNearLines(app)
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
    if(event.key == 'Down'):
        app.goDown = False
    if(event.key == 'Left'):
        app.goLeft = False
    if(event.key == 'Right'):
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
        cell = app.cells[row][col]
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


def drawDeadEnds(app, canvas):
    for end in app.newDE:
        (x0, y0, x1, y1) = getCellBounds(app, end[0], end[1])
        canvas.create_oval(x0 + app.r, y0 + app.r ,x1 - app.r ,y1 - app.r, fill = 'blue')
    
def drawPlayer(app, canvas):
    canvas.create_rectangle(app.pX - app.pR, app.pY - app.pR, app.pX + app.pR, app.pY + app.pR, fill = 'orange')

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
    runApp(width=600, height=600)
