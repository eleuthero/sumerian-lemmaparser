#!/usr/bin/python

import argparse
import operator
import random
from itertools import tee, izip
from sys       import stdout

index = { }
noise = '[]!?#*<>'

# List of professions.  If the --pf switch is provided, any lemma
# with the following roots will be marked with the PF part-of-speech
# tag.

professions = [
                "aga'us[soldier]",
                "arad[slave]",
                "aszgab[leatherworker]",
                "azlag[fuller]",
                "bahar[potter]",
                "bisajdubak[archivist]",
                "damgar[merchant]",
                "dikud[judge]",
                "dubsar[scribe]",
                "en[priest]",
                "ereszdijir[priestess]",
                "ensik[ruler]",
                "engar[farmer]",
                "enkud[tax-collector]",
                "gaba'asz[courier]",
                "galamah[singer]",
                "gala[singer]",
                "geme[worker]",
                "gudug[priest]",
                "guzala[official]",
                "idu[doorkeeper]",
                "iszib[priest]",
                "kaguruk[supervisor]",
                "kasz[runner]",
                "kijgia[messenger]",
                "kinkin[miller]",
                "kuruszda[fattener]",        # (of animals)
                "kusz[official]",
                "lugal[king]",
                "lungak[brewer]",
                "malah[sailor]",
                "maszkim[administrator]",
                "muhaldim[cook]",
                "muszendu[bird-catcher]",
                "nagada[herdsman]",
                "nagar[carpenter]",
                "nar[musician]",
                "nubanda[overseer]",
                "nukirik[horticulturalist]",
                "sajDUN[recorder]",
                "sajja[official]",
                "simug[smith]",
                "sipad[shepherd]",
                "sukkal[secretary]",
                "szabra[administrator]",
                "szagia[cup-bearer]",
                "szakkanak[general]",
                "szej[cook]",
                "szu'i[barber]",
                "szukud[fisherman]",
                "ugula[overseer]",
                "unud[cowherd]",
                "ujjaja[porter]",
                "uszbar[weaver]",
                "zabardab[official]",
                "zadim[stone-cutter]"
              ]

# Initializer arg parser.

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--percent',
                        type=int, default=100, choices=range(1, 100),
                        help='Percent of qualifying tablets to include in '
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

    parser.add_argument('--pf',
                        action='store_true',
                        help='Replace common titles and professions with '
                             'PF part-of-speech tag.')

    parser.add_argument('--bare',
                        action='store_true',
                        help='Include only lemmatized lines in output.')

    parser.add_argument('--tagsonly',
                        action='store_true',
                        help='Include only POS tags in output; do not ' \
                             'include the source text.')

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

    if ('[' in lem) and (']' in lem):

        if args.pf:
            if lem in professions:
                return 'PF'
        
        if args.nogloss:
            return 'W'

    return lem

def printWord(word, args):

    if not args.tagsonly:
        stdout.write(word)

    if word in index:
        if args.bestlemma:

            # We want to show only the best lemma for this word ...

            bestcount = max([ index[word][lem] \
                              for lem in index[word] ])
            bestlem   = [ lem for lem in index[word] \
                              if bestcount == index[word][lem] ][0]

            stdout.write( '$%s$ ' % formatLem(lem, args) )

        else:

            # Show all lemmata for this word.

            tokens = [ ]

            for lem in index[word]:
                tokens.append('%s:%i' % (formatLem(lem, args),    # lem
                                         index[word][lem]))       # count

            stdout.write( '$%s$ ' % ','.join(tokens) )

    else:

        # Word is not lemmatized anywhere in corpus.
        # Mark with X tag to signify unknown part of speech.

        stdout.write('$X$ ')
      
def process(line, args):

    if len(line) > 0 and not line[0] in '&$@#':

        if not args.bare:
            print '<l> ',

        # Skip first word in the line; that's a line number.

        for word in line.split(' ')[1:]:

            # Remove all transliteration noise first.

            word = word.translate(None, noise)
            printWord(word, args)

        if not args.bare:
            print '</l>'
        else:
            print

    else:

        # Entire line is a comment or directive.

        if not args.bare:
            print line

def parse(args):

    lemma = False
    lines = [ ]
    valid = True

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
                        if random.randint(1, 100) <= args.percent:
                            process(line, args)

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
