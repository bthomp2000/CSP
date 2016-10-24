from BoardClasses import Board, Color, Movement, Piece
from AIClasses import Player, MinimaxPlayer, AlphaBetaPlayer, GreedyPlayer
import time

class Game:
    player1 = None #White
    player2 = None #Black
    board = None
    turnNumber = 0

    def __init__(self, player1, player2, boardRows, boardCols):
        self.player1 = player1
        self.player2 = player2
        self.board = Board(boardRows, boardCols)
        self.turnNumber = 0
        self.setUpInitialBoardState()

    def setUpInitialBoardState(self):
        #boardDimension = self.board.dimension
        boardRows = self.board.rows
        boardCols = self.board.cols
        #Set up top of board
        self.board.playerPieces[Color.white] = []
        self.board.playerPieces[Color.black] = []
        for row in range(0, 2):
            for col in range(0, boardCols):
                self.board.setPiece(row, col, Piece(Color.white))
                self.board.playerPieces[Color.white].append((row, col))
        #Set up bottom of board
        for row in range(boardRows - 2, boardRows):
            for col in range(0, boardCols):
                self.board.setPiece(row, col, Piece(Color.black))
                self.board.playerPieces[Color.black].append((row, col))

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


    def mainLoop(self):
        activePlayer = self.player1
        inactivePlayer = self.player2
        player1Time = 0
        player2Time = 0
        move1Count = 0
        move2Count = 0
        while not self.board.isGameOver()[0]:
            start_time = time.time()
            activePlayer.makeMove(self.board, inactivePlayer)
            moveTime = time.time() - start_time
            self.board.printBoard()
            if activePlayer == self.player1:
                player1Time+=moveTime
                move1Count +=1
                activePlayer = self.player2
                inactivePlayer = self.player1
            else:
                player2Time+=moveTime
                move2Count +=1
                activePlayer = self.player1
                inactivePlayer = self.player2
        player1Average = player1Time / move1Count
        player2Average = player2Time / move2Count

        print "Player 1 average: ",player1Average
        print "Player 1 total nodes expanded: ",self.player1.gameTreeNodesExpanded
        print "Player 1 average nodes expanded: ",self.player1.gameTreeNodesExpanded / move1Count
        print "Number of pieces captured by Player 1: ",16-len(self.board.playerPieces[player2.color])
        print "Number of total moves made by Player 1: ",move1Count

        print "Player 2 average: ",player2Average
        print "Player 2 total nodes expanded: ",self.player2.gameTreeNodesExpanded
        print "Player 2 average nodes expanded: ",self.player2.gameTreeNodesExpanded / move2Count
        print "Number of pieces captured by Player 2: ",16-len(self.board.playerPieces[player1.color])
        print "Number of total moves made by Player 2: ",move2Count

player1 = GreedyPlayer(True,Color.white)
player2 = AlphaBetaPlayer(False,Color.black)
mainGame = Game(player1, player2, 8, 8)
mainGame.mainLoop()