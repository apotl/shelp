#!/usr/bin/env python3

import sys
from lib.bot import Shelp

USE_SSL = False

try:
    ADDR = sys.argv[1]
    NICK = sys.argv[2]
except IndexError:
    print('usage: '+sys.argv[0]+' irc_server[:port] nickname [channel1] [channel2] ...')
    exit()
try:
    ADDR = sys.argv[1].split(':', maxsplit=1)[0]
    PORT = int(sys.argv[1].split(':', maxsplit=1)[1])
except:
    print('assuming port 6667')
    PORT = 6667

if '--ssl' in sys.argv:
    USE_SSL = True

CHANNELS = sys.argv[2:]

shelp = Shelp(ADDR, PORT, NICK, CHANNELS, use_ssl=USE_SSL)

shelp.start()
