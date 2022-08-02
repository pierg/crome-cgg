.DEFAULT_GOAL := help
SHELL := bash

DUTY = $(shell [ -n "${VIRTUAL_ENV}" ] || echo pdm run) duty

args = $(foreach a,$($(subst -,_,$1)_args),$(if $(value $a),$a="$($a)"))
check_quality_args = files
docs_serve_args = host port
release_args = version
test_args = match

BASIC_DUTIES = \
	changelog \
	check-dependencies \
	clean \
	coverage \
	docs \
	docs-deploy \
	docs-regen \
	docs-serve \
	format \
	release

QUALITY_DUTIES = \
	check-quality \
	check-docs \
	check-types \
	test

.PHONY: help
help:
	@$(DUTY) --list

.PHONY: lock
lock:
	@pdm lock

.PHONY: setup
setup:
	@bash scripts/setup.sh

.PHONY: check
check:
	@bash scripts/multirun.sh duty check-quality check-types check-docs
	@$(DUTY) check-dependencies

.PHONY: $(BASIC_DUTIES)
$(BASIC_DUTIES):
	@$(DUTY) $@ $(call args,$@)

.PHONY: $(QUALITY_DUTIES)
$(QUALITY_DUTIES):
	@bash scripts/multirun.sh duty $@ $(call args,$@)

.PHONY: env-create
env-create:
	conda-merge ../crome-contracts/environment-contracts.yml ../crome-logic/environment-logic.yml ../crome-synthesis/environment-synthesis.yml environment-cgg.yml > environment.yml


.PHONY: env-install
env-install:
	conda env create --force -f environment.yml


.PHONY: env-activate
env-activate:
	conda activate crome-cgg

.PHONY: env-all
env-all: env-create env-install env-activate

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E r"(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove