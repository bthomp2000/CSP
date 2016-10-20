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
    grid = [] #A grid of Squares with arrangement [row][col]

    def __init__(self, dimension=8):
        self.initializeGrid(dimension)

    def initializeGrid(self, dimension):
        grid=[]
        for i in range(0,dimension):
            grid.append([])
            for j in range(0,dimension):
                grid.append(Square(None))

    def setPiece(self, row, col, piece):
        self.grid[row][col].piece = piece


class Movement:
    origin = (0, 0)
    destination = (0,0)

    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

#def mainLoop(Agent1, Agent2):