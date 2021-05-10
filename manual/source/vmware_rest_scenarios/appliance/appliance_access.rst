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

.. ansible-task::

  - name: Check if the Shell is enabled
    vmware.vmware_rest.appliance_access_shell_info:
    register: result
