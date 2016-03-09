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
    (?:
    [- ]+
    (.*)                # Comment
    )?
    '''

regex_death = r'''
    ^(.*)               # Name
    [ ]---*[ ]+
    (\d+)               # Level
    [@ ]+
    ([\d:.-]*)          # Time
    [| ]+
    (?:
    (.*)                # Comment
    )?
    '''


regex_texmaster = r'''
    ^(.*)               # Name
    \ ---*[ ]+
    ([\dSMVKG]+(?:[ ]o)?)      # Class
    [ ]+
    ([\dx]+)               # Level
    [ ]+
    (?:\[ol])?
    ([\d:x]+)            # Time
    (?:\[/ol])?
    (?:
    (.*)                # Comment
    )?
    '''

regex_texmaster2 = r'''
    ^(.*)               # Name
    \ ---*[ ]+
    ([\dx]+)               # Level
    [ ]+
    (?:\[ol])?
    ([\d:x]+)            # Time
    (?:\[/ol])?
    (?:
    (.*)                # Comment
    )?
    '''

regex_table = {
        'TGM1': regex_tgm,
        'TAP_master': regex_tgm,
        'TAP_death': regex_death,
        'texmaster_special_ti': regex_texmaster,
        'texmaster_special': regex_texmaster,
        'texmaster_sudden_ti': regex_texmaster,
        'texmaster_sudden': regex_texmaster2,
        }


def read_scoreboard(text, regex):
    scoreboard = []
    for line in text.split('\n'):
        match = re.match(regex, line, re.VERBOSE)
        if match:
            scoreboard.append(match.groups())
    return scoreboard



def main():
    try:
        regex = regex_table[sys.argv[1].split('/')[-1]]
    except KeyError:
        print('No input regex set for file {}.'.format(sys.argv[1]), file=sys.stdout)
        return

    with open(sys.argv[1]) as f:
        scoreboard = read_scoreboard(f.read(), regex)
    try:
        outfile = open(sys.argv[2], 'w')
    except IndexError:
        outfile = sys.stdout

    for line in scoreboard:
        print(','.join(map(lambda x: x or '', line)), file=outfile)

if __name__ == '__main__':
    main()
