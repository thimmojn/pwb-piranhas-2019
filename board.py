import enum, lxml.etree
from functools import partial
from itertools import chain
from move import MoveDirection

"""
Board of Piranhas game.
"""


class FieldState(enum.Enum):
    Empty = 'EMPTY'
    Red = 'RED'
    Blue = 'BLUE'
    Obstructed = 'OBSTRUCTED'

    def occupiedBy(self, player):
        return (player is not None and self is FieldState(player.value)) \
            or (player is None and self in {FieldState.Red, FieldState.Blue})

    def asChar(self):
        if self is FieldState.Empty:
            return '_'
        elif self is FieldState.Red:
            return 'R'
        elif self is FieldState.Blue:
            return 'B'
        elif self is FieldState.Obstructed:
            return 'O'
        else:
            raise ValueError('no character for {} given'.format(self.name))


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
            board.set(
                int(fieldNode.get('x')),
                int(fieldNode.get('y')),
                FieldState(fieldNode.get('state'))
            )

        return board

    def isValidCoordinate(self, x, y):
        return x >= 0 and x < self.columns and y >= 0 and y < self.rows

    def get(self, x, y):
        return self.fields[x][y]

    def set(self, x, y, state):
        self.fields[x][y] = state

    def copy(self):
        pass

    @staticmethod
    def fishCounter(fields, player=None):
        return sum(1 for field in fields if field.occupiedBy(player))

    def fishCount(self, player=None):
        return Board.fishCounter(chain.from_iterable(self.fields), player)

    def iterateFields(self, origin, direction, until=lambda _x, _y: False):
        x, y = origin
        shiftX, shiftY = direction
        while self.isValidCoordinate(x, y) and not until(x, y):
            yield self.get(x, y)
            x, y = x + shiftX, y + shiftY

    def movePossible(self, x, y, direction):
        if not self.get(x, y).occupiedBy(None):
            # field not occupied by a player, no move is possible
            return False

        directionShift = direction.shift
        inverseShift = (-directionShift[0], -directionShift[1])
        # steps are the sum of fish on a line across board constructed by direction
        # fish at origin is counted twice
        steps = Board.fishCounter(self.iterateFields((x, y), directionShift)) \
            + Board.fishCounter(self.iterateFields((x, y), inverseShift)) \
            - 1
        # calculate target coordinates given by steps in direction
        target = (x + steps * directionShift[0], y + steps * directionShift[1])

        # check if move ends outside board or on a field with an obstructed
        if not self.isValidCoordinate(*target) or self.get(*target) is FieldState.Obstructed:
            return False

        # check if there is a enemy fish in the way
        if any(
                # occupied fields with not own fish are enemies
                f.occupiedBy(None) and f is not self.get(x, y)
                # search until target reached, target will be skipped
                for f in self.iterateFields((x, y), directionShift, lambda fx, fy: (fx, fy) == target)
        ):
            return False

        # otherwise move is allowed
        return True

    def possibleMoves(self, x, y):
        return list(filter(partial(self.movePossible, x, y), MoveDirection))

    def __repr__(self):
        return '\n'.join(''.join(self.get(x, y).asChar() for x in range(self.columns)) for y in reversed(range(self.rows)))

# -*- encoding: utf-8-unix -*-
