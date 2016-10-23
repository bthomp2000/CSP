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

    def __init__(self, isOffensive, color):
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
        print "value: ",v
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

# (* the minimax value of n, searched to depth d.
#  * If the value is less than min, returns min.
#  * If greater than max, returns max. *)
#  fun minimax(n: node, d: int, min: int, max: int): int =
#    if leaf(n) or depth=0 return evaluate(n)
#    if n is a max node
#       v := min
#       for each child of n
#          v' := minimax (child,d-1,v,max)
#          if v' > v, v:= v'
#          if v > max return max
#       return v
#    if n is a min node
#       v := max
#       for each child of n
#          v' := minimax (child,d-1,min,v)
#          if v' < v, v:= v'
#          if v < min return min
#       return v

class AlphaBetaPlayer(Player):
    isOffensive = True

    def __init__(self, isOffensive,color):
        self.isOffensive = isOffensive
        self.color = color

    def makeMove(self, board, otherPlayer):
        bestMove = self.minimax(board, 3, -999999,999999,True, otherPlayer)[1]
        board.makeMovement(self, bestMove)

    def minimax(self, board, depth, minVal, maxVal, isThisPlayerMoving, otherPlayer):
        if board.isGameOver() or depth == 0:
            # print depth
            if self.isOffensive:
                return (self.offensiveEvaluate(board, otherPlayer), None)
            else:
                return (self.defensiveEvaluate(board, otherPlayer), None)
        currentPlayer = None
        v = minVal
        bestMove = None
        if isThisPlayerMoving:
            currentPlayer = self
        else:
            currentPlayer = otherPlayer
            v = maxVal
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
                vPrime = 0
                if isThisPlayerMoving: #we are a max node
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = leftForward
                    if v > maxVal: #we are a min node
                        return (maxVal,bestMove)
                else:
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = leftForward
                    if v < minVal:
                        return (minVal,bestMove)
                board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, forward):
                oldDestinationPiece = board.makeMovement(currentPlayer, forward)
                vPrime = 0
                if isThisPlayerMoving:
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = forward
                    if v > maxVal:
                        return (maxVal,bestMove)
                else:
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = forward
                    if v < minVal:
                        return (minVal,bestMove)
                board.undoMovement(currentPlayer, forward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, rightForward):
                oldDestinationPiece = board.makeMovement(currentPlayer, rightForward)
                vPrime = 0
                if isThisPlayerMoving:
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = rightForward
                    if v > maxVal:
                        return (maxVal,bestMove)
                else:
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = rightForward
                    if v < minVal:
                        return (minVal,bestMove)
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