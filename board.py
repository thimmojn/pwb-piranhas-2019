import enum, lxml.etree
from itertools import chain

"""
Board of Piranhas game.
"""


class FieldState(enum.Enum):
    Empty = 'EMPTY'
    Red = 'RED'
    Blue = 'BLUE'
    Obstructed = 'OBSTRUCTED'

    def asChar(self):
        if self is FieldState.Empty:
            return ' '
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

    def get(self, x, y):
        return self.fields[x][y]

    def set(self, x, y, state):
        self.fields[x][y] = state

    def copy(self):
        pass

    def fishCount(self, player=None):
        if player is not None:
            searchedFields = {FieldState(player.value)}
        else:
            searchedFields = {FieldState.Red, FieldState.Blue}
        return sum(chain.from_iterable((1 for field in row if field in searchedFields) for row in self.fields))

    def __repr__(self):
        return "\n".join(" ".join(self.get(x, y).asChar() for x in range(self.columns)) for y in reversed(range(self.rows)))

# -*- encoding: utf-8-unix -*-
