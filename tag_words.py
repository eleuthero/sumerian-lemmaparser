#!/usr/bin/python

import argparse
import operator
import fileinput
import re
from itertools import tee, izip
from sys       import stdout

# Index dictionary mapping words to their attested parts of speech and
# the count for each of those POS.  

index = { }              # { 'x': { 'u' : 0 } }
noise = '[]!?#*<>'

# Regular expressions used in massaging transliteration noise in lines.

# Implied signs: <<...>> indicates that the transliterator believes that
# the scribe has left out one or more signs.  These omitted signs will
# not appear in the lemmatization and so we need to remove the implied
# signs.

re_impl = re.compile(r"\<\<([A-Za-z0-9-()/#?*{}|@+ ]+)\>\>") 

re_slash = re.compile(r"(/)[^0-9]")

# Word regex; if a word doesn't match this regex, just ignore it; don't
# try to tag it.  This is necessary because of some transliterational typos,
# especially in older tablets, to prevent noise like commas from appearing
# as their own words.

re_word = re.compile(r"[A-Za-z0-9-]")

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

    def clean(self, line, lem):

        # Remove any independent comma tokens.

        line = line.replace(' , ', ' ')

        # Remove commas at the end of the line.

        if line.endswith(','):
            line = line[:-1]

        # Delete any implied signs <<...>>.

        line = re_impl.sub('', line)

        """
        # Deal with slashes; they may be either " " or "-".
        # Note: This has been commented out because the lemmata always
        # treat "erroneous" slashes as sign separators, even when the
        # signs are clearly meant to be word-broken, so there must be some
        # lemmatization rule that is being adhered to that I just don't
        # understand, as evidenced by the fact that the number of lemma tokens
        # is always equal to the number of words in the line when there is
        # a slash present.  We'll treat the slash as a sign separator.

        m = re_slash.search(line)

        if m:
   
            words  = [ s.strip().translate(None, '[]!?#*<>') \
                       for s in line.split()[1:] ]
            lemtok = [ s.strip()
                       for s in lem.split(';') ]

            stdout.write("!!! matched bad slash: %i %i %s\n" % \
                         ( len(words), len(lemtok), line ))
            # line = re_slash.sub('', line)
        """
            
        return line

    def parse(self, line, lem):

        line = self.clean(line, lem)

        words  = [ s.strip().translate(None, '[]!?#*<>') \
                   for s in line.split()[1:] ]
        lemtok = [ s.strip()
                   for s in lem.split(';') ]

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
    with open('./cdli_atffull_lemma.atf') as fin:
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

    # Check to make sure the word is not noise (such as a bare comma).
    # If it is, just bail.

    if not re_word.search(word):
        return

    # If we're not just emitting part of speech tags, emit the word.

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

def cleanWord(word):

    # Remove all transliteration noise.
    
    word = word.translate(None, noise)

    # [...] indicates the loss of an indeterminate number of
    # signs.  Reduce this to x, a single lost sign, for our
    # purposes.

    word = re.sub(r'\.\.\.', 'x', word)

    # There is some additional transliteration noise in the
    # form of bare colons.  I'm not sure what they mean, but
    # they are consistently lemmatized as X, so they're not
    # merely typos.  Let's remove them.

    if ':' == word:
        return None

    # Replace : and . signs (indiciating sign metathesis) with the normal
    # hyphen sign separator.  This is not linguistically defensible, but
    # it's close enough for our immediate purposes.

    word = re.sub('[.:]', '-', word)

    return word

def cleanLine(line):

    if '_' in line:

        # _ occurs in lemmata for Akkadian signs; if we see this anywhere
        # in the line, we need different rules to parse the entire line.
        # We didn't sign up for that.

        return None

    words = None

    # Skip first word in the line; that's a line number.

    for word in line.split(' '):
        word = cleanWord(word)

        if word:
            if ('%a' == word) or ('=' == word):

                # This indicates the language has switched (probably to
                # Akkadian) for the rest of the line.  Stop parsing this
                # and any following signs in this line.

                break

            else:

                words = words or list()
                words.append(word)

    return words

def process(line, args):

    if len(line) > 0 and not line[0] in '&$@#':

        # Clean the line up; there are signs that may cause us to stop
        # processing subsequent signs.

        line = cleanLine(line)

        if line:

            """
            The lines of text may contain inline comments in the form
            ($ ... $).  Oddly, the individual tokens in the inline comments
            are lemmatized individually:

            ki ($ blank space $)-ta
            ki[place]; X; X; X; X

            so we don't want to use a regex to remove the comments; rather,
            we'll just look for the inline comment delimiters and use the
            to set a processing flag.  Any signs interrupted by one of these
            inline comments (like the remaining -ta above) become noise
            in the lemma and we'll ignore them.
            """
           
            comment = False
            for word in line:
                if '($' in word:
                    comment = True
                
                if not comment:
                    printWord(word, args)

                if '$)' in word:
                    comment = False

    else:

        # Entire line is a comment or directive.

        stdout.write(line)

    stdout.write('\n')

def parse(args):

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # our command-line switches as filenames.

    for line in fileinput.input('-'):
        process(line.strip(), args)

# ====
# Main
# ====

args = init_parser()

buildIndex()
optimizeIndex(args)
parse(args)
