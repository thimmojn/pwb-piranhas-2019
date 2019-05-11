import random
from move import Move

"""
Agent for Piranhas.
"""


def PiranhasAgent:
    def __init__(self):
        self.me = None
        self.memento = None

    def setPlayer(self, player):
        self.me = player

    def updateMemento(self, memento):
        self.memento = memento

    def requestMove(self):
        board = self.memento.board
        # find fish, which can move
        myFish = [
            (x, y)
            for x in range(board.colums)
            for y in range(board.rows)
            if board.get(x, y).occupiedBy(self.me)
            and len(board.possibleMoves(x, y)) > 0
        ]
        # select one by chance
        playFish = myFish[random.randrange(len(myFish))]
        # determine possible moves
        fishMoves = board.possibleMoves(*playFish)
        # select one by chance
        playMove = fishMoves[random.randrange(len(fishMoves))]
        return Move(playFish[0], playFish[1], playMove)

# -*- encoding: utf-8-unix -*-
