# python

import lx
from sys import _getframe
from time import time
from var import *

class DebugTimer():
    _start = 0

    def __init__(self):
        self._start = time()

    def end(self):
        if not lx.eval('user.value mecco_tagger.debugMode ?'):
            return

        frame = _getframe(1)
        caller = frame.f_globals['__name__']
        line = frame.f_lineno
        elapsed = time() - self._start

        if elapsed > DEBUG_TIMER_THRESHOLD:
            lx.out('Tagger Debug Timer: %.4f (%s, line %s)' % (elapsed, caller, line))

def debug(string):
    if not lx.eval('user.value mecco_tagger.debugMode ?'):
        return

    frame = _getframe(1)
    caller = frame.f_globals['__name__']
    line = frame.f_lineno

    lx.out('Tagger Debug: %s (%s, line %s)' % (string, caller, line))
