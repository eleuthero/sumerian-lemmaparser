#!/usr/bin/python

import argparse
import operator
from itertools import tee, izip

index = { }

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--count',
                        type=int, default=100000,
                        help='Maximum number of tablets in generated corpus.')

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('--bestlemma',
                        action='store_true',
                        help='Include only the most commonly attested lemma for tagged word.')

    return parser.parse_args()

# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3), ... (n, None).
# This is useful because we need to peek at the next line during forward
# iteration to parse the lines in the .atf file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)

class Line:
    def __init__(self, line, lem):
        self.line = line
        self.lem = lem
        self.words = { }
        self.parse(line, lem)

    def parse(self, line, lem):
        words  = [ s.strip().translate(None, '[]!?#*<>') for s in line.split(' ')[1:] ]
        lemtok = [ s.strip() for s in  lem.split(';') ]

        self.valid = ( len(words) == len(lemtok) )

        if self.valid:
            # print self.line
            # print self.lem
            for i in range(0, len(words)):
                word = words[i]
                tokens = lemtok[i]

                self.words[word] = []
                for element in tokens.split('|'):
                    self.words[word].append(element)
                    # print '    %s => %s' % (word, element)
        
def buildIndex():
    with open('./cdli_atffull.atf') as fin:
        for line1, line2 in pairwise(fin):
            line1 = line1.strip()
            line2 = line2.strip()

            if line2.startswith('#lem:'):
                line = Line(line1, line2[5:])
                if line.valid:
                    for word in line.words:
                        if not word in index:
                            index[word] = { }
                        for token in line.words[word]:
                            if token in index[word]:
                                index[word][token] += 1
                            else:
                                index[word][token] = 1

def parse(args):

    """
    args:
      count:      maximum number of tablets returned.
      lang:       language of tablets to include.
      bestlemma:  include only the most commonly attested lemma for tagged word.
    """

    lemma = False
    lines = [ ]
    valid = True
    count = args.count

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
                else:
                    lines.append(line1)

            if line2.startswith('&'):
                if valid:
                    for line in lines:
                        if len(line) > 0 and not line[0] in '&$@#':
                            print '<l> ',
                            for word in line.split(' ')[1:]:
                                if word in index:
                                    tokens = [ ]
                                    word = word.translate(None, '[]!?#*<>')

                                    if args.bestlemma:
                                        bestcount = max([ index[word][lem] for lem in index[word] ])
                                        bestlem   = [ lem for lem in index[word] if bestcount == index[word][lem] ][0]
                                        print '%s$%s$ ' % (word, bestlem),
                                    else:
                                        for lem in index[word]:
                                            tokens.append('%s:%i' % (lem, index[word][lem]))
                                        print '%s$%s$ ' % (word, ','.join(tokens)),

                            print '</l>'
                        else:
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

args = init_parser()

buildIndex()
parse(args)

exit(0)

for word in index:
    print word
    dict = sorted(index[word].iteritems(), key=operator.itemgetter(1))
    dict.reverse()
    for token in dict:
        print '    %s (%i)' % (token[0], token[1])
