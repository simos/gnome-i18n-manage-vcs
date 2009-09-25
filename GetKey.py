#!/usr/bin/env python

import os
import sys
import tty
import termios 
import fcntl
import time

class GetKey:
    def __init__(self):
        self.fd = sys.stdin.fileno()

        self.oldterm = termios.tcgetattr(self.fd)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)

        tty.setcbreak(sys.stdin.fileno())
        self.newattr = termios.tcgetattr(self.fd)
        self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO

    def oldTerminalSettings(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)

    def newTerminalSettings(self):
        termios.tcsetattr(self.fd, termios.TCSANOW, self.newattr)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def getch(self):
        try:
            c = sys.stdin.read(1)
            return ord(c)

        except IOError:
            return 0

if __name__ == '__main__':
    a = GetKey()
    a.newTerminalSettings()

    while 1:
        if a.getch():
            sys.exit(-1)

    a.oldTerminalSettings()

