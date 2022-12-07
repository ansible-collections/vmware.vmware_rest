#!/usr/bin/env bash
source ../init.sh

# NOTE, the two steps a in two different isolated playbooks for the
# Downstream-EE testing. The prepare.yaml depends on community.vmware
# which is not part of Downstream-EE.
# This allow use to run the first stage with a regular ansible, and
# the second part from within a Downstream-EE container.
ansible-playbook prepare.yml
exec ansible-playbook run.yml
