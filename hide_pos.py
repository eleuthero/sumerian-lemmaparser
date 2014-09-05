#!/usr/bin/python

import argparse
import fileinput
import operator
from sys import stdout

# All parts of speech.

ALL_POS = [
              'W',  # Sumerian-language words with glosses
                    #     (e.g. ninda == "bread")
              'n',  # Numbers.
              'PN', # Personal names.
              'PF', # [Custom] Professions and titles.
              'X',  # Unknown words.
              'u',  # Unlemmatizable words.
                    #     (generally due to sign damage or loss)
              'GN', # Geographical names. (primarily cities)
              'DN', # Divine names.
              'MN', # Month names.
              'RN', # Royal names.
              'FN', # Field names. (primarily agricultural)
              'WN', # Watercourse names.  (primarily rivers)
              'TN', # Temple names.
              'ON', # Object names.
              'AN', # Agricultural names.
              'CN'  # Celestial names.
          ]

# Default list of parts of speech to grant preknowledge.

SHOW_POS = [ 'n', 'PF' ] # , 'GN', 'DN', 'MN', 'RN',
                         # 'FN', 'WN', 'TN', 'ON', 'AN', 'CN' ]

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--preknowledge',
                        type = str,
                        default = ','.join(SHOW_POS),
                        # choices = ALL_POS,
                        help='List of parts of speech for which to grant ' +
                             'preknowledge.')

    return parser.parse_args()

def set_pos_list(args):
    global SHOW_POS

    SHOW_POS = args.preknowledge.split(',')

def process_token(token):
    tokens = token.split('$')
    (word, pos) = tokens[0:2]

    # Always tag the word with the true pos.

    word += '*%s*' % pos

    # If we have preknowledge about this pos, reveal the pos.

    if pos in SHOW_POS:
        word += '$%s$' % pos

    return word

def parse_mega_corpus(args):

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # our command-line switches as filenames.

    for line in fileinput.input('-'):
        line = line.strip() 
        if len(line) > 0:
            if not line[0] in '&$@#':

                # This is a line of source text.

                for token in line.split(' '):
                    if token.endswith('$'):

                        # Determine whether to hide or show this token
                        # based on its POS.

                        stdout.write( process_token(token) + ' ' )

                    else:

                        # This isn't a word we're interested in.
                        # Pass it through.

                        stdout.write(token + ' ')

                stdout.write('\n')

            else:

                # This was a comment line; preserve it in the output.

                stdout.write(line + '\n')
        
# ====
# Main 
# ====

args = init_parser()
set_pos_list(args)
parse_mega_corpus(args)
