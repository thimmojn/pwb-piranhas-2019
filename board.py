import enum, lxml.etree
from functools import partial, reduce
from itertools import chain
from move import MoveDirection
from player import Player

"""
Board of Piranhas game.
"""


class FieldState(enum.Enum):
    Empty = 'EMPTY'
    Red = 'RED'
    Blue = 'BLUE'
    Obstructed = 'OBSTRUCTED'

    @classmethod
    def byChar(cls, char):
        return next(f for (f, c) in FieldStateCharMapping.items() if c == char)

    @property
    def char(self):
        return FieldStateCharMapping.get(self)

    def occupiedBy(self, player):
        fieldPlayer = self.toPlayer()
        return fieldPlayer is not None and (player is fieldPlayer or player is None)

    def toPlayer(self):
        try:
            return Player(self.value)
        except ValueError:
            return None

# assign field state a character (for testing and debugging)
FieldStateCharMapping = {
    FieldState.Empty:      '_',
    FieldState.Red:        'R',
    FieldState.Blue:       'B',
    FieldState.Obstructed: 'O'
}


class Board:
    def __init__(self, columns, rows):
        self.fields = [[FieldState.Empty for y in range(rows)] for x in range(columns)]

    @property
    def columns(self):
        return len(self.fields)

    @property
    def rows(self):
        return len(self.fields[0])

    @classmethod
    def fromXML(cls, boardNode):
        iterFields = lxml.etree.XPath('fields/field')
        columns = max(int(n.get('x')) for n in iterFields(boardNode)) + 1
        rows = max(int(n.get('y')) for n in iterFields(boardNode)) + 1
        board = cls(columns, rows)
        for fieldNode in iterFields(boardNode):
            board.stateSet(
                int(fieldNode.get('x')),
                int(fieldNode.get('y')),
                FieldState(fieldNode.get('state'))
            )
        return board

    @classmethod
    def fromString(cls, boardString):
        fields = boardString.split('\n')
        columns = len(fields[0])
        rows = len(fields)
        board = cls(columns, rows)
        for x in range(columns):
            for y in range(rows):
                board.stateSet(x, y, FieldState.byChar(fields[rows - y - 1][x]))
        return board

    def isValidCoordinate(self, x, y):
        return x >= 0 and x < self.columns and y >= 0 and y < self.rows

    def stateAt(self, x, y):
        return self.fields[x][y]

    def stateSet(self, x, y, state):
        self.fields[x][y] = state

    def move(self, fish, direction):
        target = direction + fish
        self.stateSet(*target, self.stateAt(*fish))
        self.stateSet(*fish, FieldState.Empty)
        return target

    def copy(self):
        board = Board(self.columns, self.rows)
        for x in range(self.columns):
            for y in range(self.rows):
                board.stateSet(x, y, self.stateAt(x, y))
        return board

    @staticmethod
    def fishCounter(fields, player=None):
        return sum(1 for field in fields if field.occupiedBy(player))

    def fishCount(self, player=None):
        return Board.fishCounter(chain.from_iterable(self.fields), player)

    def fishCoordinates(self, player=None):
        """Generator of coordinates of fish by player."""
        for x in range(self.columns):
            for y in range(self.rows):
                field = self.stateAt(x, y)
                if field.occupiedBy(player):
                    yield (field.toPlayer(), x, y)

    def iterateFields(self, origin, direction, until=lambda _x, _y: False):
        x, y = origin
        while self.isValidCoordinate(x, y) and not until(x, y):
            yield self.stateAt(x, y)
            x, y = direction + (x, y)

    def movePossible(self, x, y, direction):
        if not self.stateAt(x, y).occupiedBy(None):
            # field not occupied by a player, no move is possible
            return False

        # steps are the sum of fish on a line across board constructed by direction
        # fish at origin is counted twice
        steps = Board.fishCounter(self.iterateFields((x, y), direction)) \
            + Board.fishCounter(self.iterateFields((x, y), direction.inverse)) \
            - 1
        # calculate target coordinates given by steps in direction
        directionShift = direction.shift
        target = (x + steps * directionShift[0], y + steps * directionShift[1])

        # check if move ends outside board
        # or on a field with an obstructed
        # or on a field with an own fish
        if not self.isValidCoordinate(*target) \
           or self.stateAt(*target) is FieldState.Obstructed \
           or self.stateAt(*target) is self.stateAt(x, y):
            return False

        # check if there is a enemy fish in the way
        if any(
                # occupied fields with not own fish are enemies
                f.occupiedBy(None) and f is not self.stateAt(x, y)
                # search until target reached, target will be skipped
                for f in self.iterateFields((x, y), direction, lambda fx, fy: (fx, fy) == target)
        ):
            return False

        # otherwise move is allowed
        return True

    def possibleMoves(self, x, y):
        return list(filter(partial(self.movePossible, x, y), MoveDirection))

    def __determineSwarm(self, origin, player, swarm=set()):
        # a swarm member must have a valid coordinate,
        # owned by given player
        # and not already part of it
        if self.isValidCoordinate(*origin) and self.stateAt(*origin).occupiedBy(player) and origin not in swarm:
            # add fish to swarm and search for other members in neighborhood
            return reduce(
                lambda s, d: self.__determineSwarm(d + origin, player, s),
                MoveDirection,
                {*swarm, origin}
            )
        else:
            # otherwise stop recursion and return accumulator
            return swarm

    def swarmAt(self, coordinate):
        return self.__determineSwarm(coordinate, self.stateAt(*coordinate).toPlayer())

    def swarmSize(self, coordinate):
        return len(self.swarmAt(coordinate))

    def swarms(self, player=None):
        fish = set(self.fishCoordinates(player))
        while fish:
            fishPlayer, x, y = next(iter(fish))
            aSwarm = self.__determineSwarm((x, y), fishPlayer)
            yield aSwarm
            fish -= {(fishPlayer, *f) for f in aSwarm}

    def swarmCount(self, player=None):
        return sum(1 for s in self.swarms(player))

    def __repr__(self):
        return '\n'.join(''.join(self.stateAt(x, y).char for x in range(self.columns)) for y in reversed(range(self.rows)))

# -*- encoding: utf-8-unix -*-
