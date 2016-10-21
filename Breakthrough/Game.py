from Breakthrough.BoardClasses import Board, Color
from Breakthrough.AIClasses import *

class Game:
    player1 = None
    player2 = None
    board = None
    turnNumber = 0

    def __init__(self, player1, player2, boardDimension):
        self.player1 = player1
        self.player2 = player2
        self.board = Board(boardDimension)
        self.turnNumber = 0
        self.setUpInitialBoardState()

    def setUpInitialBoardState(self):
        boardDimension = self.board.dimension
        #Set up top of board
        for row in range(0, 2):
            for col in range(0, boardDimension):
                self.board.setPiece(row, col, Piece(Color.black))
        #Set up bottom of board
        for row in range(boardDimension - 2, boardDimension):
            for col in range(0, boardDimension):
                self.board.setPiece(row, col, Piece(Color.white))