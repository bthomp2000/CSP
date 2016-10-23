from enum import Enum

class Color(Enum):
    white = 0
    black = 1

class Piece:
    color = Color.white

    def __init__(self, color=Color.white):
        self.color = color


class Square:
    piece = None

    def __init__(self, piece=None):
        self.piece = piece

    def hasPiece(self):
        return self.piece is not None


class Board:
    grid = [] #A grid of Squares with arrangement [row][col]. Bottom-left is [0][0]
    dimension = 0 #The dimension of the game board. For example, 8 means an 8x8 board
    playerPieces = {}

    def __init__(self, dimension=8):
        assert dimension >= 4
        self.dimension = dimension
        self.initializeGrid(dimension)

    def initializeGrid(self, dimension):
        self.grid=[]
        for i in range(0,dimension):
            self.grid.append([])
            for j in range(0,dimension):
                self.grid[i].append(Square(None))

    def setPiece(self, row, col, piece):
        self.grid[row][col].piece = piece

    def getPiece(self, row, col):
        return self.grid[row][col].piece

    def isPointOnBoard(self, row, col):
        isOffBoard = row < 0 or col < 0 or row >= self.dimension or col >= self.dimension
        return not isOffBoard

    def printBoard(self):
        for row in reversed(range(0, self.dimension)):
            for col in range(0, self.dimension):
                if self.getPiece(row,col) == None:
                    print ' ',
                elif self.getPiece(row,col).color == Color.white:
                    print 'W',
                else:
                    print 'B',
            print ''
        print '------------------'

    def isGameOver(self):
        #Has either side has reached the opposing side's last row
        for col in range(0, self.dimension):
            checkPieceTop = self.getPiece(self.dimension - 1, col)
            if checkPieceTop is not None and checkPieceTop.color == Color.white:
                return (True, Color.white)
            checkPieceBottom = self.getPiece(0, col)
            if checkPieceBottom is not None and checkPieceBottom.color == Color.black:
                return (True, Color.black)
        #Check that each side has pieces left on the board
        blackPiecesLeft = False
        whitePiecesLeft = False
        for row in range(0, self.dimension):
            for col in range(0, self.dimension):
                checkPiece = self.getPiece(row, col)
                if checkPiece is not None:
                    if checkPiece.color == Color.white:
                        whitePiecesLeft = True
                    else:
                        blackPiecesLeft = True
        if not blackPiecesLeft:
            return (True, Color.white)
        if not whitePiecesLeft:
            return (True, Color.black)
        return (False, None)

    def makeMovement(self, playerMoving, movement):
        if self.isValidMove(playerMoving, movement):
            defendingPiece = self.getPiece(movement.destination[0], movement.destination[1])
            movingPiece = self.getPiece(movement.origin[0], movement.origin[1])
            self.setPiece(movement.destination[0], movement.destination[1], movingPiece)
            self.setPiece(movement.origin[0], movement.origin[1], None)
            return defendingPiece

    def undoMovement(self, playerMoving, movement, destinationPiece):
        movingPiece = self.getPiece(movement.destination[0], movement.destination[1])
        self.setPiece(movement.origin[0], movement.origin[1], movingPiece)
        self.setPiece(movement.destination[0], movement.destination[1], destinationPiece)

    def findPlayerPieces(self):
        playerPieces = {}
        playerPieces[Color.white] = []
        playerPieces[Color.black] = []
        for row in range(0, self.dimension):
            for col in range(0, self.dimension):
                currPiece = self.getPiece(row, col)
                if currPiece is not None:
                    playerPieces[currPiece.color].append((row, col))
        return playerPieces

    def isValidMove(self, playerMoving, movement):
        playerColor = playerMoving.color
        origin = movement.origin
        destination = movement.destination
        if not self.isPointOnBoard(origin[0], origin[1]) or not self.isPointOnBoard(destination[0], destination[1]):
            return False
        movingPiece = self.getPiece(origin[0], origin[1])
        if movingPiece is None or movingPiece.color is not playerColor:
            return False
        # Pieces can only move forwards
        if playerColor is Color.white and origin[0] > destination[0]:
            return False
        elif playerColor is Color.black and origin[0] < destination[0]:
            return False
        if abs(origin[1] - destination[1]) > 1:
            return False
        defendingPiece = self.getPiece(destination[0], destination[1])
        if defendingPiece is not None:
            if defendingPiece.color is playerColor:
                return False
            if origin[1] == destination[1]:
                return False
        return True


class Movement:
    origin = (0, 0)
    destination = (0,0)

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
