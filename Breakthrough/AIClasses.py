import abc
from BoardClasses import *

class Player(object):
    __metaclass__ = abc.ABCMeta
    color = Color.white
    totalNodesExpanded = 0
    opponentWorkersCaptured = 0
    totalTimeTaken = 0
    numberOfMoves = 0

    @abc.abstractmethod
    def makeMove(self, board, otherPlayer):
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

    def __init__(self, isOffensive,color):
        self.isOffensive = isOffensive
        self.color = color

    def makeMove(self, board, otherPlayer):
        bestMove = self.minimax(board, 3, True, otherPlayer)[1]
        board.makeMovement(self, bestMove)

    def minimax(self, board, depth, isThisPlayerMoving, otherPlayer):
        if board.isGameOver() or depth == 0:
            # print depth
            if self.isOffensive:
                return (self.offensiveEvaluate(board, otherPlayer), None)
            else:
                return (self.defensiveEvaluate(board, otherPlayer), None)
        currentPlayer = None
        v = -999999
        bestMove = None
        if isThisPlayerMoving:
            currentPlayer = self
        else:
            currentPlayer = otherPlayer
            v = 999999
        playerPieces = board.findPlayerPieces()
        for pieceLocation in playerPieces[currentPlayer.color]:
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
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)[0]
                # print vPrime
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                    bestMove = leftForward
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                    bestMove = leftForward
                board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, forward):
                oldDestinationPiece = board.makeMovement(currentPlayer, forward)
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)[0]
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                    bestMove = forward
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                    bestMove = forward
                board.undoMovement(currentPlayer, forward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, rightForward):
                oldDestinationPiece = board.makeMovement(currentPlayer, rightForward)
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)[0]
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                    bestMove = rightForward
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                    bestMove = rightForward
                board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
        return (v, bestMove)

    def offensiveEvaluate(self, board, otherPlayer):
        playerPieces = board.findPlayerPieces()
        total = 0
        #total += 1 * len(self.playerPieces)
        total -= 1 * len(playerPieces[otherPlayer.color])
        for pieceLocation in playerPieces[self.color]:
            if self.color == Color.white:
                total += 1 * pieceLocation[0]
            else:
                total += 1 * (board.dimension - (pieceLocation[0]+1))
        return total

    def defensiveEvaluate(self, board, otherPlayer):
        playerPieces = board.findPlayerPieces()
        total = 0
        total += 1 * len(playerPieces[self.color])
        #total -= 1 * len(otherPlayer.playerPieces)
        for pieceLocation in playerPieces[otherPlayer.color]:
            if otherPlayer.color == Color.white:
                total -= 1 * pieceLocation[0]
            else:
                total -= 1 * (board.dimension - (pieceLocation[0]+1))
        return total

#class AlphaBetaPlayer(Player):