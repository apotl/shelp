import socket
from threading import Thread
from time import sleep

from lib.structs import Queue
import shelpers

class IRCBase():
    def __init__(self):
        self._sock = None

    def _send(self, m):
        self._sock.send(m.encode()+b'\r\n')

class IRCHandler(IRCBase):

    def __init__(self, coninfo):
        self.coninfo = coninfo
        self.shelpermods = [
            [getattr(getattr(shelpers,shelper), shelpclass) for shelpclass in dir(getattr(shelpers, shelper))
             if shelpclass != 'Shelper' or shelpclass[0] != '_'][0]()
            for shelper in dir(shelpers) if shelper[0] != '_']
        for sh in self.shelpermods:
            print(dir(sh))

    def say(self, c, m):
        self._send('PRIVMSG '+c+' :'+m)

    def handle(self, buf):
        if buf[0] == 'PING':
            self._on_ping(buf)
        if buf[1] == '001':
            self._on_welcome(buf)
        if buf[1] == 'PRIVMSG':
            self._on_privmsg(buf)
        if buf[1] == 'INVITE':
            self._on_invite(buf)

    def _on_ping(self, buf):
        self._send('PONG '+buf[buf.index('PING')+1])

    def _on_welcome(self, buf):
        for channel in self.coninfo['channels']:
            self._send('JOIN '+channel)

    def _on_privmsg(self, buf):
        src = buf[0]
        srcnick = buf[0][1:buf[0].index('!')]
        m = ' '.join(buf[3:])[1:]
        dst = buf[2]

        msgs = []

        for mod in self.shelpermods:
            msgs += mod.check(m)

        print(msgs)

        for msg in msgs:
            self.say(dst, msg)

    def _on_invite(self, buf):
        self.coninfo['channels'] += [buf[3]]
        self._send('JOIN '+buf[3])

class Shelp(IRCBase):
    def __init__(self, addr, port, nick, channels):
        
        self._sock = None
        self._addr = addr
        self._port = port
        self._nick = nick

        self._q = Queue()

        self._calling_error = None
        self._call_handler_thread = None
        self._listen_thread = None

        self._handler = IRCHandler(
            {
                'addr': addr,
                'port': port,
                'nick': nick,
                'channels': channels,
            })
    
    def _connect(self):
        while 1:
            try:
                self._sock = socket.socket()
                self._handler._sock = self._sock

                self._sock.connect((self._addr, self._port))

                self._send('USER '+self._nick+' 0 * :'+self._nick)
                self._send('NICK '+self._nick)
                print('Connected.')
                break
            except Exception as e:
                if e[0] == socket.errno.ETIMEDOUT:
                    sleep(10)
                    print('Timeout, retrying...')
                else:
                    raise

    def start(self):
        while 1:
            self._connect()
            self._calling_error = False

            self._call_handler_thread = Thread(target=self._call_handler)
            self._listen_thread = Thread(target=self._listen)

            self._call_handler_thread.start()
            self._call_handler_thread.join()

    def _call_handler(self):
        self._listen_thread.start()
        while 1:
            try:
                self._handler.handle(self._q.pop())
            except IndexError:
                sleep(1)
            except Exception as e:
                self._calling_error = True
                for dst in self._handler.coninfo['channels']:
                    self._handler.say(dst, str(e))
                break
        self._listen_thread.join()

    def _listen(self):
        while not self._calling_error:
            buf = self._sock.recv(4096).decode()
            for b in buf.split('\r\n'):
                self._q.push(b.split())
