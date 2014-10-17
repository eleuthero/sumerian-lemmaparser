#!/usr/bin/python

import fileinput
from sys import stdout, stderr

# None is used as a PN wildcard in these rules.
# If the pattern matches all other rules, we assume that whatever corresponds
# to None is a PN.

PATTERNS = [
             ['\n', 'dumu*W*', None, '$PF$', '\n'],
             ['\n', None, 'szu*W*', 'ba-ti*W*', '\n'],

             ['\n', 'ki*W*', None, '\n'],
             ['\n', '1(disz)', None, '\n'],
             ['$n$', '$UNIT$', None, '\n'],
             ['\n', '$kiszib$', None, '\n'],
             ['\n', None, '$PF$', '\n'],
             ['\n', '$PF$', None, '\n'],
             ['\n', None, 'i3-dab5*W*', '\n'],

             ['$n$', '$UNIT$', None ],
             ['\n', '$jiri$', None ],
             ['$n$', None, '\n']
           ]

"""
PATTERNS = [
             ['\n', '$jiri$', None ],
             ['$kiszib$', None ],
             ['\n', '$muDU$', None ]
           ]
"""

TRUE_POSITIVE_PNS  = list()
FALSE_POSITIVE_PNS = list()
FALSE_NEGATIVE_PNS = list()

def tokenizeLine(line):
    words = list()
    for word in line.split(' '):
        if len(word) > 0:
            if not word in ['<l>', '</l>']:
                words.append(word)

    words.append('\n')             # Represent line breaks with a newline.
    return words

def matchContext(pattern, context):
    for (p, c) in zip(pattern, context):
        if (None == p):
            yield '$' not in c    # Don't tag anything as a PN if it's
                                  # already been tagged as something else.
        else:
            yield p in c          # Return true if the context contains
                                  # the pattern as a substring.

def testRules(words):
    global PATTERNS 

    for pattern in PATTERNS:
        if len(words) >= len(pattern):
            context = list( words[0:len(pattern)] )

            """
            print 'Testing: pattern: ', pattern
            print '         context: ', context
            print '         results: ', list( matchContext(pattern, context) )
            """

            # Match the pattern to the context.  If all words match
            # (i.e. matchContext() returns a list of nothing but True)
            # we have a winner.

            match = reduce(lambda x, y : x and y,
                           matchContext(pattern, context))

            if match:

                """
                print 'Found match: pattern: ', pattern
                print '             context: ', context
                """

                words[pattern.index(None)] += '$PN$'

    return None

def accumulate(l, word, score):
    if word in l:
        return (0, 0, 0)  # PN already in this list; don't score it again
    else:
        l.append(word)    # Add PN to this list
        return score
   
def verifyMatch(context, word):
    global TRUE_POSITIVE_PNS
    global FALSE_POSITIVE_PNS
    global FALSE_NEGATIVE_PNS

    guess = '$PN$' in word
    truth = '*PN*' in word

    if (guess or truth):
        if (guess == truth):
            """
            print 'TRUE POSITIVE: ', word
            """
            return accumulate( TRUE_POSITIVE_PNS, word, (1, 0, 0) )
        elif (guess):
            context = ' '.join(['<<<' + s + '>>>' if (s == word) else s \
                                for s in context])
            stderr.write('FALSE POSITIVE: %s\n' % context.replace('\n', '::'))
            return accumulate( FALSE_POSITIVE_PNS, word, (0, 1, 0) )
        else:
            context = ' '.join(['>>>' + s + '<<<' if (s == word) else s \
                                for s in context])
            stderr.write('FALSE NEGATIVE: %s\n' % context.replace('\n', '::'))
            return accumulate( FALSE_NEGATIVE_PNS, word, (0, 0, 1) )
    return (0, 0, 0)

def printScore(score):
    print '%i true positives, %i false positives, %i false negatives.' % \
          tuple(score)

def tabulate(a, b):
    return map(lambda (x, y) : x + y, zip(a, b))

def processTablet(words):
    score = (0, 0, 0)
    done = list()

    while len(words) > 0:
        testRules(words)

        context = list()
        context.extend(done[-5:])
        context.append(words[0])
        context.extend(words[1:5])

        score = tabulate(score, verifyMatch( context, words[0] ))
        done.append( words.pop(0) )

    for line in ' '.join(done).split('\n')[:-1]:
        stdout.write('<l> ' + line.strip() + ' </l>\n')

    return score

def baseline():
    score = (0, 0, 0)

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # out command-line switches as filenames.

    words = list()

    for line in fileinput.input('-'):
        if line.startswith('&P'):
            stdout.write(line)
            score = tabulate(score, processTablet(words))
            words = list()
        elif line.startswith('<l>'):
            words.extend( tokenizeLine( line.strip() ))

    score = tabulate(score, processTablet(words))
    printScore(score)

# ====
# Main
# ====

baseline()
