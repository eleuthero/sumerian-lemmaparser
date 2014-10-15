#!/usr/bin/python

import argparse
import random
from itertools import tee, izip

from tablet import *

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--trainingpercent',
                        type=int, default=100, choices=range(1, 101),
                        help='Percent of qualifying tablets to include in '
                             'generated corpus.')

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('-r', '--removelemmata',
                        help='Remove any lemmata in generated corpus.',
                        action='store_true')

    parser.add_argument('--lemmafile',
                        default='./cdli_atffull_lemma.atf',
                        help='File to which to output all tablets in the '
                             'corpus bearing at least one lemma.')

    parser.add_argument('--trainingfile',
                        default='./cdli_atffull_training.atf',
                        help='File to which to output training portion of '
                             'corpus.')

    parser.add_argument('--testingfile',
                        default='./cdli_atffull_testing.atf',
                        help='File to which to output testing portion of '
                             'corpus.')

    parser.add_argument('-s', '--seed',
                        type=int, default=None,
                        help='Specifies random number generator seed to use.')

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

    ftraining = None
    ftesting = None
    lemma = False
    valid = False 
    lines = [ ]

    if args.trainingpercent > 0:
        ftraining = open(args.trainingfile, 'w')

    if args.trainingpercent < 100:
        ftesting = open(args.testingfile, 'w')

    with open(args.lemmafile, 'w') as flemma:
        with open('./cdli_atffull.atf') as fin:
            for line1, line2 in pairwise(fin):
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

                            # Write lines to lemma file.

                            for line in lines:
                                flemma.write(line + '\n')

                            # Write line to either training or testing file.

                            if random.randint(1, 100) <= args.trainingpercent:
                                for line in lines:
                                    ftraining.write(line + '\n')
                            else:
                                for line in lines:
                                    ftesting.write(line + '\n')
                    lemma = False
                    valid = False 
                    lines = [ ]

    # Close open any file handles to which we've written training/testing
    # corpora.

    if ftraining:
        ftraining.close()

    if ftesting:
        ftesting.close()

def set_rng_seed(args):
    random.seed(args.seed)

# ====
# Main
# ====

args = init_parser()
set_rng_seed(args)
parse(args)
