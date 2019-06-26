import logging, math, random
from itertools import chain, tee
from move import Move

"""
Agent for Piranhas.
"""


class PiranhasAgent:
    def __init__(self):
        self.me = None
        self.memento = None

    def setPlayer(self, player):
        logging.info('I am %s', player)
        self.me = player

    def updateMemento(self, memento):
        self.memento = memento

    @staticmethod
    def fishCenter(fish):
        iters = tee(fish, 4)
        minX = min(f[0] for f in iters[0])
        maxX = max(f[0] for f in iters[1])
        minY = min(f[1] for f in iters[2])
        maxY = max(f[1] for f in iters[3])
        return ((minX + maxX) / 2.0, (minY + maxY) / 2.0)

    @staticmethod
    def distanceScore(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def requestMove(self):
        board = self.memento.board

        # get current situation
        mySwarms = list(board.swarms(self.me))
        currentSwarmCount = len(mySwarms)
        swarmsCenter = PiranhasAgent.fishCenter(PiranhasAgent.fishCenter(s) for s in mySwarms)

        # create copy of current board for move evaluation
        evalBoard = board.copy()

        bestMoveScore = 0
        bestMove = None

        # iterate fish (in swarms)
        for swarm in mySwarms:
            swarmSize = len(swarm)
            swarmCenter = PiranhasAgent.distanceScore(PiranhasAgent.fishCenter(swarm), swarmsCenter)
            for fish in swarm:
                # iterate possible moves of fish
                for direction in board.possibleMoves(*fish):
                    target = evalBoard.move(fish, direction)
                    # fish to center of swarms
                    distributionChange = PiranhasAgent.distanceScore(fish, swarmsCenter) \
                                         - PiranhasAgent.distanceScore(target, swarmsCenter)
                    targetSwarm = evalBoard.swarmAt(target)
                    if evalBoard.swarmCount(self.me) == 1:
                        # one swarm is good
                        distributionChange *= 10
                    elif swarmCenter < 2:
                        # not move fish, if in a swarm near center
                        distributionChange *= 0.6
                    elif len(targetSwarm) > swarmSize:
                        # hold fish together
                        distributionChange *= 1.7 if swarmSize == 1 else 1.2
                    # reset evaluation board
                    evalBoard.stateSet(*fish, board.stateAt(*fish))
                    evalBoard.stateSet(*target, board.stateAt(*target))
                    # find best move
                    if distributionChange > bestMoveScore:
                        bestMoveScore = distributionChange
                        bestMove = Move(*fish, direction)

        return bestMove

# -*- encoding: utf-8-unix -*-
