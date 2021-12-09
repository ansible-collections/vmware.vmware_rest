.. _ansible_collections.vmware.vmware_rest.docsite.vmware-rest-vm-tool-information:


How to get information from a running virtual machine
*****************************************************

*  Introduction

*  Scenario requirements

*  How to collect information

   *  Filesystem

   *  Guest identity

   *  Network

   *  Network interfaces

   *  Network routes


Introduction
============

This section shows you how to collection information from a running
virtual machine.


Scenario requirements
=====================

You"ve already followed vmware_rest_run_a_vm and your virtual machine
runs VMware Tools.


How to collect information
==========================

In this example, we use the ``vcenter_vm_guest_*`` module to collect
information about the associated resources.


Filesystem
----------

Here we use ``vcenter_vm_guest_localfilesystem_info`` to retrieve the
details about the filesystem of the guest. In this example we also use
a ``retries`` loop. The VMware Tools may take a bit of time to start
and by doing so, we give the VM a bit more time.

::

   - name: Get guest filesystem information
     vmware.vmware_rest.vcenter_vm_guest_localfilesystem_info:
       vm: '{{ test_vm1_info.id }}'
     register: _result
     until:
     - _result is not failed
     retries: 60
     delay: 5

response

::

   {
       "attempts": 7,
       "changed": false,
       "value": {
           "/": {
               "capacity": 2515173376,
               "free_space": 766377984,
               "mappings": []
           }
       }
   }


Guest identity
--------------

You can use ``vcenter_vm_guest_identity_info`` to get details like the
OS family or the hostname of the running VM.

::

   - name: Get guest identity information
     vmware.vmware_rest.vcenter_vm_guest_identity_info:
       vm: '{{ test_vm1_info.id }}'
     register: _result

response

::

   {
       "changed": false,
       "value": {
           "family": "LINUX",
           "full_name": {
               "args": [],
               "default_message": "Red Hat Fedora (64-bit)",
               "id": "vmsg.guestos.fedora64Guest.label"
           },
           "host_name": "localhost.localdomain",
           "ip_address": "192.168.122.44",
           "name": "FEDORA_64"
       }
   }


Network
-------

``vcenter_vm_guest_networking_info`` will return the OS network
configuration.

::

   - name: Get guest networking information
     vmware.vmware_rest.vcenter_vm_guest_networking_info:
       vm: '{{ test_vm1_info.id }}'
     register: _result

response

::

   {
       "changed": false,
       "value": {
           "dns": {
               "ip_addresses": [
                   "192.168.122.1"
               ],
               "search_domains": [
                   "localdomain"
               ]
           },
           "dns_values": {
               "domain_name": "localdomain",
               "host_name": "localhost.localdomain"
           }
       }
   }


Network interfaces
------------------

``vcenter_vm_guest_networking_interfaces_info`` will return a list of
NIC configurations.

See also vmware_rest_attach_a_network.

::

   - name: Get guest network interfaces information
     vmware.vmware_rest.vcenter_vm_guest_networking_interfaces_info:
       vm: '{{ test_vm1_info.id }}'
     register: _result

response

::

   {
       "changed": false,
       "value": [
           {
               "ip": {
                   "ip_addresses": [
                       {
                           "ip_address": "192.168.122.44",
                           "prefix_length": 24,
                           "state": "PREFERRED"
                       },
                       {
                           "ip_address": "fe80::5614:c95d:b044:ae15",
                           "prefix_length": 64,
                           "state": "UNKNOWN"
                       }
                   ]
               },
               "mac_address": "00:50:56:b1:6c:f3",
               "nic": "4000"
           }
       ]
   }


Network routes
--------------

Use ``vcenter_vm_guest_networking_routes_info`` to explore the route
table of your vitual machine.

::

   - name: Get guest network routes information
     vmware.vmware_rest.vcenter_vm_guest_networking_routes_info:
       vm: '{{ test_vm1_info.id }}'
     register: _result

response

::

   {
       "changed": false,
       "value": [
           {
               "gateway_address": "192.168.122.1",
               "interface_index": 0,
               "network": "0.0.0.0",
               "prefix_length": 0
           },
           {
               "interface_index": 0,
               "network": "192.168.122.0",
               "prefix_length": 24
           },
           {
               "interface_index": 0,
               "network": "fe80::",
               "prefix_length": 64
           },
           {
               "interface_index": 0,
               "network": "fe80::5614:c95d:b044:ae15",
               "prefix_length": 128
           },
           {
               "interface_index": 0,
               "network": "ff00::",
               "prefix_length": 8
           }
       ]
   }
