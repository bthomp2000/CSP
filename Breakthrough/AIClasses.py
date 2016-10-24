import abc
from BoardClasses import *

class Player(object):
    __metaclass__ = abc.ABCMeta
    color = Color.white
    totalNodesExpanded = 0
    opponentWorkersCaptured = 0
    totalTimeTaken = 0
    numberOfMoves = 0
    gameTreeNodesExpanded=0;

    @abc.abstractmethod
    def makeMove(self, board, otherPlayer):
        """Analyzes the board state and returns a Movement for this player"""
        return

    def offensiveEvaluate(self, board, otherPlayer):
        playerPieces = board.findPlayerPieces()
        result = board.isGameOver()
        if result[0]:
            if result[1] == self.color:
                return 9999
            else:
                return -9999
        total = 0
        #total += 1 * len(self.playerPieces)
        total -= 10 * len(playerPieces[otherPlayer.color])
        for pieceLocation in playerPieces[self.color]:
            if self.color == Color.white:
                total += 2 * pieceLocation[0]
            else:
                total += 2 * (board.dimension - (pieceLocation[0]+1))
        return total

    def defensiveEvaluate(self, board, otherPlayer):
        playerPieces = board.findPlayerPieces()
        result = board.isGameOver()
        if result[0]:
            if result[1] == self.color:
                return 9999
            else:
                return -9999
        total = 0
        total += 10 * len(playerPieces[self.color])
        #total -= 1 * len(otherPlayer.playerPieces)
        for pieceLocation in playerPieces[otherPlayer.color]:
            if otherPlayer.color == Color.white:
                total -= 2 * pieceLocation[0]
            else:
                total -= 2 * (board.dimension - (pieceLocation[0]+1))
        return total

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
        print "game tree nodes expanded so far: ",self.gameTreeNodesExpanded

        bestMove = self.minimax(board, 3, True, otherPlayer)[1]
        board.makeMovement(self, bestMove)

    def minimax(self, board, depth, isThisPlayerMoving, otherPlayer):
        if board.isGameOver()[0] or depth == 0:
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
                self.gameTreeNodesExpanded+=1
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
                self.gameTreeNodesExpanded+=1
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
                self.gameTreeNodesExpanded+=1
                vPrime = self.minimax(board, depth-1, not isThisPlayerMoving, otherPlayer)[0]
                if isThisPlayerMoving and vPrime > v:
                    v = vPrime
                    bestMove = rightForward
                elif not isThisPlayerMoving and vPrime < v:
                    v = vPrime
                    bestMove = rightForward
                board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
        #print "value: ",v
        return (v, bestMove)


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
        # print "game tree nodes expanded so far: ",self.gameTreeNodesExpanded
        bestMove = self.minimax(board, 3, -999999,999999,True, otherPlayer)[1]
        board.makeMovement(self, bestMove)

    def minimax(self, board, depth, minVal, maxVal, isThisPlayerMoving, otherPlayer):
        if board.isGameOver()[0] or depth == 0:
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
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = leftForward
                    if v > maxVal:
                        board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
                        return (maxVal,bestMove)
                else: #we are a min node
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = leftForward
                    if v < minVal:
                        board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
                        return (minVal,bestMove)
                board.undoMovement(currentPlayer, leftForward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, forward):
                oldDestinationPiece = board.makeMovement(currentPlayer, forward)
                vPrime = 0
                if isThisPlayerMoving:
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = forward
                    if v > maxVal:
                        board.undoMovement(currentPlayer, forward, oldDestinationPiece)
                        return (maxVal,bestMove)
                else:
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = forward
                    if v < minVal:
                        board.undoMovement(currentPlayer, forward, oldDestinationPiece)
                        return (minVal,bestMove)
                board.undoMovement(currentPlayer, forward, oldDestinationPiece)
            if board.isValidMove(currentPlayer, rightForward):
                oldDestinationPiece = board.makeMovement(currentPlayer, rightForward)
                vPrime = 0
                if isThisPlayerMoving:
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, v,maxVal,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime > v:
                        v = vPrime
                        bestMove = rightForward
                    if v > maxVal:
                        board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
                        return (maxVal,bestMove)
                else:
                    self.gameTreeNodesExpanded+=1
                    vPrime = self.minimax(board, depth-1, minVal,v,not isThisPlayerMoving, otherPlayer)[0]
                    if vPrime < v:
                        v = vPrime
                        bestMove = rightForward
                    if v < minVal:
                        board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
                        return (minVal,bestMove)
                board.undoMovement(currentPlayer, rightForward, oldDestinationPiece)
        return (v, bestMove)

