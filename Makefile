#!/bin/bash

SHELL=/bin/bash
WGET=/usr/bin/wget
UNZIP=/usr/bin/unzip

CORPUS_FILE=cdli_atffull.zip

all: $(CORPUS_FILE)

$(CORPUS_FILE):
	if [ ! -f "$(CORPUS_FILE)" ]; then \
		@echo "Getting full corpus file from CDLI..."; \
		$(WGET) http://www.cdli.ucla.edu/tools/cdlifiles/cdli_atffull.zip -O $(CORPUS_FILE); \
		$(UNZIP) ./cdli_atffull.zip; \
	fi
