def PiranhasAgent:
    def __init__(self):
        self.player = None
        self.memento = None

    def setPlayer(self, player):
        self.player = player

    def updateMemento(self, memento):
        self.memento = memento

    def requestMove(self):
        pass

# -*- encoding: utf-8-unix -*-
