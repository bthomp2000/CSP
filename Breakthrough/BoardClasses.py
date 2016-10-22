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

    def __init__(self, dimension=8):
        assert dimension >= 4
        self.dimension = dimension
        self.initializeGrid(dimension)

    def initializeGrid(self, dimension):
        grid=[]
        for i in range(0,dimension):
            grid.append([])
            for j in range(0,dimension):
                grid.append(Square(None))

    def setPiece(self, row, col, piece):
        self.grid[row][col].piece = piece

    def getPiece(self, row, col):
        return self.grid[row][col].piece

    def isPointOnBoard(self, row, col):
        isOffBoard = row < 0 or col < 0 or row >= self.dimension or col >= self.dimension
        return not isOffBoard


class Movement:
    origin = (0, 0)
    destination = (0,0)

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
