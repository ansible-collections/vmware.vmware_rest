.. _vmware.vmware_rest.content_subscribedlibrary_module:


********************************************
vmware.vmware_rest.content_subscribedlibrary
********************************************

**Creates a new subscribed library**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a new subscribed library. <p> Once created, the subscribed library will be empty. If the {@link LibraryModel#subscriptionInfo} property is set, the Content Library Service will attempt to synchronize to the remote source. This is an asynchronous operation so the content of the published library may not immediately appear.



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
                        <div>Unique token generated on the client for each creation request. The token should be a universally unique identifier (UUID), for example: <code>b8a2a2e3-2314-43cd-a871-6ede0f429751</code>. This token can be used to guarantee idempotent creation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>creation_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The date and time when this library was created.</div>
                </td>
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
                        <div>A human-readable description for this library.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>An identifier which uniquely identifies this <code>library_model</code>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>last_modified_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The date and time when this library was last updated. This field is updated automatically when the library properties are changed. This field is not affected by adding, removing, or modifying a library item or its content within the library. Tagging the library or syncing the subscribed library does not alter this field.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>last_sync_time</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The date and time when this library was last synchronized. This field applies only to subscribed libraries. It is updated every time a synchronization is triggered on the library. The value is not set for a local library.</div>
                </td>
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
                        <div>Identifier of the subscribed library whose content should be evicted. Required with <em>state=[&#x27;absent&#x27;, &#x27;evict&#x27;, &#x27;present&#x27;, &#x27;sync&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The name of the library. A Library is identified by a human-readable name. Library names cannot be undefined or an empty string. Names do not have to be unique.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>optimization_info</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Defines various optimizations and optimization parameters applied to this library.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>optimize_remote_publishing</code> (bool): If set to <code>True</code> then library would be optimized for remote publishing. Turn it on if remote publishing is dominant use case for this library. Remote publishing means here that publisher and subscribers are not the part of the same <code>vcenter</code> SSO domain. Any optimizations could be done as result of turning on this optimization during library creation. For example, library content could be stored in different format but optimizations are not limited to just storage format. Note, that value of this toggle could be set only during creation of the library and you would need to migrate your library in case you need to change this value (optimize the library for different use case). ([&#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>publish_info</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Defines how this library is published so that it can be subscribed to by a remote subscribed library. The <code>publish_info</code> defines where and how the metadata for this local library is accessible. A local library is only published publically if <code>publish_info.published</code> is <code>True</code>.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>authentication_method</code> (str): The <code>authentication_method</code> indicates how a subscribed library should authenticate to the published library endpoint. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- BASIC</div>
                        <div>- NONE</div>
                        <div>- <code>published</code> (bool): Whether the local library is published. ([&#x27;present&#x27;])</div>
                        <div>- <code>publish_url</code> (str): The URL to which the library metadata is published by the Content Library Service. This value can be used to set the <code>subscription_info.subscriptionurl</code> property when creating a subscribed library. ([&#x27;present&#x27;])</div>
                        <div>- <code>user_name</code> (str): The username to require for authentication. ([&#x27;present&#x27;])</div>
                        <div>- <code>password</code> (str): The new password to require for authentication. ([&#x27;present&#x27;])</div>
                        <div>- <code>current_password</code> (str): The current password to verify. This field is available starting in vSphere 6.7. ([&#x27;present&#x27;])</div>
                        <div>- <code>persist_json_enabled</code> (bool): Whether library and library item metadata are persisted in the storage backing as JSON files. This flag only applies if the local library is published. Enabling JSON persistence allows you to synchronize a subscribed library manually instead of over HTTP. You copy the local library content and metadata to another storage backing manually and then create a subscribed library referencing the location of the library JSON file in the <code>subscription_info.subscriptionurl</code>. When the subscribed library&#x27;s storage backing matches the subscription URL, files do not need to be copied to the subscribed library. For a library backed by a datastore, the library JSON file will be stored at the path contentlib-{library_id}/lib.json on the datastore. For a library backed by a remote file system, the library JSON file will be stored at {library_id}/lib.json in the remote file system path. ([&#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>server_guid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The unique identifier of the vCenter server where the library exists.</div>
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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>absent</li>
                                    <li>evict</li>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>probe</li>
                                    <li>sync</li>
                        </ul>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>storage_backings</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of default storage backings which are available for this library. A storage backing defines a default storage location which can be used to store files for library items in this library. Some library items, for instance, virtual machine template items, support files that may be distributed across various storage backings. One or more item files may or may not be located on the default storage backing. Multiple default storage locations are not currently supported but may become supported in future releases.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The <code>type</code> specifies the type of the storage backing. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- DATASTORE</div>
                        <div>- OTHER</div>
                        <div>- <code>datastore_id</code> (str): Identifier of the datastore used to store the content in the library. ([&#x27;present&#x27;])</div>
                        <div>- <code>storage_uri</code> (str): URI identifying the location used to store the content in the library. The following URI formats are supported: vSphere 6.5 &lt;ul&gt; &lt;li&gt;nfs://server/path?version=4 (for vCenter Server Appliance only) - Specifies an NFS Version 4 server.&lt;/li&gt; &lt;li&gt;nfs://server/path (for vCenter Server Appliance only) - Specifies an NFS Version 3 server. The nfs://server:/path format is also supported.&lt;/li&gt; &lt;li&gt;smb://server/path - Specifies an SMB server or Windows share.&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 Update 1 &lt;ul&gt; &lt;li&gt;nfs://server:/path (for vCenter Server Appliance only)&lt;/li&gt; &lt;li&gt;file://unc-server/path (for vCenter Server for Windows only)&lt;/li&gt; &lt;li&gt;file:///mount/point (for vCenter Server Appliance only) - Local file URIs are supported only when the path is a local mount point for an NFS file system. Use of file URIs is strongly discouraged. Instead, use an NFS URI to specify the remote file system.&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 &lt;ul&gt; &lt;li&gt;nfs://server:/path (for vCenter Server Appliance only)&lt;/li&gt; &lt;li&gt;file://unc-server/path (for vCenter Server for Windows only)&lt;/li&gt; &lt;li&gt;file:///path - Local file URIs are supported but strongly discouraged because it may interfere with the performance of vCenter Server.&lt;/li&gt; &lt;/ul&gt; ([&#x27;present&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>subscription_info</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Defines the subscription behavior for this Library. The <code>subscription_info</code> defines how this subscribed library synchronizes to a remote source. Setting the value will determine the remote source to which the library synchronizes, and how. Changing the subscription will result in synchronizing to a new source. If the new source differs from the old one, the old library items and data will be lost. Setting <code>subscription_info.automaticSyncEnabled</code> to false will halt subscription but will not remove existing cached data.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>authentication_method</code> (str): Indicate how the subscribed library should authenticate with the published library endpoint. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- BASIC</div>
                        <div>- NONE</div>
                        <div>- <code>automatic_sync_enabled</code> (bool): Whether the library should participate in automatic library synchronization. In order for automatic synchronization to happen, the global <code>configuration_model.automatic_sync_enabled</code> option must also be true. The subscription is still active even when automatic synchronization is turned off, but synchronization is only activated with an explicit call to <span class='module'>vmware.vmware_rest.content_subscribedlibrary</span> with <code>state=sync</code> or <span class='module'>vmware.vmware_rest.content_library_item</span> with <code>state=sync</code>. In other words, manual synchronization is still available even when automatic synchronization is disabled. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>on_demand</code> (bool): Indicates whether a library item&#x27;s content will be synchronized only on demand. If this is set to <code>True</code>, then the library item&#x27;s metadata will be synchronized but the item&#x27;s content (its files) will not be synchronized. The Content Library Service will synchronize the content upon request only. This can cause the first use of the content to have a noticeable delay. Items without synchronized content can be forcefully synchronized in advance using the <span class='module'>vmware.vmware_rest.content_library_item</span> with <code>state=sync</code> call with <code>force_sync_content</code> set to true. Once content has been synchronized, the content can removed with the <span class='module'>vmware.vmware_rest.content_library_item</span> with <code>state=sync</code> call. If this value is set to <code>False</code>, all content will be synchronized in advance. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>password</code> (str): The password to use when authenticating. The password must be set when using a password-based authentication method; empty strings are not allowed. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>ssl_thumbprint</code> (str): An optional SHA-1 hash of the SSL certificate for the remote endpoint. If this value is defined the SSL certificate will be verified by comparing it to the SSL thumbprint. The SSL certificate must verify against the thumbprint. When specified, the standard certificate chain validation behavior is not used. The certificate chain is validated normally if this value is not set. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>subscription_url</code> (str): The URL of the endpoint where the metadata for the remotely published library is being served. This URL can be the <code>publish_info.publish_url</code> of the published library (for example, https://server/path/lib.json). If the source content comes from a published library with <code>publish_info.persist_json_enabled</code>, the subscription URL can be a URL pointing to the library JSON file on a datastore or remote file system. The supported formats are: vSphere 6.5 &lt;ul&gt; &lt;li&gt;ds:///vmfs/volumes/{uuid}/mylibrary/lib.json (for datastore)&lt;/li&gt; &lt;li&gt;nfs://server/path/mylibrary/lib.json (for NFSv3 server on vCenter Server Appliance)&lt;/li&gt; &lt;li&gt;nfs://server/path/mylibrary/lib.json?version=4 (for NFSv4 server on vCenter Server Appliance) &lt;/li&gt; &lt;li&gt;smb://server/path/mylibrary/lib.json (for SMB server)&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 &lt;ul&gt; &lt;li&gt;file://server/mylibrary/lib.json (for UNC server on vCenter Server for Windows)&lt;/li&gt; &lt;li&gt;file:///path/mylibrary/lib.json (for local file system)&lt;/li&gt; &lt;/ul&gt; When you specify a DS subscription URL, the datastore must be on the same vCenter Server as the subscribed library. When you specify an NFS or SMB subscription URL, the <code>storage_backings.storage_uri</code> of the subscribed library must be on the same remote file server and should share a common parent path with the subscription URL. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>user_name</code> (str): The username to use when authenticating. The username must be set when using a password-based authentication method. Empty strings are allowed for usernames. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- <code>source_info</code> (dict): Information about the source published library. This field will be set for a subscribed library which is associated with a subscription of the published library. ([&#x27;present&#x27;, &#x27;probe&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- source_library (string): Identifier of the published library.</div>
                        <div>- subscription (string): Identifier of the subscription associated with the subscribed library.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>LOCAL</li>
                                    <li>SUBSCRIBED</li>
                        </ul>
                </td>
                <td>
                        <div>The <code>library_type</code> defines the type of a Library. The type of a library can be used to determine which additional services can be performed with a library.</div>
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
                    <b>version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A version number which is updated on metadata changes. This value allows clients to detect concurrent updates and prevent accidental clobbering of data. This value represents a number which is incremented every time library properties, such as name or description, are changed. It is not incremented by changes to a library item within the library, including adding or removing items. It is also not affected by tagging the library.</div>
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

    - name: Create subscribed library
      vmware.vmware_rest.content_subscribedlibrary:
        name: sub_lib
        subscription_info:
          subscription_url: '{{ nfs_lib.value.publish_info.publish_url }}'
          authentication_method: NONE
          automatic_sync_enabled: false
          on_demand: true
        storage_backings:
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore') }}"
          type: DATASTORE
      register: sub_lib

    - name: Create subscribed library (again)
      vmware.vmware_rest.content_subscribedlibrary:
        name: sub_lib
        subscription_info:
          subscription_url: '{{ nfs_lib.value.publish_info.publish_url }}'
          authentication_method: NONE
          automatic_sync_enabled: false
          on_demand: true
        storage_backings:
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore') }}"
          type: DATASTORE
      register: result

    - name: Clean up the cache
      vmware.vmware_rest.content_subscribedlibrary:
        name: sub_lib
        library_id: '{{ sub_lib.id }}'
        state: evict

    - name: Trigger a library sync
      vmware.vmware_rest.content_subscribedlibrary:
        name: sub_lib
        library_id: '{{ sub_lib.id }}'
        state: sync



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
                    <b>msg</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Delete all the subscribed libraries</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">All items completed</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>results</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Delete all the subscribed libraries</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;_ansible_item_label&#x27;: {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:06:05.189Z&#x27;, &#x27;description&#x27;: &#x27;&#x27;, &#x27;id&#x27;: &#x27;8b4e355e-a463-44f1-9b04-d0786a49cc7d&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:06:05.189Z&#x27;, &#x27;last_sync_time&#x27;: &#x27;2022-11-23T20:06:07.717Z&#x27;, &#x27;name&#x27;: &#x27;sub_lib&#x27;, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;datastore_id&#x27;: &#x27;datastore-1065&#x27;, &#x27;type&#x27;: &#x27;DATASTORE&#x27;}], &#x27;subscription_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;automatic_sync_enabled&#x27;: 0, &#x27;on_demand&#x27;: 1, &#x27;subscription_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/a66d5c73-57f8-4a3a-9361-292a55f68516/lib.json&#x27;}, &#x27;type&#x27;: &#x27;SUBSCRIBED&#x27;, &#x27;version&#x27;: &#x27;4&#x27;}, &#x27;_ansible_no_log&#x27;: None, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 1, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;client_token&#x27;: None, &#x27;creation_time&#x27;: None, &#x27;description&#x27;: None, &#x27;id&#x27;: None, &#x27;last_modified_time&#x27;: None, &#x27;last_sync_time&#x27;: None, &#x27;library_id&#x27;: &#x27;8b4e355e-a463-44f1-9b04-d0786a49cc7d&#x27;, &#x27;name&#x27;: None, &#x27;optimization_info&#x27;: None, &#x27;publish_info&#x27;: None, &#x27;server_guid&#x27;: None, &#x27;session_timeout&#x27;: None, &#x27;state&#x27;: &#x27;absent&#x27;, &#x27;storage_backings&#x27;: None, &#x27;subscription_info&#x27;: None, &#x27;type&#x27;: None, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: &#x27;/tmp/vmware_rest.log&#x27;, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;version&#x27;: None}}, &#x27;item&#x27;: {&#x27;creation_time&#x27;: &#x27;2022-11-23T20:06:05.189Z&#x27;, &#x27;description&#x27;: &#x27;&#x27;, &#x27;id&#x27;: &#x27;8b4e355e-a463-44f1-9b04-d0786a49cc7d&#x27;, &#x27;last_modified_time&#x27;: &#x27;2022-11-23T20:06:05.189Z&#x27;, &#x27;last_sync_time&#x27;: &#x27;2022-11-23T20:06:07.717Z&#x27;, &#x27;name&#x27;: &#x27;sub_lib&#x27;, &#x27;server_guid&#x27;: &#x27;52fb0b5e-ffc3-465b-bf4f-e4e6d5423cf5&#x27;, &#x27;storage_backings&#x27;: [{&#x27;datastore_id&#x27;: &#x27;datastore-1065&#x27;, &#x27;type&#x27;: &#x27;DATASTORE&#x27;}], &#x27;subscription_info&#x27;: {&#x27;authentication_method&#x27;: &#x27;NONE&#x27;, &#x27;automatic_sync_enabled&#x27;: 0, &#x27;on_demand&#x27;: 1, &#x27;subscription_url&#x27;: &#x27;https://vcenter.test:443/cls/vcsp/lib/a66d5c73-57f8-4a3a-9361-292a55f68516/lib.json&#x27;}, &#x27;type&#x27;: &#x27;SUBSCRIBED&#x27;, &#x27;version&#x27;: &#x27;4&#x27;}, &#x27;value&#x27;: {}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
