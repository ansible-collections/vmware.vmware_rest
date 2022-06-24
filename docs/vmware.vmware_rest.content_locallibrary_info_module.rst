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

    - name: Build a list of local libraries
      vmware.vmware_rest.content_locallibrary_info:
      register: result
      retries: 100
      delay: 3
      until: result is not failed

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
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore')\
            \ }}"
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:23.573Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;53a679e5-a7dc-4d50-ad6e-759f697b6143&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:23.573Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_3&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/53a679e5-a7dc-4d50-ad6e-759f697b6143/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:24.545Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;b8380086-243a-400d-9a9f-8259f83d0148&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:24.545Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_4&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/b8380086-243a-400d-9a9f-8259f83d0148/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:25.464Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;1bad9ede-140b-4c62-bc6b-df506eb27292&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:25.464Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_5&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/1bad9ede-140b-4c62-bc6b-df506eb27292/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:26.405Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;a2d5c986-e376-4648-95f1-661efff3f851&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:26.405Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_6&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/a2d5c986-e376-4648-95f1-661efff3f851/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:27.357Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;45f33229-1232-4d7d-9cb3-69d7888bbb07&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:27.357Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_7&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/45f33229-1232-4d7d-9cb3-69d7888bbb07/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:28.377Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;8723c432-c706-4dfb-9f56-dadd3b95f299&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:28.377Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_8&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/8723c432-c706-4dfb-9f56-dadd3b95f299/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:29.397Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;bae6e392-12e7-4868-b18f-f487307bf752&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:29.397Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_9&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/bae6e392-12e7-4868-b18f-f487307bf752/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:30.412Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;61ea41a8-9443-4a64-9181-f9a046012197&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:30.412Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_10&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/61ea41a8-9443-4a64-9181-f9a046012197/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:19.438Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;c9b8f7da-d5ac-4076-86b9-39ee107d7da3&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:19.438Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/c9b8f7da-d5ac-4076-86b9-39ee107d7da3/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:20.801Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;99517bfa-7f2c-4e01-83e5-ed1bbb13c3e6&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:20.801Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_0&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/99517bfa-7f2c-4e01-83e5-ed1bbb13c3e6/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:21.697Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;0926be51-049a-476b-8537-e4b3d0a572a9&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:21.697Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_1&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/0926be51-049a-476b-8537-e4b3d0a572a9/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}, {&#x27;creation_time&#x27;: &#x27;2022-06-23T22:35:22.620Z&#x27;, &#x27;description&#x27;: &#x27;automated&#x27;, &#x27;id&#x27;: &#x27;7c970cd1-1526-4903-8295-64e28ecc6bad&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-06-23T22:35:22.620Z&#x27;, &#x27;name&#x27;: &#x27;my_library_on_nfs_2&#x27;, &#x27;publish_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;persist_json_enabled&#x27;: 0, &#x27;publish_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/7c970cd1-1526-4903-8295-64e28ecc6bad/lib.json&#x27;, &#x27;published&#x27;: 1, &#x27;user_name&#x27;: &#x27;vcsp&#x27;}, &#x27;server_guid&#x27;: &#x27;b138c531-cd80-43f5-842d-657d9ddc98f8&#x27;, &#x27;storage_backings&#x27;: [{&#x27;storage_uri&#x27;: &#x27;nfs://datastore.test/srv/share/content-library&#x27;, &#x27;type&#x27;: &#x27;OTHER&#x27;}], &#x27;type&#x27;: &#x27;LOCAL&#x27;, &#x27;version&#x27;: &#x27;2&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
