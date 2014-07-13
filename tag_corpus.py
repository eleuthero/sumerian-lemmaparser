#!/usr/bin/python

import argparse
import operator
from itertools import tee, izip

index = { }
noise = '[]!?#*<>'

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--count',
                        type=int, default=100000,
                        help='Maximum number of tablets in '
                             'generated corpus.')

    parser.add_argument('--lang',
                        default='sux',
                        help='Language of texts to include.')

    parser.add_argument('--nogloss',
                        action='store_true',
                        help='Suppress translation glosses.  Glosses '
                             'will be replaced by a W tag.')

    parser.add_argument('--bestlemma',
                        action='store_true',
                        help='Include only the most commonly attested '
                             'lemma for tagged word.')

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
        words  = [ s.strip().translate(None, '[]!?#*<>') \
                   for s in line.split(' ')[1:] ]
        lemtok = [ s.strip() for s in  lem.split(';') ]

        # Ensure same number of lemma tokens as words.

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

            # If we see a lemmatization ...

            if line2.startswith('#lem:'):
                line = Line(line1, line2[5:])
                if line.valid:
                    for word in line.words:

                        # Remove all transliteration noise first.

                        word = word.translate(None, noise)

                        if not word in index:
                            index[word] = { }

                        # Track lemma token count.

                        for token in line.words[word]:
                            if token in index[word]:
                                index[word][token] += 1
                            else:
                                index[word][token] = 1

def optimizeIndex(args):

    if args.bestlemma:

        # Optimize index by throwing away all lemmata except for the
        # most attested one for each word.

        for word in index:
            bestcount = max([ index[word][lem] \
                              for lem in index[word] ])
            bestlem   = [ lem for lem in index[word] \
                              if bestcount == index[word][lem] ][0]
            index[word] = { }
            index[word][bestlem] = bestcount

    else:

        # Order entries in index by lemma count.

        """
        for word in index:
            dict = sorted(index[word], key=index[word].get)
            n = index[word]
            index[word] = { }
            for token in dict:
                index[word][token] = n[token]
        """

def formatLem(lem, args):

    if args.nogloss:
        if ('[' in lem) and (']' in lem):
            return 'W'
    return lem

def process(line, args):

    if len(line) > 0 and not line[0] in '&$@#':
        print '<l> ',

        # Skip first word in the line; that's a line number.

        for word in line.split(' ')[1:]:

            # Remove all transliteration noise first.

            word = word.translate(None, noise)

            if word in index:
                tokens = [ ]

                # If we want to show only the best lemma for this word ...

                if args.bestlemma:
                    bestcount = max([ index[word][lem] \
                                      for lem in index[word] ])
                    bestlem   = [ lem for lem in index[word] \
                                  if bestcount == index[word][lem] ][0]
                    print '%s$%s$ ' % (word,
                                       formatLem(bestlem, args)),

                # Show all lemmata for this word.

                else:
                    for lem in index[word]:
                        tokens.append('%s:%i' % (formatLem(lem, args),
                                                 index[word][lem]))
                    print '%s$%s$ ' % (word, ','.join(tokens)),
            else:

                # Word not in index.  Mark as unknown.

                print '%s$X$ ' % word,

        print '</l>'
    else:

        # Entire line is a comment.

        print line

def parse(args):

    """
    args:
      count:      maximum number of tablets returned.
      lang:       language of tablets to include.
      bestlemma:  include only the most commonly attested lemma for
                  tagged word.
      nogloss:    suppress gloss for translations like "udu[sheep]" and
                  replace with a W tag.
    """

    lemma = False
    lines = [ ]
    valid = True
    count = args.count

    with open('./cdli_atffull.atf') as fin:
        for line1, line2 in pairwise(fin):
            line1 = line1.strip()
            line2 = line2.strip()

            # Accumulate lines.

            if line1.startswith('&'):

                # Starting a new tablet.  Restart accumulated lines.

                lemma = False
                valid = True 
                lines = [ ]
                lines.append(line1)

            elif line1.startswith('#atf') and 'lang' in line1:

                # Check that language of tablet agrees with args lang.

                lines.append(line1)
                if not line1.endswith(args.lang):
                    valid = False

            elif line1.startswith('#lem:'):

                # Tablet has at least one lemma.

                lemma = True

            else:
                lines.append(line1)

            # End of tablet ?

            if line2.startswith('&'):

                # Starting a new tablet.  Process accumulated lines.

                if valid:
                    for line in lines:
                        process(line, args)

                    # Stop if we've generated enough output.

                    count -= 1
                    if 0 == count:
                       return

                    # Restart accumulated lines.

                    lines = [ ]
                    lemma = False
                    valid = True 

# ====
# Main
# ====

args = init_parser()

buildIndex()
optimizeIndex(args)
parse(args)
