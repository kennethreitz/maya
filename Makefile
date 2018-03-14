.PHONY: tests docs

tests:
	pytest tests/
docs:
	cd docs && make html
