import enum, lxml.etree
from board import Board
from move import Move
from player import Player

"""
Game state.
"""


class Memento:
    def __init__(self, turn, startPlayer, currentPlayer, playerNames, board, lastMove):
        self.turn = turn
        self.startPlayer = startPlayer
        self.currentPlayer = currentPlayer
        self.playerNames = playerNames
        self.board = board
        self.lastMove = lastMove

    @staticmethod
    def __getPlayerName(stateNode, player):
        expr = '*[local-name() = $tag and @color = $color]/@displayName'
        return next(iter(stateNode.xpath(expr, tag=player.value.lower(), color=player.value)))

    @classmethod
    def fromXML(cls, mementoNode):
        # get first state node in memento
        stateNode = mementoNode.find('state')

        turn = int(stateNode.get('turn'))
        startPlayer = Player(stateNode.get('startPlayer'))
        currentPlayer = Player(stateNode.get('currentPlayer'))

        playerNames = dict(
            (p, Memento.__getPlayerName(stateNode, p))
            for p in Player
        )

        board = Board.fromXML(stateNode.find('board'))

        lastMoveNode = stateNode.find('lastMove')
        lastMove = Move.fromXML(lastMoveNode) if lastMoveNode is not None else None

        # TODO: condition???

        return cls(turn, startPlayer, currentPlayer, playerNames, board, lastMove)

# -*- encoding: utf-8-unix -*-
