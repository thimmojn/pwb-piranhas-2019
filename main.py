#!/usr/bin/env python3
# -*- encoding: utf-8-unix -*-

import argparse, asyncio, logging
from protocol import PiranhasProtocol


def runGameserver(host, port, reservation):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: PiranhasProtocol(loop, reservation), host, port)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='>>>MISSING<<<', add_help=False, allow_abbrev=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('--host', '-h', default='localhost', help='gameserver host')
    parser.add_argument('--port', '-p', type=int, default=13050, help='gameserver port')
    parser.add_argument('--reservation', '-r', help='reservation number')
    args, _unknown = parser.parse_known_args()

    runGameserver(args.host, args.port, args.reservation)


if __name__ == '__main__':
    main()
