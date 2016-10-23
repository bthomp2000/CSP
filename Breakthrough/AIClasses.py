import abc
from Breakthrough.BoardClasses import *

class Player(object):
    __metaclass__ = abc.ABCMeta
    color = Color.white
    totalNodesExpanded = 0
    opponentWorkersCaptured = 0
    totalTimeTaken = 0
    numberOfMoves = 0
    playerPieces = []

    @abc.abstractmethod
    def makeMove(self, board):
        """Analyzes the board state and returns a Movement for this player"""
        return

# (* the minimax value of n, searched to depth d *)
#  fun minimax(n: node, d: int): int =
#    if leaf(n) or depth=0 return evaluate(n)
#    if n is a max node
#       v := L
#       for each child of n
#          v' := minimax (child,d-1)
#          if v' > v, v:= v'
#       return v
#    if n is a min node
#       v := W
#       for each child of n
#          v' := minimax (child,d-1)
#          if v' < v, v:= v'
#       return v

class MinimaxPlayer(Player):
    isOffensive = True

    def __init__(self, isOffensive):
        super.__init__()
        self.isOffensive = isOffensive

    def minimax(self, board, depth, isThisPlayerMoving, otherPlayer):
        if board.isGameOver() is True or depth == 0:
            if self.isOffensive:
                self.offensiveEvaluate(board, otherPlayer)
            else:
                self.defensiveEvaluate(board, otherPlayer)
        currentPlayer = None
        if isThisPlayerMoving:
            currentPlayer = self
        else:
            currentPlayer = otherPlayer
        v = -999999
        for pieceLocation in currentPlayer.playerPieces:
            upValue = 0
            if currentPlayer.color == Color.white:
                upValue = 1
            else:
                upValue = -1
            leftForward = Movement(pieceLocation, (pieceLocation[0] + upValue, pieceLocation[1] - 1))
            forward = Movement(pieceLocation, (pieceLocation[0] + upValue, pieceLocation[1]))
            rightForward = Movement(pieceLocation, (pieceLocation[0] + upValue, pieceLocation[1] + 1))
            if board.isValidMove(currentPlayer, leftForward):
                oldDestinationPiece = board.makeMovement(currentPlayer, leftForward)
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, forward):
                oldDestinationPiece = board.makeMovement(currentPlayer, forward)
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                board.undoMovement(currentPlayer, forward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, rightForward):
                oldDestinationPiece = board.makeMovement(currentPlayer, rightForward)
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
        return v

    def offensiveEvaluate(self, board, otherPlayer):
        total = 0
        #total += 1 * len(self.playerPieces)
        total -= 1 * len(otherPlayer.playerPieces)
        for pieceLocation in self.playerPieces:
            if self.color == Color.white:
                total += 1 * pieceLocation[0]
            else:
                total += 1 * (board.dimension - (pieceLocation[0]+1))

    def defensiveEvaluate(self, board, otherPlayer):
        total = 0
        total += 1 * len(self.playerPieces)
        #total -= 1 * len(otherPlayer.playerPieces)
        for pieceLocation in otherPlayer.playerPieces:
            if otherPlayer.color == Color.white:
                total -= 1 * pieceLocation[0]
            else:
                total -= 1 * (board.dimension - (pieceLocation[0]+1))


class AlphaBetaPlayer(Player):