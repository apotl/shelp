#!/usr/bin/env python3

import sys
from lib.bot import Shelp

try:
	addr = sys.argv[1]
	nick = sys.argv[2]
except IndexError:
	print('usage: '+sys.argv[0]+' irc_server nickname [channel1] [channel2] ...')
	exit()
try:
	addr = sys.argv[1].split(':',maxsplit=1)[0]
	port = sys.argv[1].split(':',maxsplit=1)[1]
except:
	port = 6667

channels = sys.argv[2:]

shelp = Shelp(addr,port,nick,channels)
shelp.start()
