# Define ANSI escape codes for colors
GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m  # No Color

.PHONY: prepare_symlinks
prepare_symlinks:
	ansible-playbook tools/prepare_symlinks.yml

.PHONY: install-ansible-collections
install-ansible-collections:
	ansible-galaxy collection install --upgrade -r tests/integration/requirements.yml

.PHONY: install-python-packages
install-python-packages:
	pip3 install -r tests/integration/requirements.txt

.PHONY: remove_aliases
remove_aliases:
	@find tests/integration/targets/ -name "aliases" -exec rm -f {} +

.PHONY: eco-vcenter-ci
eco-vcenter-ci: install-ansible-collections prepare_symlinks remove_aliases
	@[ -f /tmp/vmware_rest_tests_report.txt ] && rm /tmp/vmware_rest_tests_report.txt || true; \
	@failed=0; \
	total=0; \
	echo "===============" >> /tmp/vmware_rest_tests_report.txt; \
	echo "Tests Summary" >> /tmp/vmware_rest_tests_report.txt; \
	echo "===============" >> /tmp/vmware_rest_tests_report.txt; \
	for dir in $(shell ansible-test integration --list-target --no-temp-workdir | grep 'vmware_rest_'); do \
	  echo "Running integration test for $$dir"; \
	  total=$$((total + 1)); \
	  if ansible-test integration --no-temp-workdir $$dir; then \
	    echo -e "Test: $$dir ${GREEN}Passed${NC}" | tee -a /tmp/vmware_rest_tests_report.txt; \
	  else \
	    echo -e "Test: $$dir ${RED}Failed${NC}" | tee -a /tmp/vmware_rest_tests_report.txt; \
	    failed=$$((failed + 1)); \
	  fi; \
	done; \
	echo "$$failed test(s) failed out of $$total." >> /tmp/vmware_rest_tests_report.txt; \
	cat /tmp/vmware_rest_tests_report.txt; \
	if [ $$failed -gt 0 ]; then \
	  exit 1; \
	fi
