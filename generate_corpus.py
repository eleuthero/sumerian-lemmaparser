#!/usr/bin/python

import fileinput
import argparse
import random
from sys import stdout
from itertools import tee, izip

from tablet import *

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('-r', '--removelemmata',
                        help='Remove any lemmata in generated corpus.',
                        action='store_true')

    return parser.parse_args()

# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3), ... (n, None).
# This is useful because we need to peek at the next line during forward
# iteration to parse the lines in the .atf file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)

def parse(args):
    lemma = False
    valid = False 

    lines = list()
    for line in fileinput.input('-'):
        lines.append(line)

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # our command-line switches as filenames.

    for line1, line2 in pairwise(lines):
        line1 = line1.strip()
        line2 = line2.strip()
        if line1.startswith('&'):
            lemma = False
            valid = False 
            lines = [ ]
            lines.append(line1)
        elif line1.startswith('#atf') and 'lang' in line1:
            lines.append(line1)
            if line1.endswith(args.lang):
               valid = True 
        else:
            if line1.startswith('#lem:'):
                lemma = True
                if not args.removelemmata:
                    lines.append(line1)
            else:
                lines.append(line1)

        if line2.startswith('&'):
            if lemma:
                if valid:
                    for line in lines:
                        stdout.write(line + '\n')
            lemma = False
            valid = False 
            lines = [ ]

# ====
# Main
# ====

args = init_parser()
parse(args)
