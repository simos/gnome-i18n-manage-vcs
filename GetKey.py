#!/usr/bin/env python
# Following now http://code.activestate.com/recipes/572182/

import sys
import termios 
import atexit
import select

class GetKey:
    def __init__(self):
        self.fd = sys.stdin.fileno()

        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # new terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)

        self.initialize()
        atexit.register(self.restore)

    def restore(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def initialize(self):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

    def kbhit(self):
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        return dr <> []

if __name__ == '__main__':
    a = GetKey()

    while 1:
        if a.kbhit():
            sys.exit(-1)

