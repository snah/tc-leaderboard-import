#! /usr/bin/env python3

import re
import sys


regex_tgm = r'''
    ^[. ]*(\d+)         # Rank
    [- ]+
    ([^-]+)             # Name (assumes no '-' in name)
    [- ]+
    ([^- ]+)            # Grade
    [- ]+
    ([\d-]*)            # Level
    [ ]*@[ ]*
    ([\d:.-]*)          # Time
    (?:
    [- ]+
    ([\d.-/]*)          # Date
    )?
    '''


def read_scoreboard(text):
    scoreboard = []
    for line in text.split('\n'):
        match = re.match(regex_tgm, line, re.VERBOSE)
        if match:
            scoreboard.append(match.groups())
    return scoreboard



if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        scoreboard = read_scoreboard(f.read())
    for line in scoreboard:
        print(','.join(map(str, line)))
