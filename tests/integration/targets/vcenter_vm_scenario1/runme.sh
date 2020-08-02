#!/usr/bin/env bash
set -eu
source ../init.sh
set -eux

exec ansible-playbook -i ../inventory.networking playbook.yaml
