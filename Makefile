#!/bin/bash

# To create/recreate a prepared corpus, type ``make corpus''.
# To create/recreate a false positive digest, type ``make falsepositive''.
# To do all of the above, type ``make all'.
# To remove all automatically-generated files, type ``make clean''.

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE_ZIP=./cdli_atffull.zip
CORPUS_FILE_URL= http://www.cdli.ucla.edu/tools/cdlifiles/$(CORPUS_FILE_ZIP)
CORPUS_FILE=./cdli_atffull.atf

CORPUS_TRAINING_PERCENT=85
CORPUS_COUNT=1
CORPUS_RNGSEED=1

CORPUS_SEEDWORDS='giri3/jiri,kiszib3/kiszib,mu-DU/muDU,iti/MON,u4/DAY,sze/UNIT,gin2/UNIT,szu-si/UNIT,|SZU.BAD|/UNIT,kusz3/UNIT,gi/UNIT,ninda/UNIT,USZ/UNIT,danna/UNIT,tur/UNIT,ma-na/UNIT,sar/UNIT,GAN2/UNIT,iku/UNIT,sila3/UNIT,gur/UNIT,guru7/UNIT,dug/UNIT,gu2/UNIT,mu/YER,ki/PLC,dumu/SON,i3-dab5/TAK,zi-ga/TAK,szu/GIV,ba-ti/BATI'

CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_TAGGED_FILE=./cdli_atffull_tagged.atf

CORPUS_BARETAGGED_FILE=./pos_frequency/cdli_atffull_bare.atf
CORPUS_TAGFREQ_FILE=./cdli_atffull_tagfreq.txt
CORPUS_TAGFREQUNIQ_FILE=./cdli_atffull_tagfrequniq.txt
CORPUS_LINETAGFREQ_FILE=./cdli_atffull_linefreq.txt
CORPUS_PATTERN_FILE=./cdli_atffull_patterns.txt
CORPUS_PREKNOWLEDGE_FILE=./preknowledge.txt

FALSEPOSITIVE_SOURCEFILE=./fp.txt
FALSEPOSITIVE_DIGESTFILE=./fp_digest.txt
FALSEPOSITIVE_DIGEST_COUNT=50
FALSEPOSITIVE_LINESBEFORE=3
FALSEPOSITIVE_LINESAFTER=3
FALSEPOSITIVE_OUTPUTDIGESTFILE=false_positive_digest.atf

all: corpus falsepositive

# Generate corpus
# ===============

corpus:	\
	PREPARE_CORPORA \
	$(CORPUS_TAGFREQ_FILE) \
	$(CORPUS_TAGFREQUNIQ_FILE) \
	$(CORPUS_LINETAGFREQ_FILE) \
	$(CORPUS_PATTERN_FILE)

# Fetch compressed CDLI Ur III corpus from source.

$(CORPUS_FILE_ZIP):

	@echo "Getting full corpus file from CDLI..."
	$(WGET) $(CORPUS_FILE_URL) -O $(CORPUS_FILE_ZIP)

# Uncompress CDLI corpus.

$(CORPUS_FILE): $(CORPUS_FILE_ZIP)

	if [ ! -f "$(CORPUS_FILE)" ]; then \
		$(UNZIP) $(CORPUS_FILE_ZIP); \
	fi

# Filter corpus to generate lemmatized portion.

$(CORPUS_LEMMA_FILE): $(CORPUS_FILE)

	cat $(CORPUS_FILE) \
		| python ./generate_corpus.py \
			--lang sux \
		> $(CORPUS_LEMMA_FILE)

# From the lemmatized corpus, generate a tagged corpus.

$(CORPUS_TAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf \
		> $(CORPUS_TAGGED_FILE)

	python ./rmNoise.py $(CORPUS_TAGGED_FILE) temp
	mv temp $(CORPUS_TAGGED_FILE)

# From the tagged corpus and a preknowledge file, generate our final
# prepared corpora.

./prepared_corpora:

	mkdir --parents ./prepared_corpora

PREPARE_CORPORA: \
	./prepared_corpora \
	$(CORPUS_TAGGED_FILE) \
	$(CORPUS_PREKNOWLEDGE_FILE)

	cat $(CORPUS_TAGGED_FILE) \
		| python ./prepare.py \
			--seed $(CORPUS_SEEDWORDS) \
			--rngseed $(CORPUS_RNGSEED) \
			--trainingpercent $(CORPUS_TRAINING_PERCENT) \
			--corporacount $(CORPUS_COUNT) \
			--preknowledge $(CORPUS_PREKNOWLEDGE_FILE)

        # Generate baselines.

	cd ./prepared_corpora; \
	for file in `ls training_baseline_*.txt testing_baseline_*.txt`; \
	do \
		cat $$file \
			| python ../baseline.py \
			>  output_$$file \
			2> whiffs_$$file; \
	done

	# Report on baseline true positives, false positives, and false
	# negatives.

	cd ./prepared_corpora; \
	for file in `ls output_training_baseline_*.txt output_testing_baseline_*.txt`; \
	do \
		tail -1 $$file; \
	done

	# Generate a list of PNs, RNs, and DNs in baseline files.
        # The baseline file is the same as the testing file, except that
        # it contains "hidden" parts of speech tags.

	cd ./prepared_corpora; \
	for fin in `ls training_baseline_*.txt`; \
	do \
		fout=pnrndn_$$fin; \
        	cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*PN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			> $$fout; \
		cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*RN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			>> $$fout; \
		cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*DN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			>> $$fout; \
        	cat $$fout \
			| sort | uniq \
			> temp; \
		mv temp $$fout; \
	done

	cd ./prepared_corpora; \
	for fin in `ls testing_baseline_*.txt`; \
	do \
		fout=pnrndn_$$fin; \
        	cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*PN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			> $$fout; \
		cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*RN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			>> $$fout; \
		cat $$fin \
			| sed -e 's/ /\n/g' \
			| grep '\*DN\*' \
			| sed -e '/^$$/d' \
			| awk 'BEGIN { FS="*"; } { print $$1; }' \
			>> $$fout; \
        	cat $$fout \
			| sort | uniq \
			> temp; \
		mv temp $$fout; \
	done

# Preknowledge
# ============

# Create subdirectory for part-of-speech frequency analysis.

./pos_frequency:

	mkdir --parents ./pos_frequency

# From the corpus statistics, accumulate the heads of each of the sorted
# files to give us the most attested words of each part of speech.  We will
# use these words and their parts of speech as preknowledge for our prepared
# corpus.

$(CORPUS_PREKNOWLEDGE_FILE): \
	./pos_frequency \
	./pos_frequency/fn_frequency.txt \
	./pos_frequency/gn_frequency.txt \
	./pos_frequency/mn_frequency.txt \
	./pos_frequency/n_frequency.txt \
	./pos_frequency/on_frequency.txt \
	./pos_frequency/pn_frequency.txt \
	./pos_frequency/tn_frequency.txt \
	./pos_frequency/u_frequency.txt \
	./pos_frequency/wn_frequency.txt \
	./pos_frequency/w_frequency.txt \
	./pos_frequency/x_frequency.txt \
	./pos_frequency/pf_frequency.txt

	cat ./pos_frequency/fn_frequency.txt \
		| head -50 \
		| awk '{ print $$2 "$$FN$$" }' \
		> $(CORPUS_PREKNOWLEDGE_FILE)

	cat ./pos_frequency/gn_frequency.txt \
		| head -50 \
		| awk '{ print $$2 "$$GN$$" }' \
		>> $(CORPUS_PREKNOWLEDGE_FILE)

	cat ./pos_frequency/mn_frequency.txt \
		| head -50 \
		| awk '{ print $$2 "$$MN$$" }' \
		>> $(CORPUS_PREKNOWLEDGE_FILE)

	cat ./pos_frequency/tn_frequency.txt \
		| head -20 \
		| awk '{ print $$2 "$$TN$$" }' \
		>> $(CORPUS_PREKNOWLEDGE_FILE)

	cat ./pos_frequency/wn_frequency.txt \
		| head -50 \
		| awk '{ print $$2 "$$WN$$" }' \
		>> $(CORPUS_PREKNOWLEDGE_FILE)

# Corpus statistics by part of speech.
# ====================================

# Generate a bare tagged file containing only the words in the lemmatized
# corpus and their associated parts of speech.

$(CORPUS_BARETAGGED_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf --bare \
		> $(CORPUS_BARETAGGED_FILE)

# FN (field name) frequency analysis.

./pos_frequency/fn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$FN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/fn.txt

./pos_frequency/fn_frequency.txt: ./pos_frequency/fn.txt

	cat ./pos_frequency/fn.txt \
		| grep -v "x" \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/fn_frequency.txt

	sort -k2.1 ./pos_frequency/fn_frequency.txt \
		> ./pos_frequency/fn_sorted.txt

# GN (geographical name) frequency analysis.

./pos_frequency/gn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$GN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sed -e 's/{ki}.*/{ki}/g' \
		> ./pos_frequency/gn.txt

./pos_frequency/gn_frequency.txt: ./pos_frequency/gn.txt

	cat ./pos_frequency/gn.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/gn_frequency.txt

	sort -k2.1 ./pos_frequency/gn_frequency.txt \
		> ./pos_frequency/gn_sorted.txt

# MN (month name) frequency analysis.

./pos_frequency/mn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$MN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/mn.txt

	cat ./cdli_months.txt >> ./pos_frequency/mn.txt

	cat ./pos_frequency/mn.txt | sort | uniq \
		>> temp
	mv temp ./pos_frequency/mn.txt

./pos_frequency/mn_frequency.txt: ./pos_frequency/mn.txt

	cat ./pos_frequency/mn.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/mn_frequency.txt

	sort -k2.1 ./pos_frequency/mn_frequency.txt \
		> ./pos_frequency/mn_sorted.txt

# n (number) frequency analysis.

./pos_frequency/n.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$n\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/n.txt

./pos_frequency/n_frequency.txt: ./pos_frequency/n.txt

	cat ./pos_frequency/n.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/n_frequency.txt

	sort -k2.1 ./pos_frequency/n_frequency.txt \
		> ./pos_frequency/n_sorted.txt

# ON (object name) frequency analysis.

./pos_frequency/on.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$ON\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/on.txt

./pos_frequency/on_frequency.txt: ./pos_frequency/on.txt

	cat ./pos_frequency/on.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/on_frequency.txt

	sort -k2.1 ./pos_frequency/on_frequency.txt \
		> ./pos_frequency/on_sorted.txt

# PN (personal name) frequency analysis.

./pos_frequency/pn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$PN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/pn.txt

./pos_frequency/pn_frequency.txt: ./pos_frequency/pn.txt

	cat ./pos_frequency/pn.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/pn_frequency.txt

	sort -k2.1 ./pos_frequency/pn_frequency.txt \
		> ./pos_frequency/pn_sorted.txt

# TN (temple name) frequency analysis.

./pos_frequency/tn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$TN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/tn.txt

./pos_frequency/tn_frequency.txt: ./pos_frequency/tn.txt

	cat ./pos_frequency/tn.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/tn_frequency.txt

	sort -k2.1 ./pos_frequency/tn_frequency.txt \
		> ./pos_frequency/tn_sorted.txt

# u (unlemmatizable) frequency analysis.

./pos_frequency/u.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$u\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/u.txt

./pos_frequency/u_frequency.txt: ./pos_frequency/u.txt

	cat ./pos_frequency/u.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/u_frequency.txt

	sort -k2.1 ./pos_frequency/u_frequency.txt \
		> ./pos_frequency/u_sorted.txt

# WN (watercourse name) frequency analysis.

./pos_frequency/wn.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$WN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/wn.txt

./pos_frequency/wn_frequency.txt: ./pos_frequency/wn.txt

	cat ./pos_frequency/wn.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/wn_frequency.txt

	sort -k2.1 ./pos_frequency/wn_frequency.txt \
		> ./pos_frequency/wn_sorted.txt

# X (unknown) frequency analysis.

./pos_frequency/x.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$X\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/x.txt

./pos_frequency/x_frequency.txt: ./pos_frequency/x.txt

	cat ./pos_frequency/x.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/x_frequency.txt

	sort -k2.1 ./pos_frequency/x_frequency.txt \
		> ./pos_frequency/x_sorted.txt

./pos_frequency/pf.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$PF\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		> ./pos_frequency/pf.txt

./pos_frequency/pf_frequency.txt: ./pos_frequency/pf.txt

	cat ./pos_frequency/pf.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/pf_frequency.txt

	sort -k2.1 ./pos_frequency/pf_frequency.txt \
		> ./pos_frequency/pf_sorted.txt

# all words frequency analysis.

./pos_frequency/w.txt: $(CORPUS_BARETAGGED_FILE)
# all words frequency analysis.

./pos_frequency/w.txt: $(CORPUS_BARETAGGED_FILE)

	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
                | sed -e '/^$$/d' \
		> ./pos_frequency/w.txt

./pos_frequency/w_frequency.txt: ./pos_frequency/w.txt

	cat ./pos_frequency/w.txt \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/w_frequency.txt

	sort -k2.1 ./pos_frequency/w_frequency.txt \
		> ./pos_frequency/w_sorted.txt

# Secondary tag- and line-frequency analyses
# ==========================================
# From the lemmatized portion of the corpus, generate a tag frequency
# analysis.

$(CORPUS_TAGFREQ_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf --tagsonly --bare \
                | sed -e 's/ /\n/g' \
                | sed -e '/^$$/d' \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_TAGFREQ_FILE)

$(CORPUS_TAGFREQUNIQ_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--nogloss --bestlemma --pf --bare \
                | sed -e 's/ /\n/g' \
                | sed -e '/^$$/d' \
		| sort | uniq \
		| awk 'BEGIN { FS="$$"; } { print FS $$2 FS; }' \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_TAGFREQUNIQ_FILE)

# From the lemmatized portion of the corpus, generate a frequency analysis
# of lines reduced to their parts of speech.

$(CORPUS_LINETAGFREQ_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--bestlemma --pf --tagsonly --bare \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_LINETAGFREQ_FILE)

# From the lemmatized portion of the corpus, generate a frequency analysis
# of which sentence patterns precede and succeed other sentence patterns.

$(CORPUS_PATTERN_FILE): $(CORPUS_LEMMA_FILE)

	cat $(CORPUS_LEMMA_FILE) \
		| python ./tag_corpus.py \
			--bestlemma --pf --tagsonly \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' \
		> $(CORPUS_PATTERN_FILE)
	./patterns.py --threshold1 1000 --threshold2 100 > ./temp
	mv ./temp $(CORPUS_PATTERN_FILE)

# False positive digest generation
# ================================

falsepositive: $(FALSEPOSITIVE_DIGESTFILE)

	# Generate a digest of the contexts of a subset of the false
	# positives.

	while read -r line; do \
		grep -B $(FALSEPOSITIVE_LINESBEFORE) \
			-A $(FALSEPOSITIVE_LINESAFTER) \
			--max-count 1 \
			" $$line" $(CORPUS_TAGGED_FILE); \
		echo "---------"; \
		done \
	< $(FALSEPOSITIVE_DIGESTFILE) \
	> $(FALSEPOSITIVE_OUTPUTDIGESTFILE)

$(FALSEPOSITIVE_DIGESTFILE): \
	$(FALSEPOSITIVE_SOURCEFILE)

	cat $(FALSEPOSITIVE_SOURCEFILE) \
		| python false_positive.py \
		> $(FALSEPOSITIVE_DIGESTFILE)

	shuf -n $(FALSEPOSITIVE_DIGEST_COUNT) $(FALSEPOSITIVE_DIGESTFILE) \
		> temp
	mv temp  $(FALSEPOSITIVE_DIGESTFILE)

	cat $(FALSEPOSITIVE_DIGESTFILE) \
		| awk 'BEGIN { FS="$$"; OFS="[$$]"; } { print $$1,$$2,"" }' \
		> temp
	mv temp $(FALSEPOSITIVE_DIGESTFILE)

# Cleanup
# =======

clean:
	rm -f $(CORPUS_LEMMA_FILE)
	rm -f $(CORPUS_TAGGED_FILE)
	rm -rf ./prepared_corpora
	rm -f $(CORPUS_BARETAGGED_FILE)
	rm -f $(CORPUS_TAGFREQ_FILE)
	rm -f $(CORPUS_TAGFREQUNIQ_FILE)
	rm -f $(CORPUS_LINETAGFREQ_FILE)
	rm -f $(CORPUS_PATTERN_FILE)
	rm -f $(CORPUS_PREKNOWLEDGE_FILE)
	rm -f $(FALSEPOSITIVE_DIGESTFILE)
	rm -f $(FALSEPOSITIVE_OUTPUTDIGESTFILE)
	rm -rf ./pos_frequency
