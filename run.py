#!/usr/bin/env python3

import sys
from lib.bot import Shelp

try:
    ADDR = sys.argv[1]
    NICK = sys.argv[2]
except IndexError:
    print('usage: '+sys.argv[0]+' irc_server nickname [channel1] [channel2] ...')
    exit()
try:
    ADDR = sys.argv[1].split(':', maxsplit=1)[0]
    PORT = sys.argv[1].split(':', maxsplit=1)[1]
except:
    PORT = 6667

CHANNELS = sys.argv[2:]

shelp = Shelp(ADDR, PORT, NICK, CHANNELS)
shelp.start()
