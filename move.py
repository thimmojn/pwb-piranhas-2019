import enum
from lxml.builder import E

"""
Game moves.
"""


class MoveDirection(enum.Enum):
    Up = 'UP'
    UpRight = 'UP_RIGHT'
    Right = 'RIGHT'
    DownRight = 'DOWN_RIGHT'
    Down = 'DOWN'
    DownLeft = 'DOWN_LEFT'
    Left = 'LEFT'
    UpLeft = 'UP_LEFT'


class Move:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.hints = []

    @classmethod
    def fromXML(cls, dataNode):
        return cls(
            int(dataNode.get('x')),
            int(dataNode.get('y')),
            MoveDirection(dataNode.get('direction'))
        )

    def toXML(self):
        moveNode = E.data({
            'class': 'move',
            'x': str(self.x),
            'y': str(self.y),
            'direction': self.direction.value
        })
        for hint in self.hints:
            moveNode.append(E.hint(content=hint))
        return moveNode

    def addHint(self, content):
        self.hints.append(content)
        return self

    def __repr__(self):
        return '({},{}) -> {}'.format(self.x, self.y, self.direction.name)

# -*- encoding: utf-8-unix -*-
