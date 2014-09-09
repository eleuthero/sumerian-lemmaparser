#!/bin/bash

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE=./cdli_atffull.zip
CORPUS_FILE_URL= http://www.cdli.ucla.edu/tools/cdlifiles/cdli_atffull.zip

CORPUS_PERCENT=100
CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_NONLEMMA_FILE=./cdli_atffull_nonlemma.atf
CORPUS_TAGGED_FILE=./cdli_atffull_tagged.atf
CORPUS_BARETAGGED_FILE=./pos_frequency/cdli_atffull_bare.atf
CORPUS_PREPARED_CORPUS_FILE=./cdli_atffull_prepared.atf
CORPUS_TAGFREQ_FILE=./cdli_atffull_tagfreq.txt
CORPUS_LINETAGFREQ_FILE=./cdli_atffull_linefreq.txt
CORPUS_PATTERN_FILE=./cdli_atffull_patterns.txt
CORPUS_PREKNOWLEDGE_FILE=./preknowledge.txt

all: \
	$(CORPUS_FILE) \
	$(CORPUS_LEMMA_FILE) \
	$(CORPUS_NONLEMMA_FILE) \
	$(CORPUS_TAGGED_FILE) \
	$(CORPUS_LINETAGFREQ_FILE) \
	$(CORPUS_PATTERN_FILE) \
	$(CORPUS_PREPARED_CORPUS_FILE) \
	CORPUS_STATISTICS \
	$(CORPUS_PREKNOWLEDGE_FILE)

$(CORPUS_FILE):
	if [ ! -f "$(CORPUS_FILE)" ]; then \
		@echo "Getting full corpus file from CDLI..."; \
		$(WGET) $(CORPUS_FILE_URL) -O $(CORPUS_FILE); \
		$(UNZIP) $(CORPUS_FILE); \
	fi

$(CORPUS_LEMMA_FILE):
	./generate_corpus.py --lemma --lang sux \
		--percent $(CORPUS_PERCENT) \
		> $(CORPUS_LEMMA_FILE)

$(CORPUS_NONLEMMA_FILE):
	./generate_corpus.py --nonlemma --lang sux \
		--percent $(CORPUS_PERCENT) \
		> $(CORPUS_NONLEMMA_FILE)

$(CORPUS_TAGGED_FILE):
	./tag_corpus.py --nogloss --bestlemma --pf \
		> $(CORPUS_TAGGED_FILE)

$(CORPUS_PREPARED_CORPUS_FILE): $(CORPUS_TAGGED_FILE)
	cat $(CORPUS_TAGGED_FILE) \
		| python ./mark_rules.py --seed 'giri3,kiszib3,muDU' \
		> $(CORPUS_PREPARED_CORPUS_FILE)

$(CORPUS_TAGFREQ_FILE):
	./tag_corpus.py --nogloss --bestlemma --pf --tagsonly --bare \
                | sed -e 's/ /\n/g' \
                | sed -e '/^$$/d' \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_TAGFREQ_FILE)

$(CORPUS_LINETAGFREQ_FILE):
	./tag_corpus.py --bestlemma --pf --tagsonly --bare \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' \
		| sort | uniq -c | sort -rn \
		> $(CORPUS_LINETAGFREQ_FILE)

$(CORPUS_PATTERN_FILE):
	./tag_corpus.py --bestlemma --pf --tagsonly \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' \
		> $(CORPUS_PATTERN_FILE)
	./patterns.py --threshold1 2500 --threshold2 500 > ./temp
	mv ./temp $(CORPUS_PATTERN_FILE)

# Corpus statistics by part of speech.

CORPUS_STATISTICS: \
	./pos_frequency/fn_frequency.txt \
	./pos_frequency/gn_frequency.txt \
	./pos_frequency/mn_frequency.txt \
	./pos_frequency/n_frequency.txt \
	./pos_frequency/on_frequency.txt \
	./pos_frequency/tn_frequency.txt \
	./pos_frequency/u_frequency.txt \
	./pos_frequency/wn_frequency.txt
		
$(CORPUS_BARETAGGED_FILE):
	mkdir --parents ./pos_frequency
	./tag_corpus.py --nogloss --bestlemma --pf --bare \
		> $(CORPUS_BARETAGGED_FILE)

./pos_frequency/fn_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$FN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/fn_frequency.txt

	sort -k2.1 ./pos_frequency/fn_frequency.txt \
		> ./pos_frequency/fn_sorted.txt

./pos_frequency/gn_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$GN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sed -e 's/{ki}.*/{ki}/g' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/gn_frequency.txt

	sort -k2.1 ./pos_frequency/gn_frequency.txt \
		> ./pos_frequency/gn_sorted.txt

./pos_frequency/mn_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$MN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/mn_frequency.txt

	sort -k2.1 ./pos_frequency/mn_frequency.txt \
		> ./pos_frequency/mn_sorted.txt

./pos_frequency/n_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$n\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/n_frequency.txt

	sort -k2.1 ./pos_frequency/n_frequency.txt \
		> ./pos_frequency/n_sorted.txt

./pos_frequency/on_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$ON\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/on_frequency.txt

	sort -k2.1 ./pos_frequency/on_frequency.txt \
		> ./pos_frequency/on_sorted.txt

./pos_frequency/tn_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$TN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/tn_frequency.txt

	sort -k2.1 ./pos_frequency/tn_frequency.txt \
		> ./pos_frequency/tn_sorted.txt

./pos_frequency/u_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$u\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/u_frequency.txt

	sort -k2.1 ./pos_frequency/u_frequency.txt \
		> ./pos_frequency/u_sorted.txt

./pos_frequency/wn_frequency.txt: $(CORPUS_BARETAGGED_FILE)
	cat $(CORPUS_BARETAGGED_FILE) \
		| sed -e 's/ /\n/g' \
		| grep '\$$WN\$$' \
		| sed -e '/^$$/d' \
		| awk 'BEGIN { FS="$$"; } { print $$1; }' \
		| sort | uniq -c | sort -rn \
		> ./pos_frequency/wn_frequency.txt

	sort -k2.1 ./pos_frequency/wn_frequency.txt \
		> ./pos_frequency/wn_sorted.txt

# Preknowledge

$(CORPUS_PREKNOWLEDGE_FILE): \
	./pos_frequency/fn_frequency.txt \
	./pos_frequency/gn_frequency.txt \
	./pos_frequency/mn_frequency.txt \
	./pos_frequency/tn_frequency.txt \
	./pos_frequency/wn_frequency.txt
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

clean:
	rm -f $(CORPUS_LEMMA_FILE)
	rm -f $(CORPUS_NONLEMMA_FILE)
	rm -f $(CORPUS_TAGGED_FILE)
	rm -f $(CORPUS_BARETAGGED_FILE)
	rm -f $(CORPUS_PREPARED_CORPUS_FILE)
	rm -f $(CORPUS_TAGFREQ_FILE)
	rm -f $(CORPUS_LINETAGFREQ_FILE)
	rm -f $(CORPUS_PATTERN_FILE)
	rm -f $(CORPUS_PREKNOWLEDGE_FILE)
	rm -f ./pos_frequency/fn_frequency.txt ./pos_frequency/fn_sorted.txt
	rm -f ./pos_frequency/gn_frequency.txt ./pos_frequency/gn_sorted.txt
	rm -f ./pos_frequency/mn_frequency.txt ./pos_frequency/mn_sorted.txt
	rm -f ./pos_frequency/n_frequency.txt  ./pos_frequency/n_sorted.txt
	rm -f ./pos_frequency/on_frequency.txt ./pos_frequency/on_sorted.txt
	rm -f ./pos_frequency/tn_frequency.txt ./pos_frequency/tn_sorted.txt
	rm -f ./pos_frequency/u_frequency.txt  ./pos_frequency/u_sorted.txt
	rm -f ./pos_frequency/wn_frequency.txt ./pos_frequency/wn_sorted.txt
	rm -f ./pos_frequency
