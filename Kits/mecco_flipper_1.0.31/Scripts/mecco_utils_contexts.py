#python
import lx
import sys
from contextlib import contextmanager

@contextmanager
def ignore(*exceptions):
    """ Use to quickly catch certain exceptions
        without needing try/except statements.
        Equivalent to:

        try:
            (code)
        except exceptions:
            pass

        *exceptions = exceptions to catch

        Any other exceptions will still raise exceptions.

        Syntax:

        with ignore(AssertionError, IndexError):
            raise AssertionError
            # this code will suppress the AssertionError
    """
    try:
        yield
    except exceptions:
        pass

@contextmanager
def catch(info="", stop=False, *exceptions):
    """ Use to catch a list of exceptions and write
        info to the modo log.

        info = string describing the situation
        stop = if False, exception is suppressed
               if True, exception is re-raised
        *exceptions = list of exceptions to suppress,
                      if stop is False. If empty,
                      all exceptions are suppressed.



        Syntax:

        with catch("", False, AssertionError):
            raise AssertionError

        This code would print an error message to the log,
        and then keep running. If another error was raised
        instead, the code would print and error message and
        raise another exception.
    """
    try:
        yield
    except Exception as e:
        e_name = str(e.__class__).rsplit('.')[-1][:-2]
        line = sys.exc_traceback.tb_lineno
        exc_value = sys.exc_value
        lx.out('%s: "%s" on line %d: %s' % (e_name, exc_value, line, info))
        if exceptions:
            if type(e) not in exceptions:
                raise e
        if stop:
            raise e

