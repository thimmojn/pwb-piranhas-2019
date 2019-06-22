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

    def myCenter(self):
        swarms = self.memento.board.swarms(self.me)
        # center of swarm centers
        return PiranhasAgent.fishCenter(PiranhasAgent.fishCenter(s) for s in swarms)

    def moveScore(self, currentCenter, currentSwarms, fishSwarmSize, fish, direction):
        score = 0
        testBoard = self.memento.board.copy()
        target = testBoard.move(fish, direction)
        if PiranhasAgent.distanceScore(target, currentCenter) < PiranhasAgent.distanceScore(fish, currentCenter):
            score += 1
        if testBoard.swarmSize(target) > fishSwarmSize:
            score += 1 if self.memento.turn >= 30 else 0
        if testBoard.swarmCount() < currentSwarms:
            score += 2 if self.memento.turn >= 50 else 0
        return score

    def requestMove(self):
        board = self.memento.board

        currentCenter = self.myCenter()
        currentSwarms = board.swarmCount(self.me)
        logging.info('current center: %f,%f', currentCenter[0], currentCenter[1])

        myFish = [
            ((x, y), board.swarmSize((x, y)), board.possibleMoves(x, y))
            for (_p, x, y) in board.fishCoordinates(self.me)
        ]

        allMoves = list(chain.from_iterable(
            ((fish, m, self.moveScore(currentCenter, currentSwarms, swarmSize, fish, m)) for m in moves)
            for (fish, swarmSize, moves) in myFish
        ))

        scoreSum = sum(m[2] for m in allMoves)
        selectScore = random.randrange(scoreSum)
        i = 0
        for m in allMoves:
            i += m[2]
            if i >= selectScore:
                return Move(m[0][0], m[0][1], m[1])

# -*- encoding: utf-8-unix -*-
