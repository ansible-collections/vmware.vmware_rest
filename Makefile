# Optional extra args for ansible-test (leave unset for full suite)
SANITY_TARGETS ?=
INTEGRATION_TARGETS ?=
UNIT_TARGETS ?=

UNIT_PYTHON_VERSION ?= 3.12

GALAXY_YML ?= $(CURDIR)/galaxy.yml
COLLECTION_ROOT = ~/.ansible/collections/ansible_collections/vmware/vmware_rest

# Emit --exclude flags for build_ignore directories that exist (ansible-test errors on missing paths).
# $(1) = path to galaxy.yml; run from COLLECTION_ROOT so -d checks the install tree.
define sanity_build_ignore_excludes
sed -n '/^build_ignore:/,$$p' "$(1)" | sed '1d' | sed -n 's/^[[:space:]]*-[[:space:]]*//p' | while IFS= read -r path; do \
		if [ -d "$$path" ]; then printf ' --exclude %s' "$$path"; fi; \
done
endef

# setup commands
.PHONY: upgrade-collections
upgrade-collections:
	ansible-galaxy collection install --upgrade -p ~/.ansible/collections .

.PHONY: install-collection-python-reqs
install-collection-python-reqs:
	pip install -r requirements.txt

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

.PHONY: integration
integration: upgrade-collections
		ansible-galaxy collection install -r tests/integration/requirements.yml; \
		cd $(COLLECTION_ROOT); \
		ansible --version; \
		ansible-test --version; \
		ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_ROOT)/../.. ansible-galaxy collection list; \
		ANSIBLE_ROLES_PATH=$(COLLECTION_ROOT)/tests/integration/targets \
				ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_ROOT)/../.. \
				ansible-test integration $(INTEGRATION_TARGETS) $(CLI_ARGS);

.PHONY: sanity
sanity: upgrade-collections
		cd $(COLLECTION_ROOT); \
		SANITY_EXCLUDES=$$($(call sanity_build_ignore_excludes,$(GALAXY_YML))); \
		ansible-test sanity -v --color --coverage --junit \
				--docker default $$SANITY_EXCLUDES $(SANITY_TARGETS)
