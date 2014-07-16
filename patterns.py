#!/usr/bin/python

import argparse
import operator
from itertools import tee, izip
from sys       import stdout

INDEX = { }

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('-t1', '--threshold1',
                        type=int, default=10000,
                        help='Minimum number of attestations required for '
                             'pattern to be returned.')

    parser.add_argument('-t2', '--threshold2',
                        type=int, default=1000,
                        help='Minimum number of attestations required for '
                             'pattern to be returned in the list of patterns '
                             'preceding or following a pattern.')

    return parser.parse_args()

# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3), ... (n, None).
# This is useful because we need to peek at the next line during forward
# iteration to parse the lines in the .atf file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)

def getPattern(line):
    
    # Remove <l> from front of the string and </l> from the end.
    return line[3:-4].strip()

def index(p, n):

    if p in INDEX:
        if n in INDEX[p]['next']:
            INDEX[p]['next'][n] += 1
        else:
            INDEX[p]['next'][n] = 1
    else:
        INDEX[p] = { 'count': 1, 'next': { }, 'prev': { } }
        INDEX[p]['next'][n] = 1

    if n in INDEX:
        if p in INDEX[n]['prev']:
            INDEX[n]['prev'][p] += 1
        else:
            INDEX[n]['prev'][p] = 1
    else:
        INDEX[n] = { 'count': 1, 'next': { }, 'prev': { } }
        INDEX[n]['prev'][p] = 1

    if n:
        INDEX[n]['count'] += 1

def buildIndex(args):

    """
    args:
        lang:     language of tablets to include.
    """

    with open('./cdli_atffull_patterns.txt') as fin:
        p_prev = None
        indexing = True
        for line1, line2 in pairwise(fin):
            line1 = line1.strip()
            line2 = line2.strip()

            if not line2 or line2.startswith('&'):

                # Either end of file or end of tablet.
                # Previous pattern is followed by None.

                if indexing:
                    if p_prev:
                        index(p_prev, None)
                p_prev = None

            elif line2.startswith('#atf') and 'lang' in line2:

                # Check to see whether this tablet is in the
                # desired language.  Toggle the indexing flag.

                indexing = line2.endswith(args.lang)

            elif line2.startswith('<l>'):

                # New line.  Get pattern and index it.

                p_curr = getPattern(line2)

                # p_prev may be None.  That's good; it'll tell us
                # which lines start tablets (i.e. follow None).

                if indexing:
                    index(p_prev, p_curr)
                p_prev = p_curr
  
def process(args):

    """
    args:
        threshold1:   Number of times a pattern must occur to show
                      up in list.
        threshold2:   Number of times a pattern must precede or follow
                      a pattern to show up in list.
    """

    d = sorted(INDEX.items(), key=lambda l: l[1]['count'])
    d.reverse()

    for key in d:
        word = key[0]

        if INDEX[word]['count'] >= args.threshold1:
            print '%-8i %s' % (INDEX[word]['count'], word)

            dp = sorted(INDEX[word]['prev'].items(), key=lambda l: l[1])
            dp.reverse()

            print '  prev:'
            for key_p in dp:
                word_p = key_p[0]

                if INDEX[word]['prev'][word_p] >= args.threshold2:
                    print '    %-8i %s' % (INDEX[word]['prev'][word_p], word_p)

            dn = sorted(INDEX[word]['next'].items(), key=lambda l: l[1])
            dn.reverse()

            print '  next:'
            for key_n in dn:
                word_n = key_n[0]

                if INDEX[word]['next'][word_n] >= args.threshold2:
                    print '    %-8i %s' % (INDEX[word]['next'][word_n], word_n)

            print
# ====
# Main
# ====

args = init_parser()
buildIndex(args)
process(args)

