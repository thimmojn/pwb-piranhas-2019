#!/usr/bin/env python3
# -*- encoding: utf-8-unix -*-

import argparse, asyncio, logging
from agent import PiranhasAgent
from protocol import PiranhasClient


def runGameclient(host, port, agent, reservation):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(PiranhasClient(loop, host, port, agent, reservation))
    loop.close()

def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='>>>MISSING<<<', add_help=False, allow_abbrev=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('--host', '-h', default='localhost', help='gameserver host')
    parser.add_argument('--port', '-p', type=int, default=13050, help='gameserver port')
    parser.add_argument('--reservation', '-r', help='reservation number')
    args, _unknown = parser.parse_known_args()

    agent = PiranhasAgent()

    runGameclient(args.host, args.port, agent, args.reservation)


if __name__ == '__main__':
    main()
