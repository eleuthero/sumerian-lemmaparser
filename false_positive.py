#!/usr/bin/python

import fileinput
import operator
from sys import stdout

global POS

def load_tags():
    global POS 

    d = list()
    with open('./pos_frequency/w.txt') as fin:
        POS = dict()
        lines = fin.readlines()
        for line in lines:
            tokens = line.strip().split('$')
            if len(tokens) >= 2:
                word = tokens[0]
                pos = tokens[1]
                if word not in d:
                    d.append(word)
                    POS[word] = pos

def tag_false_positives():
    global POS

    keys = POS.keys()

    # Pass '-' to input() to make sure fileinput doesn't interpret
    # our command-line switches as filenames.

    for line in fileinput.input('-'):
        word = line.strip() 

        if word in keys:
            pos = POS[word]
            if pos in ('u', 'x', 'X'):
                stdout.write('%s$%s$\n' % (word, pos))
        
# ====
# Main 
# ====

load_tags()
tag_false_positives()
