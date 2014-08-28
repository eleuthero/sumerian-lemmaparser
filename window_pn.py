#!/usr/bin/python

import argparse
import fileinput
import pickle
import operator

def init_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('-w', '--width',
                        type=int, default=3, choices=range(1, 11),
                        help='Radius of context window.')

    parser.add_argument('-i', '--ignorebreaks',
                        action='store_true',
                        help='Ignore line and column breaks.')

    return parser.parse_args()

def read_pickled_dict():
    p = ''

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # our command-line switches as filenames.

    for line in fileinput.input('-'):
        p += line

    return pickle.loads(p)

def reduce_tag(l):
    r = list()

    for word in l:
        if '$' in word:

            # This word has been tagged as a part of speech.

            tokens = word.split('$')

        else:

            # This word wasn't lemmatized.  It's probably a synthetic
            # tag we use to mark the beginning or ending of lines or
            # columns or tablets (i.e. <l>, </p>).

            if args.ignorebreaks:
                continue

            r.append(word)
            continue

        # If we're still in the loop, deal with the tokens.

        if (3 == len(tokens)):

            # This word is tagged with lemma information.
            # The token at index 1 contains the gloss root if the
            # token is a word, or the part of speech tag if not.

            r.append(tokens[1])

        else:
          
            # This word isn't tagged; whatever it is, preserve it.

            r.append(tokens[0])

    return r
           
def find_ngrams(l):

    # Find all n-grams of l where n = range(len(l)) that contain a
    # false-negative name. 

    for n in range(len(l)):

        # This is a clever idiom that clusters a list into n-length tuples.

        for q in zip(*[ iter(l) ]*n):

            # Return a list generated from the tuple if it contains a PN.

            if 'PN' in q:
                yield list(q)

def parse_mega_corpus(args):
    d = read_pickled_dict()

    # This will be our running dict that tracks patterns that contain
    # a PN (key) and the number of times this pattern has been seen
    # (value).

    g = dict()

    for key in d:
        tokens = d[key].split(' ')
        n = len(tokens)
        for i in range(n):
            token = tokens[i]

            # For each word in each line in the tagged corpus, check to
            # see if the word is tagged as PN.  If so, investigate
            # its context.

            if '$PN$' in token:

                u = max(i - args.width, 0)
                v = min(i + args.width + 1, n)
                context = reduce_tag( tokens[u:v] )

                # Find all ngrams containing the false-negative PN and
                # accumulate them in the running dictionary.

                for ngram in find_ngrams(context):
                    pattern = ' '.join(ngram)
                    if pattern in g:
                        g[pattern] += 1
                    else:
                        g[pattern] = 1

    return g

def render_patterns(d):

    # Order the dictionary by values.

    s = sorted(d.iteritems(),
               key=operator.itemgetter(1),
               reverse=True)

    # Render all n-grams containing false-negative PNs that occur at
    # least 100 times.

    for tuple in s:
        if tuple[1] >= 100:
            print '%8i %s' % (tuple[1], tuple[0])
       
# ====
# Main 
# ====

args = init_parser()
d = parse_mega_corpus(args)
render_patterns(d)
