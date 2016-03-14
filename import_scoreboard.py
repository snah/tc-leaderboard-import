#! /usr/bin/env python3

#    TC leaderboard import
#    Copyright (C) 2016  Hans Maree
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import sys


regex_tgm = r'''
    ^[. ]*(\d+)         # Rank
    --
    (.*[^-])            # Name
    ---*[ ]*
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
regex_tgm_20G = r'''
    ^[. ]*(\d+)         # Rank
    [ .]*
    (.*[^-])            # Name
    ---*[ ]*
    ([\d-]*)            # Level
    [ ]*@[ ]*
    ([\d:.-]*)          # Time
    [ ]
    ([^- ]+)            # Grade
    (?:
    [- ]+
    (.*)                # Comment
    )?
    '''

regex_tap_normal = r'''
    ^[. ]*(\d+)         # Rank
    --
    (.*[^-])            # Name
    ---*
    (\d+)               # Points
    [ ]pts[@ ]+
    ([\d:.-]+)          # Time
    (?:
    [| ]+
    (.*)                # Comment
    )?
    '''

regex_death = r'''
    ^(.*[^-])           # Name
    [ ]---*[ ]+
    (\d+)               # Level
    [@ ]+
    ([\d:.-]*)          # Time
    [| ]+
    (?:
    (.*)                # Comment
    )?
    '''

regex_doubles = r'''
    ^(.+[^-])           # Name1
    ---*[ ]
    (\d+)               # Lines1
    [@ ]+
    ([\d:.-]+)          # Time
    [@ ]+
    (\d+)               # Lines2
    [ ]---*
    (.+)                # Name2
    (?:
    [| ]+
    (.*)                # Comment
    )?
    '''

regex_tap_big = r'''
    ^[. ]*(\d+)         # Rank
    [. ]*
    (.*\S)            # Name
    \s+
    ([SGMsgm\d_]+)      # Grade
    \s+
    (\d+)               # Level
    \s+
    ([\d:.-]+)          # Time
    (?:
    [| ]+
    (.*)                # Comment
    )?
    '''

regex_ti = r'''
    ^[. ]*(\d+)         # Rank
    --
    (.*[^-])            # Name
    ---*[ ]*
    ([^- ]+)            # Grade
    [- ]+
    ([\d?-]*)           # Level
    [ ]*@[ ]*
    ([\d:.-?]*)         # Time
    \s+-\s+
    ([\d./?-]*)         # Date
    (?:
    [ ]-[ ]
    (..)                # ST
    [ ]
    (..)                # AC
    [ ]
    (..)                # CO
    [ ]
    (..)                # SK
    (?:
    [ ]-[ ]
    (.*)                # Comment
    )?
    )?
    '''

regex_texmaster = r'''
    ^(.*[^-])               # Name
    \ ---*[ ]+
    ([\dSMVKG]+(?:[ ]o)?)   # Class
    [ ]+
    ([\dx]+)                # Level
    [ ]+
    (?:\[ol])?
    ([\d:x]+)               # Time
    (?:\[/ol])?
    (?:
    (.*)                    # Comment
    )?
    '''

regex_texmaster2 = r'''
    ^(.*[^-])            # Name
    \ ---*[ ]+
    ([\dx]+)             # Level
    [ ]+
    (?:\[ol])?
    ([\d:x]+)            # Time
    (?:\[/ol])?
    (?:
    (.*)                 # Comment
    )?
    '''

regex_NES = r'''
    ^[. ]*(\d+)         # Rank
    [- ]+
    (.*[^-])            # Name
    [- ]+
    ([\d,]+)            # Score
    [- ]+
    (\d+[+][\d.]+)      # Level
    [ -]
    (.*)                # Comment
    '''

regex_NES_level19 = r'''
    ^[. ]*(\d+)         # Rank
    --
    (.*[^-])            # Name
    ---*[ ]*
    ([\d,]+)            # Score
    [- ]+
    ([\d?]+)            # Lines
    [ -]+
    ([\d?]+)            # pts/line
    [ -]+
    (.*)                # Comment
    '''

regex_table = {
        'TGM1': regex_tgm,
        'TGM_20G_code': regex_tgm_20G,
        'TAP_master': regex_tgm,
        'TAP_death': regex_death,
        'TAP_normal': regex_tap_normal,
        'TAP_doubles': regex_doubles,
        'TAP_master_big_code': regex_tap_big,
        'Ti_master_provisional': regex_ti,
        'Ti_master_qualified': regex_ti,
        'Ti_master_world_provisional': regex_ti,
        'Ti_master_world_qualified': regex_ti,
        'Ti_shirase': regex_ti,
        'texmaster_special_ti': regex_texmaster,
        'texmaster_special': regex_texmaster,
        'texmaster_sudden_ti': regex_texmaster,
        'texmaster_sudden': regex_texmaster2,
        'NES_NTSC_A_type': regex_NES,
        'NES_NTSC_A_type_level19': regex_NES_level19,
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
