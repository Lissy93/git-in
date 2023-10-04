.PHONY: all install_lib_requirements insert_contributor_content copy_resources_to_site insert_resource_list install_web_dependencies build_web start_web

PYTHON := $(shell which python3 2>/dev/null || which python)

# Targets for lib/
install_lib_requirements:
	$(PYTHON) -m pip install -r lib/requirements.txt

insert_contributor_content:
	$(PYTHON) lib/insert_contributor_content.py

copy_resources_to_site:
	$(PYTHON) lib/copy_resources_to_site.py

insert_resource_list:
	$(PYTHON) lib/insert_resource_list.py

validate_pr:
	$(PYTHON) lib/validate_pr.py

# Targets for web/
install_web_dependencies:
	cd web && npm install

build_web:
	cd web && npm run build

start_web:
	cd web && npm run start
