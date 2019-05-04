# -*- encoding: utf-8-unix -*-

"""Gameserver communication protocol"""

import asyncio, logging, lxml.etree
from lxml.builder import E


class PiranhasProtocol(asyncio.Protocol):
    def __init__(self, loop, room=None):
        self.transport = None
        self.loop = loop
        self.room = room

    def connection_made(self, transport):
        # connected to gameserver
        logging.debug('connected to gameserver')
        self.transport = transport
        self.data_send(b'<protocol>')
        if self.room is not None:
            self.message_send(E.joined(roomId=self.room))
        else:
            self.message_send(E.join(gameType='swc_2019_piranhas'))

    def data_received(self, data):
        # data from gameserver
        logging.debug('received data from gameserver')
        logging.debug(data.decode())
        withoutEndProtocol = data.replace(b'</protocol>', b'')
        xmlWrapped = b''.join([b'<gsm>', withoutEndProtocol, b'</gsm>'])
        xmlParsed = lxml.etree.fromstring(xmlWrapped)
        for message in xmlParsed:
            self.message_received(message)

    def data_send(self, data):
        self.transport.write(data)

    def message_received(self, message):
        logging.debug('received message from gameserver')

    def message_send(self, message):
        self.data_send(lxml.etree.tostring(message))

    def connection_lost(self, exc):
        logging.debug('connection to gameserver lost - %s', 'regular close' if exc is None else 'error')
        self.loop.stop()
