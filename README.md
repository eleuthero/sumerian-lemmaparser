sumerian-lemmaparser
====================

Analyzes a Sumerian corpus to associate any lemmata it contains with the words
that the lemmata rows refer to.  For instance, in the corpus, especially with
older transliterations, there are lemma comments immediately following each line
of transliterated text, e.g.:

4. GAN2 ur-{gesz}gigir nu-banda3 gu4
#lem: iku[unit]; PN; nubanda[overseer]; gud[ox]

These lemmata are very helpful for learning the language, but are also useful
for testing natural-language algorithms to test recall.  In the above case,
the transliterated Sumerian words are matched up with either their stems and a
personal name (PN) is identified. 

This repository creates a "mini-shell" that downloads and unzips the Sumerian
corpus from CDLI, the Cuneiform Digital Library Initiative (http://www.cdli.ucla.edu),
unzips it, parses the corpus to associate any lemmata it contains with the rows the
lemmata describe, and then provides a shell-like interface for querying the data.

To get started, do a ``make all`` to download and prepare the corpus.  Then,
you can run ``python tag.py`` at the shell to begin.  The ``tag.py`` script will
parse the corpus.  At the time of writing, there are 53146 tablets out of 85458 that
contain at least one lemma.  The processing of the corpus may take a couple moments;
please be patient.  Once completed, the script will present a ``Sumerian$ `` prompt.

At this point, you have the following options:

- ``word <sumerian_word>``: This will return the lemmata for the specified word.
For instance, to get all lemmata for the word "kiszib3":

``Sumerian$ word kiszib3
		...
		kiszib3 (19038 lemmatized attestations)
			kiszib = seal
			kiszib = sealed tablet
			dub = tablet
			kiszib3 = seal
			kiszib3 = hand
		kiszib3! (6 lemmatized attestations)
			kiszib = seal
		kiszib3!(URUDU) (1 lemmatized attestations)
			kiszib = seal
		...``

Similarly, to return lemmata for the partial name "ab-ba-sag10":

``Sumerian$ word ab-ba-sag10
 		a-ab-ba-sag10 (1 lemmatized attestations)
			PN
		ab-ba-sag10 (132 lemmatized attestations)
			PN
			FN
		ab-ba-sag10# (5 lemmatized attestations)
			PN
			FN
		ab-ba-sag10#? (2 lemmatized attestations)
			PN
			FN``

You can enter ``word`` by itself to get all lemmata for all words in the corpus,
but I wouldn't recommend it.

- ``line <word> [<word> ...]: This will return the lemmata for all words from all
lines that match the specified sequence of words.  For every word in every matched
line, the available lemmata will be expanded.  For instance:

``Sumerian$ line sza3-asz-ru-um{ki} ba-hul
	...
 	4. iti nesag2 mu sza3-asz-ru-um{ki} ba-hul
		iti (1 lemmatized attestations)
			itud = month
		nesag2 (1 lemmatized attestations)
			nesaj = offering
		mu (1 lemmatized attestations)
			mu = year
		sza3-asz-ru-um{ki} (1 lemmatized attestations)
			GN
		ba-hul (1 lemmatized attestations)
			hulu = destroy
	1. mu sza3-asz-ru-um{ki} ba-hul
		mu (1 lemmatized attestations)
			mu = year
		sza3-asz-ru-um{ki} (1 lemmatized attestations)
			GN
		ba-hul (1 lemmatized attestations)
			hulu = destroy
	10. mu us2-sa sza3-asz-ru-um{ki} ba-hul
		mu (1 lemmatized attestations)
			mu = year
		us2-sa (1 lemmatized attestations)
			us = follow
		sza3-asz-ru-um{ki} (1 lemmatized attestations)
			GN
		ba-hul (1 lemmatized attestations)
			hulu = destroy
	...``

You can enter ``line`` by itself to get all lemmata for all lines in the corpus, but
I really wouldn't recommend it.

You can quit the shell by entering ``exit`` or ``quit``.
