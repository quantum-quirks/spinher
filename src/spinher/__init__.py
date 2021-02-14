"""
Spinher is a Python  based module for showing the user that the Command-Line Interface(CLI) is active.
"""


import sys
import threading
import itertools
import quo


class Whirl(object):
    spinner_cycle = itertools.cycle(['-', '/', '|', '\\'])

    def __init__(self, beep=False, disable=False, force=False, stream=sys.stdout):
        self.disable = disable
        self.beep = beep
        self.force = force
        self.stream = stream
        self.stop_running = None
        self.spin_thread = None

    def start(self):
        if self.disable:
            return
        if self.stream.isatty() or self.force:
            self.stop_running = threading.Event()
            self.spin_thread = threading.Thread(target=self.init_spin)
            self.spin_thread.start()

    def stop(self):
        if self.spin_thread:
            self.stop_running.set()
            self.spin_thread.join()

    def init_spin(self):
        while not self.stop_running.is_set():
            self.stream.write(next(self.spinner_cycle))
            self.stream.flush()
            self.stop_running.wait(0.2)
            self.stream.write('\b')
            self.stream.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.disable:
            return False
        self.stop()
        if self.beep:
            self.stream.write('\7')
            self.stream.flush()
        return False


def whirl(beep=False, disable=False, force=False, stream=sys.stdout):
    """This function creates a context manager that is used to display a
    spinner on stdout as long as the context has not exited.

    The spinner is created only if stdout is not redirected, or if the spinner
    is forced using the `force` parameter.

    Parameters
    ----------
    beep : bool
        Beep when spinner finishes.
    disable : bool
        Hide spinner.
    force : bool
        Force creation of spinner even when stdout is redirected.

    Example
    -------

        with spinher():
            open_file()
            check_wordcount()

    """
    return Whirl(beep, disable, force, stream)


__version__ = "2021.2.dev2"
