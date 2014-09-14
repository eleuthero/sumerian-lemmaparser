#!/usr/bin/python

import argparse
import fileinput
import operator
import os.path
from sys import stdout

global SEED_WORDS 
global PREKNOWLEDGE

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--seed',
                        type = str,
                        default = '',
                        help='Words used in seed rules to be marked as ' \
                             'their own parts of speech.')

    parser.add_argument('--preknowledge',
                        type = str,
                        default = None,
                        help='File containing words and their parts of ' \
                             'speech to be used as preknowledge.')

    return parser.parse_args()

def set_seed_words(args):
    global SEED_WORDS

    SEED_WORDS = args.seed.split(',')

def set_preknowlege(args):
    global PREKNOWLEDGE

    if args.preknowledge:
        if os.path.isfile(args.preknowledge):
            PREKNOWLEDGE = list()
            with open(args.preknowledge) as fin:
                lines = fin.readlines()
                for line in lines:
                    PREKNOWLEDGE.append( line.strip() )

def process_token(token):
    global SEED_WORDS
    global PREKNOWLEDGE

    tokens = token.split('$')
    (word, pos) = tokens[0:2]

    # Start with the word itself.

    result = word

    # Always tag the word with the true pos.

    result += '*%s*' % pos

    # If this is a seed word, mark it as its own synethetic part of speech.

    if word in SEED_WORDS:
        result += '$%s$' % word

    # If this word is included in our preknowledge, mark it with the
    # part of speech from the preknowledge.

    elif token in PREKNOWLEDGE:
        result += '$%s$' % pos

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
set_preknowlege(args)
parse_mega_corpus(args)