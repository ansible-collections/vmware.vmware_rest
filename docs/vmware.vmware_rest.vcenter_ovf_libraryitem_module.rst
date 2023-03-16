.. _vmware.vmware_rest.vcenter_ovf_libraryitem_module:


******************************************
vmware.vmware_rest.vcenter_ovf_libraryitem
******************************************

**Creates a library item in content library from a virtual machine or virtual appliance**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a library item in content library from a virtual machine or virtual appliance. <p> This {@term operation} creates a library item in content library whose content is an OVF package derived from a source virtual machine or virtual appliance, using the supplied create specification. The OVF package may be stored as in a newly created library item or in an in an existing library item. For an existing library item whose content is updated by this {@term operation}, the original content is overwritten. Meta data such as name and description is not updated for the exisitng library item. </p>



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
                    <b>client_token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Client-generated token used to retry a request if the client fails to get a response from the server. If the original request succeeded, the result of that request will be returned, otherwise the operation will be retried.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>create_spec</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Information used to create the OVF package from the source virtual machine or virtual appliance. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Name to use in the OVF descriptor stored in the library item. ([&#x27;present&#x27;])</div>
                        <div>- <code>description</code> (str): Description to use in the OVF descriptor stored in the library item. ([&#x27;present&#x27;])</div>
                        <div>- <code>flags</code> (list): Flags to use for OVF package creation. The supported flags can be obtained using {@link ExportFlag#list}. ([&#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>deployment_spec</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specification of how the OVF package should be deployed to the target. Required with <em>state=[&#x27;deploy&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Name assigned to the deployed target virtual machine or virtual appliance. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>annotation</code> (str): Annotation assigned to the deployed target virtual machine or virtual appliance. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>accept_all_EULA</code> (bool): Whether to accept all End User License Agreements. ([&#x27;deploy&#x27;])</div>
                        <div>This key is required with [&#x27;deploy&#x27;].</div>
                        <div>- <code>network_mappings</code> (dict): Specification of the target network to use for sections of type ovf:NetworkSection in the OVF descriptor. The key in the {@term map} is the section identifier of the ovf:NetworkSection section in the OVF descriptor and the value is the target network to be used for deployment. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>storage_mappings</code> (dict): Specification of the target storage to use for sections of type vmw:StorageGroupSection in the OVF descriptor. The key in the {@term map} is the section identifier of the ovf:StorageGroupSection section in the OVF descriptor and the value is the target storage specification to be used for deployment. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>storage_provisioning</code> (str): The <code>disk_provisioning_type</code> defines the virtual disk provisioning types that can be set for a disk on the target platform. ([&#x27;deploy&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- eagerZeroedThick</div>
                        <div>- thick</div>
                        <div>- thin</div>
                        <div>- <code>storage_profile_id</code> (str): Default storage profile to use for all sections of type vmw:StorageSection in the OVF descriptor. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>locale</code> (str): The locale to use for parsing the OVF descriptor. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>flags</code> (list): Flags to be use for deployment. The supported flag values can be obtained using {@link ImportFlag#list}. ([&#x27;deploy&#x27;])</div>
                        <div>- <code>additional_parameters</code> (list): Additional OVF parameters that may be needed for the deployment. Additional OVF parameters may be required by the OVF descriptor of the OVF package in the library item. Examples of OVF parameters that can be specified through this field include, but are not limited to: &lt;ul&gt; &lt;li&gt;{@link DeploymentOptionParams}&lt;/li&gt; &lt;li&gt;{@link ExtraConfigParams}&lt;/li&gt; &lt;li&gt;{@link IpAllocationParams}&lt;/li&gt; &lt;li&gt;{@link PropertyParams}&lt;/li&gt; &lt;li&gt;{@link ScaleOutParams}&lt;/li&gt; &lt;li&gt;{@link VcenterExtensionParams}&lt;/li&gt; &lt;/ul&gt; ([&#x27;deploy&#x27;])</div>
                        <div>- <code>default_datastore_id</code> (str): Default datastore to use for all sections of type vmw:StorageSection in the OVF descriptor. ([&#x27;deploy&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ovf_library_item_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the content library item containing the OVF package to be deployed. Required with <em>state=[&#x27;deploy&#x27;, &#x27;filter&#x27;]</em></div>
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
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the virtual machine or virtual appliance to use as the source. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): Type of the deployable resource. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
                        <div>- <code>id</code> (str): Identifier of the deployable resource. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
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
                                    <li>filter</li>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Specification of the target content library and library item. This parameter is mandatory.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>library_id</code> (str): Identifier of the library in which a new library item should be created. This field is not used if the <code>#library_item_id</code> field is specified. ([&#x27;present&#x27;])</div>
                        <div>- <code>library_item_id</code> (str): Identifier of the library item that should be should be updated. ([&#x27;present&#x27;])</div>
                        <div>- <code>resource_pool_id</code> (str): Identifier of the resource pool to which the virtual machine or virtual appliance should be attached. ([&#x27;deploy&#x27;, &#x27;filter&#x27;])</div>
                        <div>This key is required with [&#x27;deploy&#x27;, &#x27;filter&#x27;].</div>
                        <div>- <code>host_id</code> (str): Identifier of the target host on which the virtual machine or virtual appliance will run. The target host must be a member of the cluster that contains the resource pool identified by {@link #resourcePoolId}. ([&#x27;deploy&#x27;, &#x27;filter&#x27;])</div>
                        <div>- <code>folder_id</code> (str): Identifier of the vCenter folder that should contain the virtual machine or virtual appliance. The folder must be virtual machine folder. ([&#x27;deploy&#x27;, &#x27;filter&#x27;])</div>
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
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        name: test_vm1
        guest_OS: RHEL_7_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
      register: my_vm

    - name: Create a content library pointing on a NFS share
      vmware.vmware_rest.content_locallibrary:
        name: my_library_on_nfs
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - storage_uri: nfs://datastore.test/srv/share/content-library
          type: OTHER
        state: present
      register: nfs_lib

    - name: Export the VM as an OVF on the library
      vmware.vmware_rest.vcenter_ovf_libraryitem:
        session_timeout: 2900
        source:
          type: VirtualMachine
          id: '{{ my_vm.id }}'
        target:
          library_id: '{{ nfs_lib.id }}'
        create_spec:
          name: golden_image
          description: an OVF example
          flags: []
        state: present
      register: ovf_item

    - name: Get the list of items of the NFS library
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ nfs_lib.id }}'
      register: lib_items

    - name: Create a new VM from the OVF
      vmware.vmware_rest.vcenter_ovf_libraryitem:
        ovf_library_item_id: '{{ (lib_items.value|selectattr("name", "equalto", "golden_image")|first).id }}'
        state: deploy
        target:
          resource_pool_id: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        deployment_spec:
          name: my_vm_from_ovf
          accept_all_EULA: true
          storage_provisioning: thin

    - name: Create a new VM from the OVF and specify the host and folder
      vmware.vmware_rest.vcenter_ovf_libraryitem:
        ovf_library_item_id: '{{ (lib_items.value|selectattr("name", "equalto", "golden_image")|first).id }}'
        state: deploy
        target:
          resource_pool_id: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
          folder_id: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          host_id: "{{ lookup('vmware.vmware_rest.host_moid', '/my_dc/host/my_cluster/esxi1.test/test_vm1') }}"
        deployment_spec:
          name: my_vm_from_ovf_on_a_host
          accept_all_EULA: true
          storage_provisioning: thin



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
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Create a new VM from the OVF and specify the host and folder</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;error&#x27;: {&#x27;errors&#x27;: [], &#x27;information&#x27;: [], &#x27;warnings&#x27;: []}, &#x27;resource_id&#x27;: {&#x27;id&#x27;: &#x27;vm-1078&#x27;, &#x27;type&#x27;: &#x27;VirtualMachine&#x27;}, &#x27;succeeded&#x27;: 1}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
