#!/usr/bin/python

import argparse
from itertools import tee, izip

from tablet import *

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--count',
                        type=int, default=100000,
                        help='Maximum number of tablets in generated corpus.')

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('-r', '--removelemmata',
                        help='Remove any lemmata in generated corpus.',
                        action='store_true')

    g = parser.add_mutually_exclusive_group()

    g.add_argument('-l', '--lemma',
                   help='Generate a corpus of tablets containing lemmata',
                   action='store_true')

    g.add_argument('-u', '--nonlemma',
                   help='Generate a corpus of tablets not containing lemmata',
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

    # lemmatized: if True, only tablets with one or more lemmata are returned.
    #             if False, only tablets with no lemmata are returned.
    #             if None, all tablets are returned, regardless of lemmata.
    # count:      maximum number of tablets returned.

    lemma = False
    lines = [ ]
    count = args.count
    valid = True

    with open('./cdli_atffull.atf') as fin:
        for line1, line2 in pairwise(fin):
            line1 = line1.strip()
            line2 = line2.strip()
            if line1.startswith('&'):
                lemma = False
                valid = True 
                lines = [ ]
                lines.append(line1)
            elif line1.startswith('#atf') and 'lang' in line1:
                lines.append(line1)
                if not line1.endswith(args.lang):
                    valid = False
            else:
                if line1.startswith('#lem:'):
                    lemma = True
                    if not args.removelemmata:
                        lines.append(line1)
                else:
                    lines.append(line1)

            if line2.startswith('&'):
                if (lemma and args.lemma) or (not lemma and args.nonlemma):
                    if valid:
                        for line in lines:
                            print line

                        count -= 1
                        if 0 == count:
                            return

                lines = [ ]
                lemma = False
                valid = True 
# ====
# Main
# ====

parse( init_parser() )
