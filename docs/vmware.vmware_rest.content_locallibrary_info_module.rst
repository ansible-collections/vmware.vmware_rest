.. _vmware.vmware_rest.content_locallibrary_info_module:


********************************************
vmware.vmware_rest.content_locallibrary_info
********************************************

**Returns a given local library.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Returns a given local library.



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
                        <div>Identifier of the local library to return. Required with <em>state=[&#x27;get&#x27;]</em></div>
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

    - name: List Local Content Library
      vmware.vmware_rest.content_locallibrary_info:
      register: my_content_library

    - name: List all Local Content Library
      vmware.vmware_rest.content_locallibrary_info:
      register: all_content_libraries

    - name: Create a new local content library
      vmware.vmware_rest.content_locallibrary:
        name: local_library_001
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore') }}"
          type: DATASTORE
        state: present
      register: ds_lib

    - name: Retrieve the local content library information based upon id check mode
      vmware.vmware_rest.content_locallibrary_info:
        library_id: '{{ ds_lib.id }}'
      register: result
      check_mode: true



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
                            <div>List all Local Content Library</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:22.940Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;a66d5c73-57f8-4a3a-9361-292a55f68516&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:22.940Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/a66d5c73-57f8-4a3a-9361-292a55f68516/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:25.134Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;3393956a-43ed-4e7f-bd96-eb39bd604445&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:25.134Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_0&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/3393956a-43ed-4e7f-bd96-eb39bd604445/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:26.342Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;87f66f86-c046-45a7-9563-d59ea220babf&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:26.342Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_1&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/87f66f86-c046-45a7-9563-d59ea220babf/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:27.504Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;f6c590c4-ae6d-4ad0-9362-378196e98a3c&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:27.504Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_2&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/f6c590c4-ae6d-4ad0-9362-378196e98a3c/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:28.821Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;e8917499-2a4c-4b70-b39b-ae0caaef89c3&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:28.821Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_3&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/e8917499-2a4c-4b70-b39b-ae0caaef89c3/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:30.085Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;630ebdfe-8913-45d3-aaa8-9c2fdecbb76b&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:30.085Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_4&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/630ebdfe-8913-45d3-aaa8-9c2fdecbb76b/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:31.482Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;a046e2e5-bd55-4d04-9443-750a2ab35a6d&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:31.482Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_5&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/a046e2e5-bd55-4d04-9443-750a2ab35a6d/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:32.846Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;b94383b1-7877-4dbd-8c33-51abc39451ff&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:32.846Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_6&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/b94383b1-7877-4dbd-8c33-51abc39451ff/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:34.218Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;8e3efb68-cb84-4ce0-a65a-6c94cc6e6e00&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:34.218Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_7&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/8e3efb68-cb84-4ce0-a65a-6c94cc6e6e00/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:35.922Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;0b12c0b3-6c6d-448d-9033-e054a70183e7&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:35.922Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_8&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/0b12c0b3-6c6d-448d-9033-e054a70183e7/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:37.796Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;46454797-bbe0-415a-9fe9-3cf2f74a14db&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:37.796Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_9&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/46454797-bbe0-415a-9fe9-3cf2f74a14db/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:02:38.976Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;209926aa-e3fe-46a5-95f2-501e82a5139b&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:02:38.976Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_10&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/209926aa-e3fe-46a5-95f2-501e82a5139b/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
