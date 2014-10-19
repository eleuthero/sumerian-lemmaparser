#!/usr/bin/python

import re
import argparse
import fileinput
import operator
import os.path
import random
from sys import stdout

global SEED_WORDS 
global PREKNOWLEDGE
global LINES

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--trainingpercent',
                        type=int, default=100, choices=range(1, 101),
                        help='Percent of qualifying tablets to include in '
                             'generated corpus.')

    parser.add_argument('-n', '--corporacount',
                        type=int,
                        default=1,
                        help='Specifies number of training, testing, and ' \
                             'baseline corpora sets to generate.')

    parser.add_argument('--seed',
                        type=str,
                        default='',
                        help='Words used in seed rules to be marked as ' \
                             'their own parts of speech.')

    parser.add_argument('--rngseed',
                        type=int,
                        default=None,
                        help='Specifies random number generator seed to use.')

    parser.add_argument('--preknowledge',
                        type=str,
                        default=None,
                        help='File containing words and their parts of ' \
                             'speech to be used as preknowledge.')

    """
    parser.add_argument('-o', '--omniscient',
                        action='store_true',
                        help='Include lemmatized part of speech in output.')
    """

    return parser.parse_args()

def set_rng_seed(args):
    random.seed(args.rngseed)

def set_seed_words(args):
    global SEED_WORDS
    SEED_WORDS = dict()

    for word in args.seed.split(','):
        if '/' in word:

            # The slash indicates that we wish to replace the seed
            # word with some root variant of that word.

            (f, r) = word.split('/')
            SEED_WORDS[f] = r
        else:
            SEED_WORDS[word] = word

def set_preknowlege(args):
    global PREKNOWLEDGE

    if args.preknowledge:
        if os.path.isfile(args.preknowledge):
            PREKNOWLEDGE = list()
            with open(args.preknowledge) as fin:
                lines = fin.readlines()
                for line in lines:
                    PREKNOWLEDGE.append( line.strip() )

def readLines():
    global LINES

    LINES = list()
    for line in fileinput.input('-'):
        LINES.append(line)

def process_token(args, token, baseline):
    global SEED_WORDS
    global PREKNOWLEDGE

    tokens = token.split('$')
    (word, pos) = tokens[0:2]

    # Start with the word itself.

    result = word

    # If running in baseline mode, give part of speech in output.

    if baseline:
        result += '*%s*' % pos

    # Give ourselves all numbers and professions as preknowledge.

    if pos in ('n', 'PF'):
        result += '$%s$' % pos 

    else:

        # If this is a seed word, mark it as its own synthetic part
        # of speech.  The SEED_WORDS dict has the words to find as its
        # keys and the word which which to replace that seed word as 
        # the associated value.

        if word in SEED_WORDS.keys():
            result += '$%s$' % SEED_WORDS[word]

        # If this word is included in our preknowledge, mark it with the
        # part of speech from the preknowledge.

        elif token in PREKNOWLEDGE:
            result += '$%s$' % pos

    # Final preprocessing for problematic words

    result = re.sub('--', '-', result)     # Take that, lu2--dingir-rax!

    return result 

def get_filename(i, prefix, baseline):
    return './prepared_corpora/%s%s_%i.txt' % \
        (prefix,
         '_baseline' if baseline else '',
         i)

def update_output(output):
    if args.trainingpercent > 0:
        if args.trainingpercent < 100:
            if random.randint(1, 100) < args.trainingpercent:
                training = True
            else:
                training = False
        else:
            training = True
    else:
        training = False

    for u in output:
        u['active'] = (training == u['training'])

def print_output(args, output, token):
    for u in output:
        if u['active']:
            if token.endswith('$'):

                # Determine whether to hide or show this token
                # based on its POS.

                u['handle'].write( process_token(args,
                                                 token,
                                                 u['baseline']) )
            else:

                # This isn't a word we're interested in.
                # Pass it through.

                u['handle'].write(token)

def close_handles_output(output):
    for u in output:
        if u['handle']:
            u['handle'].close()
            u['handle'] = None

def parse_mega_corpus(args):
    global LINES

    # File handles.

    ftrain = None
    ftest = None
    fbase = None

    # Generate corpora...

    for i in range(1, args.corporacount + 1):

        # Open file handles.

        if args.trainingpercent > 0:
            ftrain  = open(get_filename(i, 'training', False), 'w')
            ftrainb = open(get_filename(i, 'training', True),  'w')

        if args.trainingpercent < 100:
            ftest   = open(get_filename(i, 'testing', False), 'w')
            ftestb  = open(get_filename(i, 'testing', True),  'w')

        output = [
                    { 'handle':   ftrain,
                      'active':   False,
                      'training': True,
                      'baseline': False },

                    { 'handle':   ftrainb,
                      'active':   False,
                      'training': True,
                      'baseline': True },      # Write *POS* tags.

                    { 'handle':   ftest,
                      'active':   False,
                      'training': False,
                      'baseline': False },

                    { 'handle':   ftestb,
                      'active':   False,
                      'training': False,
                      'baseline': True  } ]    # Write *POS* tags.

        # Iterate over lines in the tagged corpus.

        for line in LINES:
            line = line.strip() 
            if len(line) > 0:
                if line.startswith('&P'):

                    # This line is the start of a new tablet.
                    # Decide which of the file handles we'll be writing to.

                    update_output(output)

                elif not line[0] in '&$@#':
 
                    # This is a line of source text.

                    for token in line.split(' '):
                        print_output(args, output, token)
                        print_output(args, output, ' ')

                    print_output(args, output, '\n')

                else:

                    # This was a comment line; preserve it in the output.

                    print_output(args, output, line + '\n')

        # Close any open file handles.

        close_handles_output(output)

# ====
# Main 
# ====

args = init_parser()
set_seed_words(args)
set_preknowlege(args)
set_rng_seed(args)
readLines()
parse_mega_corpus(args)
