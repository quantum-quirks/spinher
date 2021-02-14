"""
Spinher is a Python  based module for showing the user that the Command-Line Interface(CLI) is active.
"""


import sys
import threading
import itertools
import quo


class Whirl(object):
    sequence = itertools.cycle(['-', '/', '_', '|', '\\'])

    def initialize(solitary, sound=False, disable=False, force=False, stream=sys.stdout):
        solitary.sound = sound
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
            solitary.spin_thread = threading.Thread(target=solitary.initialize_spinner)
            solitary.spin_thread.start()

    def stop(solitary):
        if solitary.spin_thread:
            solitary.stop_running.set()
            solitary.spin_thread.join()

    def initialize_spinner(solitary):
        while not solitary.stop_running.is_set():
            solitary.stream.write(next(solitary.sequence))
            solitary.stream.flush()
            solitary.stop_running.wait(0.2)
            solitary.stream.write('\b')
            solitary.stream.flush()

    def enter(solitary):
        solitary.start()
        return solitary

    def exit(solitary, exc_type, exc_val, exc_tb):
        if solitary.disable:
            return False
        solitary.stop()
        if solitary.sound:
            solitary.stream.write('\7')
            solitary.stream.flush()
        return False

def whirl(sound=False, disable=False, force=False, stream=sys.stdout):
    return Whirl(sound, disable, force, stream)


__version__ = "2021.2.dev3"
