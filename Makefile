#!/bin/bash

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE=cdli_atffull.zip

CORPUS_LEMMA_FILE=./cdli_atffull_lemma.atf
CORPUS_NONLEMMA_FILE=./cdli_atffull_nonlemma.atf
CORPUS_TAGGED_FILE=./cdli_atffull_tagged.atf
CORPUS_LINETAGFREQ_FILE=./cdli_atffull_linefreq.txt

all: $(CORPUS_FILE) $(CORPUS_LEMMA_FILE) $(CORPUS_NONLEMMA_FILE) $(CORPUS_TAGGED_FILE) $(CORPUS_LINETAGFREQ_FILE)

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
	./tag_corpus.py --nogloss --bestlemma --lang=sux > $(CORPUS_TAGGED_FILE)
	# ./tag_corpus.py --nogloss --bestlemma --lang=akk >> $(CORPUS_TAGGED_FILE)

$(CORPUS_LINETAGFREQ_FILE):
	./tag_corpus.py --bestlemma --lang=sux --tagsonly --bare \
		| sort | uniq -c | sort -rn > $(CORPUS_LINETAGFREQ_FILE)

clean:
	rm -f $(CORPUS_LEMMA_FILE) $(CORPUS_NONLEMMA_FILE) $(CORPUS_TAGGED_FILE) $(CORPUS_LINETAGFREQ_FILE)
