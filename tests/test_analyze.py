import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

from keyboardtools.analyze import logkeys, _logkeys_analyze
from pkg_resources import resource_string


@contextlib.contextmanager
def suppress_output():
    stdout = io.StringIO()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stdout
    yield stdout
    sys.stdout = old_stdout
    sys.stderr = old_stderr


class TestLogkeysParse(unittest.TestCase):

    def test_incorrect_commandline(self):
        with suppress_output():
            sys.argv = ['kbt-logkeys']
            self.assertRaises(SystemExit, logkeys)

            sys.argv = ['kbt-logkeys', 'foo']
            self.assertRaises(SystemExit, logkeys)

    def test_file_output(self):
        with suppress_output(), tempfile.TemporaryDirectory() as tempdir:
            with open(os.path.join(tempdir, 'infile'), 'wb') as infile, \
                 open(os.path.join(tempdir, 'outfile'), 'wt') as outfile:
                    test_data = resource_string(__name__, 'logkeys.log')
                    infile.write(test_data)
                    infile.flush()
                    sys.argv = ['kbt-logkeys', infile.name, outfile.name]
                    logkeys()

                    result = json.load(open(outfile.name, 'rt'))

        self.assertEqual(
            result['k'],
            {'key': 'k', '<rshft>': 0, 'count': 9, '<lmeta>': 0,
             '<lshft>': 0, '<rctrl>': 0, '<lctrl>': 0, '<ralt>': 0,
             '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})
        self.assertEqual(
          result['ö'],
          {'key': 'ö', '<rshft>': 0, 'count': 3, '<lmeta>': 0,
           '<lshft>': 0, '<rctrl>': 0, '<lctrl>': 0, '<ralt>': 0,
           '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})
        self.assertEqual(
          result['f'],
          {'key': 'f', '<rshft>': 0, 'count': 7, '<lmeta>': 0,
           '<lshft>': 1, '<rctrl>': 0, '<lctrl>': 1, '<ralt>': 0,
           '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})

    def test_analyze(self):
        test_data = resource_string(__name__, 'logkeys.log').decode('UTF-8')
        test_file = io.StringIO(test_data)
        result = _logkeys_analyze(test_file)

        self.assertEqual(
            result.keys['k'],
            {'key': 'k', '<rshft>': 0, 'count': 9, '<lmeta>': 0,
             '<lshft>': 0, '<rctrl>': 0, '<lctrl>': 0, '<ralt>': 0,
             '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})
        self.assertEqual(
            result.keys['ö'],
            {'key': 'ö', '<rshft>': 0, 'count': 3, '<lmeta>': 0,
             '<lshft>': 0, '<rctrl>': 0, '<lctrl>': 0, '<ralt>': 0,
             '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})
        self.assertEqual(
          result.keys['f'],
          {'key': 'f', '<rshft>': 0, 'count': 7, '<lmeta>': 0,
           '<lshft>': 1, '<rctrl>': 0, '<lctrl>': 1, '<ralt>': 0,
           '<rmeta>': 0, '<altgr>': 0, '<lalt>': 0})
