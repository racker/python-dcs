test:
	python -m unittest discover

tests: test

coverage:
	python tests/testutils.py
	@echo ""
	@echo "Coverage results in coverage_html_report"
tests: test

.PHONY: test tests coverage

