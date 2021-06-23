.. _vmware.vmware_rest.content_library_item_info_module:


********************************************
vmware.vmware_rest.content_library_item_info
********************************************

**Returns the {@link ItemModel} with the given identifier.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Returns the {@link ItemModel} with the given identifier.



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
                    <b>library_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the library whose items should be returned. Required with <em>state=[&#x27;list&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>library_item_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the library item to return. Required with <em>state=[&#x27;get&#x27;]</em></div>
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




Examples
--------

.. code-block:: yaml

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

    - name: Get the list of items of the NFS library
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ nfs_lib.id }}'
      register: result

    - name: We can also use filter to limit the number of result
      vmware.vmware_rest.vcenter_datastore_info:
        filter_names:
        - rw_datastore
      register: my_datastores

    - name: Set my_datastore
      set_fact:
        my_datastore: '{{ my_datastores.value|first }}'

    - name: Create a new local content library
      vmware.vmware_rest.content_locallibrary:
        name: local_library_001
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - datastore_id: '{{ my_datastore.datastore }}'
          type: DATASTORE
        state: present
      register: ds_lib

    - name: Get the (empty) list of items of the library
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ ds_lib.id }}'
      register: result

    - name: Create subscribed library
      content_subscribedlibrary:
        name: sub_lib
        subscription_info:
          subscription_url: '{{ nfs_lib.value.publish_info.publish_url }}'
          authentication_method: NONE
          automatic_sync_enabled: false
          on_demand: true
        storage_backings:
        - datastore_id: '{{ my_datastore.datastore }}'
          type: DATASTORE
      register: sub_lib

    - name: Ensure the OVF is here
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ sub_lib.id }}'
      register: result



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
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Ensure the OVF is here</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;cached&#x27;: 0, &#x27;content_version&#x27;: &#x27;2&#x27;, &#x27;creation_time&#x27;: &#x27;2021-06-23T23:32:56.088Z&#x27;, &#x27;description&#x27;: &#x27;an OVF example&#x27;, &#x27;id&#x27;: &#x27;9f8398fd-b4c4-4bb4-afe5-8302dcdc4a2b&#x27;, &#x27;last_modified_time&#x27;: &#x27;2021-06-23T23:32:56.552Z&#x27;, &#x27;last_sync_time&#x27;: &#x27;2021-06-23T23:32:56.551Z&#x27;, &#x27;library_id&#x27;: &#x27;899184df-f3ab-4284-ac9b-02407fd9536e&#x27;, &#x27;metadata_version&#x27;: &#x27;1&#x27;, &#x27;name&#x27;: &#x27;my_vm&#x27;, &#x27;size&#x27;: 0, &#x27;source_id&#x27;: &#x27;2d564ff7-4b74-41d6-961a-7f892bb11fdb&#x27;, &#x27;type&#x27;: &#x27;ovf&#x27;, &#x27;version&#x27;: &#x27;1&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
