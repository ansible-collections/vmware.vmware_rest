.. _vmware_rest_appliance_services:

******************
Services managment
******************

Handle your VCSA services with Ansible
======================================

You can use Ansible to control the VCSA services. To get a view of all the known services, you can use the appliance_services_info module:

.. ansible-task::

  - name: List all the services
    vmware.vmware_rest.appliance_services_info:

If you need to target a specific service, you can pass its name through the ``service`` parameter.
    
.. ansible-task::

  - name: Get information about ntpd
    vmware.vmware_rest.appliance_services_info:
      service: ntpd


Use the appliance_services module to stop a service:
      
.. ansible-tasks::

   - name: Stop the ntpd service
     vmware.vmware_rest.appliance_services:
       service: ntpd
       state: stop

or to start a service:
       
.. ansible-task::

    - name: Start the ntpd service
      vmware.vmware_rest.appliance_services:
        service: ntpd
        state: start


VMON services
=============

The VMON services can also be managed from Ansible. For instance to get the state of the ``vpxd`` service:
        
.. ansible-task::

    - name: Get information about a VMON service
      vmware.vmware_rest.appliance_vmon_service_info:
        service: vpxd

And to ensure it starts ``automatically``:
        
.. ansible-task::
 
    - name: Adjust vpxd configuration
      vmware.vmware_rest.appliance_vmon_service:
        service: vpxd
        startup_type: AUTOMATIC
