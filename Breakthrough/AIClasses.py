import abc
from Breakthrough.BoardClasses import *

class Player(object):
    __metaclass__ = abc.ABCMeta
    color = Color.white
    totalNodesExpanded = 0
    opponentWorkersCaptured = 0
    totalTimeTaken = 0
    numberOfMoves = 0

    @abc.abstractmethod
    def makeMove(self, board):
        """Analyzes the board state and returns a Movement for this player"""
        return
