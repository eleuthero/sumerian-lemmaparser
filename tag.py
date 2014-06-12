#!/usr/bin/python

import sys
from sys       import stdin

from itertools import tee, izip
from tablet    import *

MAX_TABLETS = int(sys.argv[1]) if (len(sys.argv) >= 2) else 100000

TABLETS = { }

def pairwise(iter):
    a, b = tee(iter)
    next(b, None)
    return izip(a, b)

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
        elif 'exit' == verb:
            exit(0)
        elif 'quit' == verb:
            exit(0)

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

    
# ======================

stats = parse()

print "Loaded %i of %i tablets:" % stats

"""
for t in TABLETS:
    tablet = TABLETS[t]
    print "\t%s (%i lines)" % ( tablet.name, len(tablet.lines) )
    for l in tablet.lines:
        print "\t\t%s (%i words)" % ( l.line, len(l.words) )
        for w in l.words:
            print "\t\t\t%s (%i lemma rules)" % ( w.word, len(w.lem.rules) )
            for r in w.lem.rules:
                if isinstance(r, LemmaTag):
                    print "\t\t\t\t%s" % r.tag
                elif isinstance(r, LemmaRoot):
                    print "\t\t\t\t%s = %s" % (r.root, r.gloss)
"""


"""
for w in sorted(WORDS):
    words = WORDS[w]
    for word in words:
        print "\t\t\t%s (%i lemma rules)" % ( word.word, len(word.lem.rules) )
        for r in word.lem.rules:
            if isinstance(r, LemmaTag):
                print "\t\t\t\t%s" % r.tag
            elif isinstance(r, LemmaRoot):
                print "\t\t\t\t%s = %s" % (r.root, r.gloss)
"""




result = True

while result:
    print "Sumerian$ ",
    line = stdin.readline()
    if line:
        result = process(line)
    else:
        result = False




