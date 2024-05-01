# Variables
BIRDS := PFW_all_2021_2023_June2023_Public
BIRDS_RAW := raw/${BIRDS}.csv
BIRDS_COOKED := cooked/birds-ca.csv
BIRDS_CONVERT := bin/birds-ca.py
SPECIES := PFW_spp_translation_table_May2023
SPECIES_RAW := raw/${SPECIES}.csv
SPECIES_COOKED := cooked/species-ca.csv
SPECIES_CONVERT := bin/species-ca.py
DB := feederwatch.db
DB_MAKE := bin/make-db.sql

# By default, show available commands (by finding '##' comments)
.DEFAULT: commands

## commands: show available commands
.PHONY: commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} \
	| sed -e 's/## //g' \
	| column -t -s ':'

## get: get raw data (too large for GitHub)
.PHONY: get
get:
	@mkdir -p raw
	wget https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/${BIRDS}.zip
	unzip ${BIRDS}.zip
	mv ${BIRDS}.csv raw
	wget https://clo-pfw-prod.s3.us-west-2.amazonaws.com/data/202306/${SPECIES}.zip
	unzip ${SPECIES}.zip
	mv ${SPECIES}.csv raw
	@touch raw/*.csv
	@rm -rf *.zip __MACOSX

## data: re-build data files
data: ${DB}

${DB}: ${BIRDS_COOKED} ${SPECIES_COOKED}
	@rm -f ${DB}
	sqlite3 ${DB} < ${DB_MAKE}

${BIRDS_COOKED}: ${BIRDS_RAW} ${BIRDS_CONVERT}
	@mkdir -p cooked
	python ${BIRDS_CONVERT} ${BIRDS_RAW} ${BIRDS_COOKED}

${SPECIES_COOKED}: ${SPECIES_RAW} ${SPECIES_CONVERT}
	@mkdir -p cooked
	python ${SPECIES_CONVERT} ${SPECIES_RAW} ${SPECIES_COOKED}

## settings: show variables
.PHONY: settings
settings:
	@echo "BIRDS_CONVERT:" ${BIRDS_CONVERT}
	@echo "BIRDS_COOKED:" ${BIRDS_COOKED}
	@echo "BIRDS_RAW:" ${BIRDS_RAW}
	@echo "DB:" ${DB}
	@echo "DB_MAKE:" ${DB_MAKE}
	@echo "SPECIES_CONVERT:" ${SPECIES_CONVERT}
	@echo "SPECIES_COOKED:" ${SPECIES_COOKED}
	@echo "SPECIES_RAW:" ${SPECIES_RAW}

## clean: clean up stray files
.PHONY: clean
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r
	@find . -type d -name .pytest_cache | xargs rm -r
