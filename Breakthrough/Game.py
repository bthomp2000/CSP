from Breakthrough.BoardClasses import Board, Color, Movement, Piece
from Breakthrough.AIClasses import Player

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

    def isValidMove(self, playerMoving, movement):
        playerColor = playerMoving.color
        origin = movement.origin
        destination = movement.destination
        if not self.board.isPointOnBoard(origin[0], origin[1]) or not self.board.isPointOnBoard(destination[0], destination[1]):
            return False
        movingPiece = self.board.getPiece(origin[0], origin[1])
        if movingPiece is None or movingPiece.color is not playerColor:
            return False
        # Pieces can only move forwards
        if playerColor is Color.white and origin[0] > destination[0]:
            return False
        elif playerColor is Color.black and origin[0] < destination[0]:
            return False
        if abs(origin[1] - destination[1]) > 1:
            return False
        defendingPiece = self.board.getPiece(destination[0], destination[1])
        if defendingPiece is not None:
            if defendingPiece.color is playerColor:
                return False
        #TODO: Add logic for attacking enemies