# -*- encoding: utf-8-unix -*-

"""Gameserver communication protocol"""

import asyncio, logging, lxml.etree
from lxml.builder import E
from memento import Memento
from player import Player


def sendXML(writer, message):
    writer.write(lxml.etree.tostring(message))


@asyncio.coroutine
def PiranhasClient(loop, host, port, agent, reservation=None):
    room = None
    player = None

    # build join message
    if reservation is not None:
        # join to existing room by reservation
        joinMessage = E.joinPrepared(reservationCode=reservation)
    else:
        # join to existing game or create a new one
        joinMessage = E.join(gameType='swc_2019_piranhas')

    # connect to gameserver
    reader, writer = yield from asyncio.open_connection(host, port, loop=loop)
    logging.info('connected to gameserver %s:%d', host, port)

    logging.info('join game (%s)', 'prepared' if reservation is not None else 'new')
    # initiate communication
    writer.write(b'<protocol>')
    # and join
    sendXML(writer, joinMessage)

    logging.info('enter communication loop')
    # communication loop
    parser = lxml.etree.XMLPullParser(events=('end',))
    while not reader.at_eof():
        # read next tag
        try:
            data = yield from reader.readuntil(b'>')
        except asyncio.IncompleteReadError:
            # no more tags read
            data = b''
        logging.debug('get: %s', data.decode())
        # feed to XML parser
        parser.feed(data)
        # check for XML parser events,
        # must be a close event
        event = next(parser.read_events(), None)
        if event is not None:
            # closed element
            element = event[1]
            logging.debug('XML tag closed: %s', element.tag)
            if element.tag == 'room':
                logging.debug(lxml.etree.tostring(element))
                # matches room identifier?
                if element.get('roomId') == room:
                    # game events
                    dataNode = element.find('data')
                    dataClass = dataNode.get('class')
                    if dataClass == 'sc.framework.plugins.protocol.MoveRequest':
                        # move request
                        logging.info('move requested')
                        # request move from agent
                        move = agent.requestMove()
                        # agent is allowed to return None (in development phase)
                        if move is not None:
                            # send to game server
                            response = E.room(roomId=room)
                            response.append(move.toXML())
                            sendXML(writer, response)
                    elif dataClass == 'welcomeMessage':
                        # receive my color
                        if player is not None:
                            logging.warning('unexpected welcome message, ignore it')
                        else:
                            # send to agent
                            player = Player(dataNode.get('color').upper())
                            agent.setPlayer(player)
                    elif dataClass == 'memento':
                        # update memento
                        memento = Memento.fromXML(dataNode)
                        agent.updateMemento(memento)
                else:
                    logging.info('received message for another room')
                element.clear()
            elif element.tag == 'joined':
                # joined event
                if room is not None:
                    logging.warning('unexpected joined event, ignore it')
                else:
                    # save room identifier
                    room = element.get('roomId')
                    logging.info('joined room %s', room)
                element.clear()
            elif element.tag == 'left':
                # client left event
                # is event for my room?
                if element.get('roomId') == room:
                    # end communication
                    writer.write(b'</protocol>')
                else:
                    logging.info('some client left another room')
                element.clear()
            elif element.tag == 'protocol':
                # communication end
                logging.info('gameserver send goodbye')
    # server closed communication, close parser
    parser.close()
