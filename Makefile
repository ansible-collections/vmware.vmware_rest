# Optional extra args for ansible-test (leave unset for full suite)
SANITY_TARGETS ?=
INTEGRATION_TARGETS ?=
UNIT_TARGETS ?=

UNIT_PYTHON_VERSION ?= 3.12

GALAXY_YML ?= $(CURDIR)/galaxy.yml
COLLECTION_ROOT = ~/.ansible/collections/ansible_collections/vmware/vmware_rest

# setup commands
.PHONY: upgrade-collections
upgrade-collections:
	ansible-galaxy collection install --upgrade -p ~/.ansible/collections .

.PHONY: install-collection-python-reqs
install-collection-python-reqs:
	pip install -r requirements.txt

.PHONY: install-integration-reqs
install-integration-reqs: install-collection-python-reqs
	pip install -r tests/integration/requirements.txt; \
	ansible-galaxy collection install --upgrade -p ~/.ansible/collections -r tests/integration/requirements.yml

tests/integration/integration_config.yml:
	chmod +x ./tests/integration/generate_integration_config.sh; \
	./tests/integration/generate_integration_config.sh

# test commands
.PHONY: linters
linters:  ## Run extra linter tests
	@pip install -r linters.requirements.txt; err=0; echo "\nStart tests.\n"; \
	black --check --diff --color . --extend-exclude ".agents/*" || err=1; \
	if [ "$$err" = 1 ]; then echo "\nAt least one linter failed\n" >&2; exit 1; fi

.PHONY: units
units: upgrade-collections
		cd $(COLLECTION_ROOT); \
		ansible-test units --docker --python $(UNIT_PYTHON_VERSION) --coverage $(UNIT_TARGETS); \
		ansible-test coverage combine --requirements --export tests/output/coverage/; \
		ansible-test coverage report --requirements --docker --omit 'tests/*' --show-missing;

.PHONY: units-coverage
units-coverage: units
		cd $(COLLECTION_ROOT); \
		ansible-test coverage xml --requirements; \
		cp tests/output/reports/coverage.xml $(CURDIR)/coverage-units.xml;

# Copy .agents and config to the collection root so they are available for sanity tests.
# This is a workaround to make the local tests match the CI tests.
.PHONY: sanity
sanity: upgrade-collections
		cp -r .agents $(COLLECTION_ROOT)/; \
		cp -r config $(COLLECTION_ROOT)/; \
		cd $(COLLECTION_ROOT); \
		ansible-test sanity -v --color --coverage --junit \
				--docker default; \

# Temporarily include a step to remove the eco-vcenter-ci targets
.PHONY: integration
integration: upgrade-collections
	ansible-galaxy collection install -r tests/integration/requirements.yml; \
	cd $(COLLECTION_ROOT); \
	rm -rf tests/integration/targets/vmware_rest_*;
	ansible --version; \
	ansible-test --version; \
	ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_ROOT)/../.. ansible-galaxy collection list; \
	ANSIBLE_ROLES_PATH=$(COLLECTION_ROOT)/tests/integration/targets \
		ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_ROOT)/../.. \
		ansible-test integration $(INTEGRATION_TARGETS) $(CLI_ARGS);

.PHONY: eco-vcenter-ci
eco-vcenter-ci: tests/integration/integration_config.yml install-integration-reqs upgrade-collections
	rm -rf ~/.ansible/collections/ansible_collections/cloud/common; \
	cd ~/.ansible/collections/ansible_collections/vmware/vmware_rest; \
	ansible --version; \
	ansible-test --version; \
	ANSIBLE_COLLECTIONS_PATH=~/.ansible/collections/ansible_collections ansible-galaxy collection list; \
	chmod +x tests/integration/run_eco_vcenter_ci.sh; \
	ANSIBLE_ROLES_PATH=~/.ansible/collections/ansible_collections/vmware/vmware_rest/tests/integration/targets \
		ANSIBLE_COLLECTIONS_PATH=~/.ansible/collections/ansible_collections \
		./tests/integration/run_eco_vcenter_ci.sh $(INTEGRATION_TARGETS)
