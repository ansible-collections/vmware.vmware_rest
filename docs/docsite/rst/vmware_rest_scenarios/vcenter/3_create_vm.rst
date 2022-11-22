.. _ansible_collections.vmware.vmware_rest.docsite.vmware-rest-create-vm:


How to create a Virtual Machine
*******************************

*  Introduction

*  Scenario requirements

*  How to create a virtual machine


Introduction
============

This section shows you how to use Ansible to create a virtual machine.


Scenario requirements
=====================

You"ve already followed vmware_rest_collect_info and you"ve got the
following variables defined:

*  ``my_cluster_info``

*  ``my_datastore``

*  ``my_virtual_machine_folder``

*  ``my_cluster_info``


How to create a virtual machine
===============================

In this example, we will use the ``vcenter_vm`` module to create a new
guest.

::

   - name: Create a VM
     vmware.vmware_rest.vcenter_vm:
       placement:
         cluster: "{{ my_cluster_info.id }}"
         datastore: "{{ my_datastore.datastore }}"
         folder: "{{ my_virtual_machine_folder.folder }}"
         resource_pool: "{{ my_cluster_info.value.resource_pool }}"
       name: test_vm1
       guest_OS: DEBIAN_8_64
       hardware_version: VMX_11
       memory:
         hot_add_enabled: true
         size_MiB: 1024
     register: _result

response

::

   {
       "changed": true,
       "id": "vm-1184",
       "value": {
           "boot": {
               "delay": 0,
               "enter_setup_mode": false,
               "retry": false,
               "retry_delay": 10000,
               "type": "BIOS"
           },
           "boot_devices": [],
           "cdroms": {},
           "cpu": {
               "cores_per_socket": 1,
               "count": 1,
               "hot_add_enabled": false,
               "hot_remove_enabled": false
           },
           "disks": {
               "2000": {
                   "backing": {
                       "type": "VMDK_FILE",
                       "vmdk_file": "[rw_datastore] test_vm1/test_vm1.vmdk"
                   },
                   "capacity": 17179869184,
                   "label": "Hard disk 1",
                   "scsi": {
                       "bus": 0,
                       "unit": 0
                   },
                   "type": "SCSI"
               }
           },
           "floppies": {},
           "guest_OS": "DEBIAN_8_64",
           "hardware": {
               "upgrade_policy": "NEVER",
               "upgrade_status": "NONE",
               "version": "VMX_11"
           },
           "identity": {
               "bios_uuid": "423123c1-253c-9785-5925-16de430abbe5",
               "instance_uuid": "50310cfd-c581-0f13-d0ed-9811073d02d7",
               "name": "test_vm1"
           },
           "instant_clone_frozen": false,
           "memory": {
               "hot_add_enabled": true,
               "size_MiB": 1024
           },
           "name": "test_vm1",
           "nics": {},
           "nvme_adapters": {},
           "parallel_ports": {},
           "power_state": "POWERED_OFF",
           "sata_adapters": {},
           "scsi_adapters": {
               "1000": {
                   "label": "SCSI controller 0",
                   "scsi": {
                       "bus": 0,
                       "unit": 7
                   },
                   "sharing": "NONE",
                   "type": "PVSCSI"
               }
           },
           "serial_ports": {}
       }
   }

Note: ``vcenter_vm`` accepts more parameters, however you may prefer to
   start with a simple VM and use the ``vcenter_vm_hardware`` modules
   to tune it up afterwards. It"s easier this way to identify a
   potential problematical step.
