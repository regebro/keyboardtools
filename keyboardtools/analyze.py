import argparse
import collections
import json
import re


MODIFIERS = ('<lshft>', '<rshft>', '<lctrl>', '<rctrl>', '<lmeta>',
             '<rmeta>', '<lalt>', '<ralt>', '<altgr>')

class KeyStats(object):

    def __init__(self):
        self.keys = {}

    def keypress(self, key, modifiers):
        if key not in self.keys:
            self.keys[key] = {'key': key, 'count': 0}
            for modifier in MODIFIERS:
                self.keys[key][modifier] = 0

        self.keys[key]['count'] += 1
        for modifier in modifiers:
            self.keys[key][modifier] += 1

    def keys_by_count(self):
        return sorted(self.keys.keys(),
                      key=lambda x: self.keys[x]['count'],
                      reverse=True)


def logkeys():
    parser = argparse.ArgumentParser(
        description='Analyze a logkeys log to generate statistics.')

    parser.add_argument('infile', help='Path to the logkeys log file.')
    parser.add_argument('outfile', help='Path to create the analysis file.')

    args = parser.parse_args()
    with open(args.infile, 'rt') as infile, open(args.outfile, 'wt') as outfile:
        stats = _logkeys_analyze(infile)
        json.dump(stats.keys, outfile)

    print("Keys in order of popularity:")
    for key in stats.keys_by_count():
        if key[0] in ('<', ' '):
            continue  # Don't print out fixed keys
        print("%s: %s" % (key, stats.keys[key]['count']))


def _logkeys_analyze(infile):
    stats = KeyStats()

    for line in infile:
        if not ' > ' in line:
            continue

        timestamp, logged = line.lower().split(' > ', 1)
        keys = logged.replace('\n', '<enter>')
        keys = re.findall('\<\w*?\>|.', keys)
        modifiers = []
        for key in keys:
            if key in MODIFIERS:
                modifiers.append(key)
                continue
            stats.keypress(key, modifiers)
            modifiers = []

    return stats
