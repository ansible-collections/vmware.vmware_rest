#!/usr/bin/env bash
# shellcheck disable=SC2155,SC2086

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"  # No Color
BASE_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")
TEST_OUTPUT_LOG="/tmp/vmware_vmware_rest_tests_report.txt"

if [ -f "$TEST_OUTPUT_LOG" ]; then
    rm -f "$TEST_OUTPUT_LOG"
fi

# Generates a string starting with 'test-' followed by 4 random lowercase characters
tiny_prefix="test-vmware-rest-$(uuidgen | tr -d '-' | cut -c1-4 | tr '[:upper:]' '[:lower:]')"
if grep -qa 'tiny_prefix' "${BASE_DIR}/integration_config.yml"; then
    sed -i "s|tiny_prefix:.*|tiny_prefix: $tiny_prefix|" "${BASE_DIR}/integration_config.yml"
else
    echo "tiny_prefix: $tiny_prefix" >> "${BASE_DIR}/integration_config.yml"
fi

echo ""
echo ""
echo "******   Starting Eco vCenter tests   ******"
grep 'tiny_prefix' ${BASE_DIR}/integration_config.yml
grep 'vcenter_hostname' ${BASE_DIR}/integration_config.yml
echo ""
echo ""

failed=0
total=0
{
    echo "==============="
    echo "Tests Summary"
    echo "==============="
} >> "$TEST_OUTPUT_LOG"

for target in $(ansible-test integration --list-target | grep 'vmware_'); do
    echo "Running integration test for $target"
    total=$((total + 1))
    if ansible-test integration $target --skip-tags force-simulator-run; then
        echo -e "Test: $target ${GREEN}Passed${NC}" | tee -a "$TEST_OUTPUT_LOG"
    else
        echo -e "Test: $target ${RED}Failed${NC}" | tee -a "$TEST_OUTPUT_LOG"
        failed=$((failed + 1))
    fi
done
echo "$failed test(s) failed out of $total." >> "$TEST_OUTPUT_LOG"
cat "$TEST_OUTPUT_LOG"
if [ $failed -gt 0 ]; then
    exit 1
fi
