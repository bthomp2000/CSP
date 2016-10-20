import abc
from Breakthrough.BoardClasses import *

class Player(object):
    __metaclass__ = abc.ABCMeta
    color = Color.white

    @abc.abstractmethod
    def makeMove(self, board):
        """Analyzes the board state and returns a Movement for this player"""
        return
