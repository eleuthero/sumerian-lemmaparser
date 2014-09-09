#!/usr/bin/python

import argparse
import fileinput
import operator
from sys import stdout

global SEED_WORDS 

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--seed',
                        type = str,
                        default = '',
                        help='Words used in seed rules to be marked as ' \
                             'their own parts of speech.')

    return parser.parse_args()

def set_seed_words(args):
    global SEED_WORDS

    SEED_WORDS = args.seed.split(',')

def process_token(token):
    global SEED_WORDS

    tokens = token.split('$')
    (word, pos) = tokens[0:2]

    # Start with the word itself.

    result = word

    # Always tag the word with the true pos.

    result += '*%s*' % pos

    # If we have preknowledge about this word, mark it as its own
    # synethetic part of speech.

    if word in SEED_WORDS:
        result += '$%s$' % word

    return result 

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
set_seed_words(args)
parse_mega_corpus(args)
