PROJECT := earthkit-climate
COV_REPORT := html

default: qa unit-tests
qa:
	pre-commit run --all-files

unit-tests:
	python -m pytest -vv --cov=. --cov-report=$(COV_REPORT) --doctest-glob="*.md" --doctest-glob="*.rst"

type-check:
	python -m mypy . --no-namespace-packages

template-update:
	pre-commit run --all-files cruft -c .pre-commit-config-cruft.yaml

docs-build:
	cd docs && rm -fr _api && make clean && make html

# DO NOT EDIT ABOVE THIS LINE, ADD COMMANDS BELOW
