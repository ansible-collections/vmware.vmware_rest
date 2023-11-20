.. _vmware.vmware_rest.vcenter_vmtemplate_libraryitems_module:


**************************************************
vmware.vmware_rest.vcenter_vmtemplate_libraryitems
**************************************************

**Creates a library item in content library from a virtual machine**


Version added: 2.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a library item in content library from a virtual machine. This {@term operation} creates a library item in content library whose content is a virtual machine template created from the source virtual machine, using the supplied create specification. The virtual machine template is stored in a newly created library item.



Requirements
------------
The below requirements are needed on the host that executes this module.

- vSphere 7.0.2 or greater
- python >= 3.6
- aiohttp


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Description of the deployed virtual machine.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disk_storage</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Storage specification for the virtual machine template&#x27;s disks.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>datastore</code> (str): Identifier for the datastore associated the deployed virtual machine&#x27;s disk. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- <code>storage_policy</code> (dict): Storage policy for the deployed virtual machine&#x27;s disk. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): Policy type for a virtual machine template&#x27;s disk.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>USE_SPECIFIED_POLICY</code></div>
                        <div>- policy (string): Identifier for the storage policy to use.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disk_storage_overrides</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Storage specification for individual disks in the deployed virtual machine. This is specified as a mapping between disk identifiers in the source virtual machine template contained in the library item and their storage specifications.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>guest_customization</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Guest customization spec to apply to the deployed virtual machine.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Name of the customization specification. ([&#x27;deploy&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hardware_customization</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Hardware customization spec which specifies updates to the deployed virtual machine.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>nics</code> (dict): Map of Ethernet network adapters to update. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>disks_to_remove</code> (list): Idenfiers of disks to remove from the deployed virtual machine. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>disks_to_update</code> (dict): Disk update specification for individual disks in the deployed virtual machine. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>cpu_update</code> (dict): CPU update specification for the deployed virtual machine. ([&#x27;deploy&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- num_cpus (integer): Number of virtual processors in the deployed virtual machine.</div>
                        <div>- num_cores_per_socket (integer): Number of cores among which to distribute CPUs in the deployed virtual machine.</div>
                        <div>- <code>memory_update</code> (dict): Memory update specification for the deployed virtual machine. ([&#x27;deploy&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- memory (integer): Size of a virtual machine&#x27;s memory in MB.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>library</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the library in which the new library item should be created. Required with <em>state=[&#x27;present&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the deployed virtual machine. This parameter is mandatory.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>placement</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Information used to place the virtual machine template.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>folder</code> (str): Virtual machine folder into which the deployed virtual machine should be placed. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- <code>resource_pool</code> (str): Resource pool into which the deployed virtual machine should be placed. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- <code>host</code> (str): Host onto which the virtual machine should be placed. If <code>#host</code> and <code>#resource_pool</code> are both specified, <code>#resource_pool</code> must belong to <code>#host</code>. If <code>#host</code> and <code>#cluster</code> are both specified, <code>#host</code> must be a member of <code>#cluster</code>. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- <code>cluster</code> (str): Cluster onto which the deployed virtual machine should be placed. If <code>#cluster</code> and <code>#resource_pool</code> are both specified, <code>#resource_pool</code> must belong to <code>#cluster</code>. If <code>#cluster</code> and <code>#host</code> are both specified, <code>#host</code> must be a member of <code>#cluster</code>. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>powered_on</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Specifies whether the deployed virtual machine should be powered on after deployment.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>session_timeout</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">float</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.1.0</div>
                </td>
                <td>
                </td>
                <td>
                        <div>Timeout settings for client session.</div>
                        <div>The maximal number of seconds for the whole operation including connection establishment, request sending and response.</div>
                        <div>The default value is 300s.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_vm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the source virtual machine to create the library item from. Required with <em>state=[&#x27;present&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>deploy</li>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>template_library_item</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>identifier of the content library item containing the source virtual machine template to be deployed. Required with <em>state=[&#x27;deploy&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_hostname</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The hostname or IP address of the vSphere vCenter</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_HOST</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The vSphere vCenter password</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_PASSWORD</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_rest_log_file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>You can use this optional parameter to set the location of a log file.</div>
                        <div>This file will be used to record the HTTP REST interaction.</div>
                        <div>The file will be stored on the host that run the module.</div>
                        <div>If the value is not specified in the task, the value of</div>
                        <div>environment variable <code>VMWARE_REST_LOG_FILE</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_username</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The vSphere vCenter username</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_USER</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vcenter_validate_certs</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>Allows connection when SSL certificates are not valid. Set to <code>false</code> when certificates are not trusted.</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_VALIDATE_CERTS</code> will be used instead.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vm_home_storage</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Storage location for the virtual machine template&#x27;s configuration and log files.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>datastore</code> (str): Identifier of the datastore for the deployed virtual machine&#x27;s configuration and log files. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- <code>storage_policy</code> (dict): Storage policy for the deployed virtual machine&#x27;s configuration and log files. ([&#x27;deploy&#x27;, &#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): Policy type for the virtual machine template&#x27;s configuration and log files.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>USE_SPECIFIED_POLICY</code></div>
                        <div>- policy (string): Identifier for the storage policy to use.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.2



Examples
--------

.. code-block:: yaml

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        name: test_vm1
        guest_OS: RHEL_7_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
        disks:
        - type: SATA
          backing:
            type: VMDK_FILE
            vmdk_file: '[local] test_vm1/{{ disk_name }}.vmdk'
        - type: SATA
          new_vmdk:
            name: second_disk
            capacity: 32000000000
        cdroms:
        - type: SATA
          sata:
            bus: 0
            unit: 2
        nics:
        - backing:
            type: STANDARD_PORTGROUP
            network: "{{ lookup('vmware.vmware_rest.network_moid', '/my_dc/network/VM Network') }}"
      register: my_vm

    - name: Create a content library based on a DataStore
      vmware.vmware_rest.content_locallibrary:
        name: my_library_on_datastore
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          type: DATASTORE
        state: present
      register: nfs_lib

    - name: Create a VM template on the library
      vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
        name: golden-template
        library: '{{ nfs_lib.id }}'
        source_vm: '{{ my_vm.id }}'
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
      register: mylib_item

    - name: Get the list of items of the NFS library
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ nfs_lib.id }}'
      register: lib_items

    - name: Use the name to identify the item
      set_fact:
        my_template_item: "{{ lib_items.value | selectattr('name', 'equalto', 'golden-template')|first }}"

    - name: Deploy a new VM based on the template
      vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
        name: vm-from-template
        library: '{{ nfs_lib.id }}'
        template_library_item: '{{ my_template_item.id }}'
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        state: deploy
      register: my_new_vm



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>moid of the resource</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">9c6df1f5-faba-490c-a8e6-edb72f787ab8</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Create a VM template on the library</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;cpu&#x27;: {&#x27;cores_per_socket&#x27;: 1, &#x27;count&#x27;: 1}, &#x27;disks&#x27;: {&#x27;16000&#x27;: {&#x27;capacity&#x27;: 16106127360, &#x27;disk_storage&#x27;: {&#x27;datastore&#x27;: &#x27;datastore-1122&#x27;}}, &#x27;16001&#x27;: {&#x27;capacity&#x27;: 32000000000, &#x27;disk_storage&#x27;: {&#x27;datastore&#x27;: &#x27;datastore-1122&#x27;}}}, &#x27;guest_OS&#x27;: &#x27;RHEL_7_64&#x27;, &#x27;memory&#x27;: {&#x27;size_MiB&#x27;: 1024}, &#x27;nics&#x27;: {&#x27;4000&#x27;: {&#x27;backing_type&#x27;: &#x27;STANDARD_PORTGROUP&#x27;, &#x27;mac_type&#x27;: &#x27;ASSIGNED&#x27;, &#x27;network&#x27;: &#x27;network-1123&#x27;}}, &#x27;vm_home_storage&#x27;: {&#x27;datastore&#x27;: &#x27;datastore-1122&#x27;}, &#x27;vm_template&#x27;: &#x27;vm-1132&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
