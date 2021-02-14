import sys
import os
import time
import tempfile
from six import StringIO
import quo
from quo.testing import CliRunner

import spinher


def test_spinner():
    @quo.command()
    def cli():
       with spinher.spinner():
           for thing in range(10):
               pass

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_resume():
    @quo.command()
    def cli():
       spinner = spinher.Spinner()
       spinner.start()
       for thing in range(10):
           pass
       spinner.stop()
       spinner.start()
       for thing in range(10):
           pass
       spinner.stop()

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_redirect():
    @quo.command()
    def cli():
       stdout_io = StringIO()
       saved_stdout = sys.stdout
       sys.stdout = stdout_io  # redirect stdout to a string buffer
       spinner = spinher.Spinner()
       spinner.start()
       time.sleep(1)  # allow time for a few spins
       spinner.stop()
       sys.stdout = saved_stdout
       stdout_io.flush()
       stdout_str = stdout_io.getvalue()
       assert len(stdout_str) == 0

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_redirect_force():
    @quo.command()
    def cli():
       stdout_io = StringIO()
       spinner = spinher.Spinner(force=True, stream=stdout_io)
       spinner.start()
       time.sleep(1)  # allow time for a few spins
       spinner.stop()
       stdout_io.flush()
       stdout_str = stdout_io.getvalue()
       assert len(stdout_str) > 0

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_disable():
    @quo.command()
    def cli():
       stdout_io = StringIO()
       saved_stdout = sys.stdout
       sys.stdout = stdout_io  # redirect stdout to a string buffer
       spinner = spinher.Spinner(disable=True)
       spinner.start()
       time.sleep(1)  # allow time for doing nothing
       spinner.stop()
       sys.stdout = saved_stdout
       stdout_io.flush()
       stdout_str = stdout_io.getvalue()
       assert len(stdout_str) == 0

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None


def test_spinner_as():
    @quo.command()
    def cli():
       spinner = spinher.spinner()
       with spinner as sp:
           assert sp == spinner

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exception is None

class CMException(Exception):
    pass


def test_spinner_exc():
    @quo.command()
    def cli():
       with spinher.spinner():
           for thing in range(10):
               if thing == 5:
                   raise CMException("foo")

    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert isinstance(result.exception, CMException)
