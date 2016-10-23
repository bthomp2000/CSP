from Breakthrough.BoardClasses import Board, Color, Movement, Piece
from Breakthrough.AIClasses import Player, MinimaxPlayer

class Game:
    player1 = None #White
    player2 = None #Black
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
        self.board.playerPieces[Color.white] = []
        self.board.playerPieces[Color.black] = []
        for row in range(0, 2):
            for col in range(0, boardDimension):
                self.board.setPiece(row, col, Piece(Color.black))
                self.board.playerPieces[Color.black].append((row, col))
        #Set up bottom of board
        for row in range(boardDimension - 2, boardDimension):
            for col in range(0, boardDimension):
                self.board.setPiece(row, col, Piece(Color.white))
                self.board.playerPieces[Color.white].append((row, col))

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
            if origin[1] == destination[1]:
                return False

    def isGameOver(self):
        #Has either side has reached the opposing side's last row
        for col in range(0, self.board.dimension):
            checkPieceTop = self.board.getPiece(0, col)
            if checkPieceTop is not None and checkPieceTop.color == Color.white:
                return True
            checkPieceBottom = self.board.getPiece(self.board.dimension - 1, col)
            if checkPieceBottom is not None and checkPieceBottom.color == Color.black:
                return True
        #Check that each side has pieces left on the board
        blackPiecesLeft = False
        whitePiecesLeft = False
        for row in range(0, self.board.dimension):
            for col in range(0, self.board.dimension):
                checkPiece = self.board.getPiece(row, col)
                if checkPiece is not None:
                    if checkPiece.color == Color.white:
                        whitePiecesLeft = True
                    else:
                        blackPiecesLeft = True
        if not blackPiecesLeft or not whitePiecesLeft:
            return True

    def makeMovement(self, playerMoving, movement):
        if self.isValidMove(playerMoving, movement):
            defendingPiece = self.board.getPiece(movement.destination[0], movement.destination[1])
            if defendingPiece is not None:
                playerMoving.opponentWorkersCaptured += 1
            movingPiece = self.board.getPiece(movement.origin[0], movement.origin[1])
            self.board.setPiece(movement.destination[0], movement.destination[1], movingPiece)
            self.board.setPiece(movement.origin[0], movement.origin[1], None)
        else:
            print("Not valid move")

    def mainLoop(self):
        activePlayer = self.player1
        inactivePlayer = self.player2
        while not self.isGameOver():
            movement = activePlayer.makeMove(self.board, inactivePlayer)
            self.makeMovement(activePlayer, movement)
            if activePlayer == self.player1:
                activePlayer = self.player2
                inactivePlayer = self.player1
            else:
                activePlayer = self.player1
                inactivePlayer = self.player2

player1 = MinimaxPlayer(True)
player2 = MinimaxPlayer(False)
mainGame = Game(player1, player2, 8)
mainGame.mainLoop()