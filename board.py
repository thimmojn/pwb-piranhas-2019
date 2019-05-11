# -*- encoding: utf-8-unix -*-

"""Board of Piranhas game."""

import enum, lxml.etree
from lxml.builder import E


class FieldState(enum.Enum):
    Empty = enum.auto()
    Red = enum.auto()
    Blue = enum.auto()
    Obstructed = enum.auto()

    @classmethod
    def fromString(cls, value):
        if value == 'EMPTY':
            return cls.Empty
        elif value == 'RED':
            return cls.Red
        elif value == 'BLUE':
            return cls.Blue
        elif value == 'OBSTRUCTED':
            return cls.Obstructed
        else:
            raise ValueError('unknown field state: {}'.format(value))

    def __repr__(self):
        if self is FieldState.Empty:
            return ' '
        elif self is FieldState.Red:
            return 'R'
        elif self is FieldState.Blue:
            return 'B'
        elif self is FieldState.Obstructed:
            return 'O'
        else:
            raise ValueError('no representation for {} given'.format(self.name))


class PiranhasBoard:
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
                FieldState.fromString(fieldNode.get('state'))
            )

        return board

    def get(self, x, y):
        return self.fields[x][y]

    def set(self, x, y, state):
        self.fields[x][y] = state

    def copy(self):
        pass

    def __repr__(self):
        return "\n".join(" ".join(repr(self.get(x, y)) for x in range(self.columns)) for y in reversed(range(self.rows)))
