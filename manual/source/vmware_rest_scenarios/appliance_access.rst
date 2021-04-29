.. _vmware_rest_appliance_access:

************************************
Configure the console and SSH access
************************************

.. contents::
  :local:


Introduction
============

This section show you how to manage the console and SSH access of the vCenter Server Appliance (VCSA).

Scenario requirements
=====================

You've got an up and running vCenter Server Appliance.

Manage the Shell access
---------------------------------------------------

Detect if the Shell is enabled.

.. literalinclude:: task_outputs/Check_if_the_Shell_is_enabled.task.yaml

Result
______

.. literalinclude:: task_outputs/Check_if_the_Shell_is_enabled.result.json


Change the upgrade policy to UPGRADE_AT_POWER_CYCLE 
------------------------------------------------------------------------------------------

.. literalinclude:: task_outputs/Change_vm-tools_upgrade_policy_to_UPGRADE_AT_POWER_CYCLE.task.yaml

Result
______

.. literalinclude:: task_outputs/Change_vm-tools_upgrade_policy_to_UPGRADE_AT_POWER_CYCLE.result.json

