"""
Spinher is a Python  based module for showing the user that the Command-Line Interface(CLI) is active.
"""


import sys
import threading
import itertools
import quo


class Whirl(object):
    spinner_cycle = itertools.cycle(['-', '/', '_', '|', '\\'])

    def init (solitary, beep=False, disable=False, force=False, stream=sys.stdout):
        solitary.beep = beep
        solitary.disable = disable
        solitary.force = force
        solitary.stream = stream
        solitary.stop_running = None
        solitary.spin_thread = None

    def start(solitary):
        if solitary.disable:
            return
        if solitary.stream.isatty() or solitary.force:
            solitary.stop_running = threading.Event()
            solitary.spin_thread = threading.Thread(target=solitary.init_spin)
            solitary.spin_thread.start()

    def stop(solitary):
        if solitary.spin_thread:
            solitary.stop_running.set()
            solitary.spin_thread.join()

    def init_spin(solitary):
        while not solitary.stop_running.is_set():
            solitary.stream.write(next(solitary.spinner_cycle))
            solitary.stream.flush()
            solitary.stop_running.wait(0.2)
            solitary.stream.write('\b')
            solitary.stream.flush()

    def __enter__(solitary):
        solitary.start()
        return solitary

    def __exit__(solitary, exc_type, exc_val, exc_tb):
        if solitary.disable:
            return False
        solitary.stop()
        if solitary.beep:
            solitary.stream.write('\7')
            solitary.stream.flush()
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


__version__ = "2021.2.dev3"
