#!/bin/bash

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE=cdli_atffull.zip

CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_NONLEMMA_FILE=./cdli_atffull_nonlemma.atf
CORPUS_TAGGED_FILE=./cdli_atffull_tagged.atf
CORPUS_TAGGED_PERCENT=10
CORPUS_LINETAGFREQ_FILE=./cdli_atffull_linefreq.txt
CORPUS_PATTERN_FILE=./cdli_atffull_patterns.txt

all: $(CORPUS_FILE) $(CORPUS_LEMMA_FILE) $(CORPUS_NONLEMMA_FILE) $(CORPUS_TAGGED_FILE) \
	$(CORPUS_LINETAGFREQ_FILE) $(CORPUS_PATTERN_FILE)

$(CORPUS_FILE):
	if [ ! -f "$(CORPUS_FILE)" ]; then \
		@echo "Getting full corpus file from CDLI..."; \
		$(WGET) http://www.cdli.ucla.edu/tools/cdlifiles/cdli_atffull.zip -O $(CORPUS_FILE); \
		$(UNZIP) ./cdli_atffull.zip; \
	fi

$(CORPUS_LEMMA_FILE):
	./generate_corpus.py --lemma --lang=sux > $(CORPUS_LEMMA_FILE)
	# ./generate_corpus.py --lemma --lang=akk >> $(CORPUS_LEMMA_FILE)

$(CORPUS_NONLEMMA_FILE):
	./generate_corpus.py --nonlemma --lang=sux > $(CORPUS_NONLEMMA_FILE)
	# ./generate_corpus.py --nonlemma --lang=akk >> $(CORPUS_NONLEMMA_FILE)

$(CORPUS_TAGGED_FILE):
	./tag_corpus.py --nogloss --bestlemma --pf --percent $(CORPUS_TAGGED_PERCENT) --lang=sux > $(CORPUS_TAGGED_FILE)
	# ./tag_corpus.py --nogloss --bestlemma --pf --percent $(CORPUS_TAGGED_PERCENT) --lang=akk >> $(CORPUS_TAGGED_FILE)

$(CORPUS_LINETAGFREQ_FILE):
	./tag_corpus.py --bestlemma --pf --lang=sux --tagsonly --bare \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' \
		| sort | uniq -c | sort -rn > $(CORPUS_LINETAGFREQ_FILE)

$(CORPUS_PATTERN_FILE):
	./tag_corpus.py --bestlemma --lang=sux --pf --tagsonly \
                | sed -e 's/\(\$$n\$$\)\( \1\)*/\1/g' > $(CORPUS_PATTERN_FILE)
	./patterns.py --lang=sux --threshold1=2500 --threshold2=500 > ./temp
	mv ./temp $(CORPUS_PATTERN_FILE)

clean:
	rm -f $(CORPUS_LEMMA_FILE) $(CORPUS_NONLEMMA_FILE) $(CORPUS_TAGGED_FILE) $(CORPUS_LINETAGFREQ_FILE)
	rm -f $(CORPUS_PATTERN_FILE)
