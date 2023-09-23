.PHONY: all install_requirements insert_contributor_content

PYTHON := $(shell which python3 2>/dev/null || which python)

install_requirements:
	$(PYTHON) -m pip install -r lib/requirements.txt

insert_contributor_content:
	$(PYTHON) lib/insert_contributor_content.py
