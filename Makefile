SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run doc8 -q docs
	poetry run black crome_logic examples
	poetry run pyupgrade
	poetry run pycln crome_logic --all
	poetry run autoflake .
	poetry run isort .
	poetry run autopep8 --in-place -r crome_logic examples
	poetry run docformatter --in-place -r crome_logic examples
	poetry run yapf -ir .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: flake
flake:
	poetry run flake8 crome_logic

.PHONY: mypy
mypy:
	poetry run mypy .

.PHONY: unit
unit:
	poetry run pytest

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit



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
