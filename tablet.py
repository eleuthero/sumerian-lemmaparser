#!/usr/bin/python

from itertools import tee, izip
import repr

LINES = { }
WORDS = { }

class Tablet:
    def __init__(self, lines):
        self.lines = list()
        self.parse(lines)

    def pairwise(self, iter):
        a, b = tee(iter)
        next(b, None)
        return izip(a, b)

    def parse(self, lines):
        self.name = lines.pop(0)[1:8]
        for line1, line2 in self.pairwise(lines):
            if line2:
                self.test(line1.strip(), line2.strip())
        self.valid = ( len(self.lines) > 0)

    def test(self, line1, line2):
        global LINES

        if line2.startswith('#lem:'):
            l = Line(line1, line2[5:])
            if l.valid:
                self.lines.append(l)
                if not line1 in LINES:
                    LINES[line1] = l

class Line:
    def __init__(self, line, lem):
        self.line = line
        self.words = list()
        self.parse(line, lem)

    def parse(self, line, lem):
        global WORDS

        words        = [ s.strip() for s in line.split(' ')[1:] ]
        lemtokensets = [ s.strip() for s in  lem.split(';') ]

        """
        assert len(words) == len(lemtokensets), \
               'tokenization mismatch:\n\t(%2i) : %s\n\t(%2i) : %s' \
               % (len(words), words, len(lemtokensets), lemtokensets)
        """

        self.valid = ( len(words) == len(lemtokensets) )

        if self.valid:
            for i in range(len(words)):
                word = Word( words[i], lemtokensets[i] )
                if word.valid:
                    self.words.append(word)

                    if not word.word in WORDS:
                        WORDS[word.word] = word
                    else:
                        attest = WORDS[word.word]
                        attest.count += 1

                        l = [ str(rule) for rule in attest.lem.rules ]
                        for rule in word.lem.rules:
                            if not str(rule) in l:
                                attest.lem.rules.append(rule)

class Word:
    def __init__(self, word, lemtokenset):
        self.word  = word
        self.count = 1
        self.lem   = Lemma(lemtokenset)
        self.valid = self.lem.valid

    """
    def __eq__(self, other):
        return isinstance(other, self.__class__)  \
            and (self.word == other.word) \
            and (self.lem == other.lem)

    def __ne__(self, other):
        return not self.__eq__(other)
    """

class Lemma:
    def __init__(self, tokens):
        self.rules = list()
        self.parse(tokens)
     
    def parse(self, tokens):
        self.valid = True
        for token in tokens.split('|'):
            if '[' in token:
                lemma = LemmaRoot(token)
                if lemma.valid: 
                    self.rules.append(lemma)
                else:
                    self.valid = False
            else:
                lemma = LemmaTag(token)
                if lemma.valid:
                    self.rules.append(lemma)
                else:
                    self.valid = False

    """
    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and (self.rules == other.rules)

    def __ne__(self, other):
        return not self.__eq__(other)
    """
    
class LemmaTag:
    def __init__(self, tag):
        self.tag   = tag 
        self.valid = True

    def __str__(self):
        return self.tag
        
class LemmaRoot:
    def __init__(self, root):
        tokens = root.replace(']', '').split('[')
            
        assert 2 == len(tokens), \
            "Encountered more than just a root and gloss in lemma root."

        if (2 == len(tokens)):
            self.root  = tokens[0].strip()
            self.gloss = tokens[1].strip()
            self.valid = True
        else:
            self.valid = False
            print "~lem: ", root

    def __str__(self):
        return "%s = %s" % (self.root, self.gloss)
