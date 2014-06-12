#!/usr/bin/python

import sys
from sys       import stdin

from itertools import tee, izip
from tablet    import *

# Max number of tablets to parse.

MAX_TABLETS = int(sys.argv[1]) if (len(sys.argv) >= 2) else 100000

TABLETS = { }

# Funny pattern for iterating via a pair of elements.
# (0, 1), (1, 2), (2, 3).  This is useful because we need to peek at
# the next line during forward iteration to parse the lines in the .atf
# file efficiently.

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)

# Parse the tablet corpus file and associate any words with #lem:
# lemmatizations.

def parse():
    global TABLETS

    lemcount = 0
    tabletcount = 0

    print "Parsing ... please wait."
    with open('./cdli_atffull.atf') as fin:

        t = MAX_TABLETS

        for line1, line2 in pairwise(fin):
            if line1.startswith('&'):
                lines = list()
                lines.append(line1)
            elif line2.startswith('&'):
                lines.append(line1)

                tabletcount += 1

                tablet = Tablet(lines)
                if tablet.valid:
                    TABLETS[tablet.name] = tablet
                    lemcount += 1

                    t -= 1
                    if 0 == t:
                        break
                     
                lines = list()
            else:
                lines.append(line1)

    return (lemcount, tabletcount)

def process(line):
    tokens = line.strip().split(' ')

    if len(tokens) > 0:
        verb = tokens[0].lower()

        if 'word' == verb:
            if len(tokens) > 1:
                processWord(tokens[1])
            else:
                processWord(None)
        elif 'line' == verb:
            processLine( ' '.join(tokens[1:]) )
        elif 'tablet' == verb:
            if len(tokens) > 1:
                processTablet(tokens[1])
            else:
                processTablet(None)
        elif 'help' == verb:

            print """Commands:
          tablet <name>
              Prints all lines in tablet.
              ex: tablet P010632
          word <word>
              Prints all parts of speech for all words containing <word>.
              ex: word IGI.DUB.bar
              ex: word iti
          line <word> [<word> ...]
              Prints all parts of speech for all words in line containing words.
              ex: line sza3-asz-ru-um{ki} ba-hul
          quit
          exit
              Exits Sumerian mini-shell."""

        elif 'exit' == verb:
            return False
        elif 'quit' == verb:
            return False

        return True
    else:
        return False
        
def processWord(word):
    found = False

    if word:
        for w in sorted(WORDS):
            attest = WORDS[w]
            if attest.word.find(word) >= 0:
                renderWord(attest)
                found = True
        if not found:
            print "No lemmatized attestations of %s." % word
    else:
        for attest in sorted(WORDS):
            renderWord(WORDS[attest])

def renderWord(attest):
    print "\t\t%s (%i lemmatized attestations)" % (attest.word, attest.count)
    for r in attest.lem.rules:
        if isinstance(r, LemmaTag):
            print "\t\t\t%s" % r.tag
        elif isinstance(r, LemmaRoot):
            print "\t\t\t%s = %s" % (r.root, r.gloss)
    
def processLine(line):
    found = False

    if line:
        for l in LINES:
            attest = LINES[l]
            if attest.line.find(line) >= 0:
                renderLine(attest)
                found = True
        if not found:
            print "Could not find line in lemmatized corpus."

def renderLine(attest):
    print "\t%s" % attest.line
    for word in attest.words:
        renderWord(word)

def processTablet(name):
    found = False

    if name:
        for t in TABLETS:
            attest = TABLETS[t]
            if attest.name == name:
                for line in attest.lines:
                    renderLine(line)
                    found = True
        if not found:
            print "Could not find tablet %s." % name
    else:
        print "Please specify a tablet name (Pnnnnnn)."
            
# ====
# Main
# ====

# Parse the .atf to extract lemmatization information from
# tablets that have it.

stats = parse()
print "Loaded %i of %i tablets:" % stats

# Main shell loop.

result = True

while result:
    print "Sumerian$ ",
    line = stdin.readline()
    if line:
        result = process(line)
    else:
        result = False
