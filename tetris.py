from cmu_graphics import *
import random

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 65
    app.boardTop = 50
    app.boardWidth = 270
    app.boardHeight = 330
    app.cellBorderWidth = 2
    app.counter = 0
    app.paused = False
    app.score = 0
    app.gameOver = False
    app.nextPieceIndex = 0
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadTetrisPieces(app)
    loadNextPiece(app)
    
def resetGame(app):
    app.counter = 0
    app.score = 0
    app.gameOver = False
    app.nextPieceIndex = 0
    app.board = [([None] * app.cols) for row in range(app.rows)]
    loadNextPiece(app)
    
    
def loadTetrisPieces(app):
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]
                              
def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    app.pieceLeftCol = (app.cols - len(app.piece[0]))//2
    if not pieceIsLegal(app):
        app.gameOver = True
    
def loadNextPiece(app):
    loadPiece(app, app.nextPieceIndex)
    app.nextPieceIndex = random.randrange(len(app.tetrisPieces))

def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if not pieceIsLegal(app):
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    return True

def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldRows = len(app.piece)
    oldCols = len(app.piece[0])
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    
    centerRow = oldTopRow + len(app.piece)//2
    centerCol = oldLeftCol + len(app.piece[0])//2
    
    app.piece = rotate2dListClockwise(app.piece)
    
    app.pieceTopRow = centerRow - len(app.piece)//2
    app.pieceLeftCol = centerCol - len(app.piece[0])//2
    if not pieceIsLegal(app):
            app.piece = oldPiece
            app.pieceTopRow = oldTopRow
            app.pieceLeftCol = oldLeftCol
    
def pieceIsLegal(app):
    if (app.pieceTopRow < 0 or app.pieceTopRow+len(app.piece) > app.rows):
        return False
    if (app.pieceLeftCol < 0 or app.pieceLeftCol+len(app.piece[0]) > app.cols):
        return False
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col] == True:
                if app.board[app.pieceTopRow+row][app.pieceLeftCol+col] != None:
                    return False
    return True
    
def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
    
def placePieceOnBoard(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col] == True:
                app.board[app.pieceTopRow+row][app.pieceLeftCol+col] = app.pieceColor 
    
def drawPiece(app):
    for row in range(len(app.piece)):
        for col in range(len(app.piece[0])):
            if app.piece[row][col] == True:
                drawCell(app, app.pieceTopRow+row, app.pieceLeftCol+col, app.pieceColor)

def redrawAll(app):
    if not app.gameOver:
        drawLabel('TETRIS!', 200, 20, size=16)
        drawLabel(f'Score: {str(app.score)}', 200, 40, size=12)
        drawBoard(app)
        drawPiece(app)
        drawBoardBorder(app)
    else:
        drawLabel('Game Over!', 200, 200, size=24)
        drawLabel('Press s to start over', 200, 230, size=16)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    
def onKeyPress(app, key):
    if key == 'p':
        app.paused = not app.paused
    if not app.paused:
        if key == 'left':
            movePiece(app, 0, -1)
        if key == 'right':
            movePiece(app, 0, +1)
        if key == 'up':
            rotatePieceClockwise(app)
        if key == 'space':
            hardDropPiece(app)
        if key == 's' and app.gameOver:
            resetGame(app)
        
def onStep(app):
    app.counter += 1
    if (app.counter % 8 == 0) and not app.paused:
        takeStep(app)
        
def takeStep(app):
    if not movePiece(app, +1, 0):
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)
    
def removeFullRows(app):
    i = len(app.board) - 1
    removals = 0
    while i >= 0:
        if None not in app.board[i]:
            app.board.pop(i)
            removals += 1
        i -= 1
    
    app.score += 100 * (removals**2)
    emptyRows = [([None]*len(app.board[0])) for row in range(removals)]
    app.board = emptyRows + app.board
        
def rotate2dListClockwise(L):
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    M = [([None]*newCols) for row in range(newRows)]
    counter = -1
    for oldRow in range(oldRows-1, -1, -1):
        counter += 1
        for oldCol in range(oldCols):
            newRow = oldCol
            newCol = counter
            M[newRow][newCol] = L[oldRow][oldCol]
    return M

def main():
    runApp()

main()