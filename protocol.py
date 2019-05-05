# -*- encoding: utf-8-unix -*-

"""Gameserver communication protocol"""

import asyncio, logging, lxml.etree
from lxml.builder import E


def sendXML(writer, message):
    writer.write(lxml.etree.tostring(message))


@asyncio.coroutine
def PiranhasClient(loop, host, port, reservation=None):
    room = None

    # build join message
    if reservation is not None:
        # join to existing room by reservation
        joinMessage = E.joinedPrepared(reservationCode=reservation)
    else:
        # join to existing game or create a new one
        joinMessage = E.join(gameType='swc_2019_piranhas')

    # connect to gameserver
    reader, writer = yield from asyncio.open_connection(host, port, loop=loop)
    logging.info('connected to gameserver')

    logging.info('join game')
    # initiate communication
    writer.write(b'<protocol>')
    # and join
    sendXML(writer, joinMessage)

    logging.info('enter communication loop')
    # communication loop
    parser = lxml.etree.XMLPullParser(events=('end',))
    while not reader.at_eof():
        # read next tag
        data = yield from reader.readuntil(b'>')
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
            if element.tag == 'joined':
                # joined event
                if room is not None:
                    logging.warning('unexpected joined event, ignore it')
                else:
                    # save room identifier
                    room = element.get('roomId')
                    logging.info('joined room %s', room)
                element.clear()
            elif element.tag == 'protocol':
                # communication end
                logging.info('gameserver send goodbye')
            elif element.tag == 'room':
                # game events
                print(element)
                element.clear()
    # server closed communication, close parser
    parser.close()
