#!/usr/bin/env bash
set -eux
source ../init.sh
exec ansible-playbook playbook.yaml
