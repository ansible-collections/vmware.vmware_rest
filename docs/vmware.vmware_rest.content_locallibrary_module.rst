.. _vmware.vmware_rest.content_locallibrary_module:


***************************************
vmware.vmware_rest.content_locallibrary
***************************************

**Creates a new local library.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a new local library.



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
                        <div>A unique token generated on the client for each creation request. The token should be a universally unique identifier (UUID), for example: <code>b8a2a2e3-2314-43cd-a871-6ede0f429751</code>. This token can be used to guarantee idempotent creation.</div>
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
                        <div>An identifier which uniquely identifies this Library.</div>
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
                        <div>Identifier of the local library to delete. Required with <em>state=[&#x27;absent&#x27;, &#x27;present&#x27;, &#x27;publish&#x27;]</em></div>
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
                        <div>- <code>optimize_remote_publishing</code> (bool): If set to <code>True</code> then library would be optimized for remote publishing. Turn it on if remote publishing is dominant use case for this library. Remote publishing means here that publisher and subscribers are not the part of the same vCenter SSO domain. Any optimizations could be done as result of turning on this optimization during library creation. For example, library content could be stored in different format but optimizations are not limited to just storage format. Note, that value of this toggle could be set only during creation of the library and you would need to migrate your library in case you need to change this value (optimize the library for different use case).</div>
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
                        <div>- <code>authentication_method</code> (str): The authentication_method indicates how a subscribed library should authenticate to the published library endpoint.</div>
                        <div>- Accepted values:</div>
                        <div>- BASIC</div>
                        <div>- NONE</div>
                        <div>- <code>published</code> (bool): Whether the local library is published.</div>
                        <div>- <code>publish_url</code> (str): The URL to which the library metadata is published by the Content Library Service. This value can be used to set the <code>subscription_info.subscriptionurl</code> property when creating a subscribed library.</div>
                        <div>- <code>user_name</code> (str): The username to require for authentication.</div>
                        <div>- <code>password</code> (str): The new password to require for authentication.</div>
                        <div>- <code>current_password</code> (str): The current password to verify. This field is available starting in vSphere 6.7.</div>
                        <div>- <code>persist_json_enabled</code> (bool): Whether library and library item metadata are persisted in the storage backing as JSON files. This flag only applies if the local library is published. Enabling JSON persistence allows you to synchronize a subscribed library manually instead of over HTTP. You copy the local library content and metadata to another storage backing manually and then create a subscribed library referencing the location of the library JSON file in the <code>subscription_info.subscriptionurl</code>. When the subscribed library&#x27;s storage backing matches the subscription URL, files do not need to be copied to the subscribed library. For a library backed by a datastore, the library JSON file will be stored at the path contentlib-{library_id}/lib.json on the datastore. For a library backed by a remote file system, the library JSON file will be stored at {library_id}/lib.json in the remote file system path.</div>
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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>absent</li>
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                                    <li>publish</li>
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
                        <div>- <code>type</code> (str): The {@name Type} specifies the type of the storage backing.</div>
                        <div>- Accepted values:</div>
                        <div>- DATASTORE</div>
                        <div>- OTHER</div>
                        <div>- <code>datastore_id</code> (str): Identifier of the datastore used to store the content in the library.</div>
                        <div>- <code>storage_uri</code> (str): URI identifying the location used to store the content in the library. The following URI formats are supported: vSphere 6.5 &lt;ul&gt; &lt;li&gt;nfs://server/path?version=4 (for vCenter Server Appliance only) - Specifies an NFS Version 4 server.&lt;/li&gt; &lt;li&gt;nfs://server/path (for vCenter Server Appliance only) - Specifies an NFS Version 3 server. The nfs://server:/path format is also supported.&lt;/li&gt; &lt;li&gt;smb://server/path - Specifies an SMB server or Windows share.&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 Update 1 &lt;ul&gt; &lt;li&gt;nfs://server:/path (for vCenter Server Appliance only)&lt;/li&gt; &lt;li&gt;file://unc-server/path (for vCenter Server for Windows only)&lt;/li&gt; &lt;li&gt;file:///mount/point (for vCenter Server Appliance only) - Local file URIs are supported only when the path is a local mount point for an NFS file system. Use of file URIs is strongly discouraged. Instead, use an NFS URI to specify the remote file system.&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 &lt;ul&gt; &lt;li&gt;nfs://server:/path (for vCenter Server Appliance only)&lt;/li&gt; &lt;li&gt;file://unc-server/path (for vCenter Server for Windows only)&lt;/li&gt; &lt;li&gt;file:///path - Local file URIs are supported but strongly discouraged because it may interfere with the performance of vCenter Server.&lt;/li&gt; &lt;/ul&gt;</div>
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
                        <div>- <code>authentication_method</code> (str): Indicate how the subscribed library should authenticate with the published library endpoint.</div>
                        <div>- Accepted values:</div>
                        <div>- BASIC</div>
                        <div>- NONE</div>
                        <div>- <code>automatic_sync_enabled</code> (bool): Whether the library should participate in automatic library synchronization. In order for automatic synchronization to happen, the global <code>configuration_model.automaticSyncEnabled</code> option must also be true. The subscription is still active even when automatic synchronization is turned off, but synchronization is only activated with an explicit call to Subscribed Library Sync or Subscribed Item Sync. In other words, manual synchronization is still available even when automatic synchronization is disabled.</div>
                        <div>- <code>on_demand</code> (bool): Indicates whether a library item&#x27;s content will be synchronized only on demand. If this is set to <code>True</code>, then the library item&#x27;s metadata will be synchronized but the item&#x27;s content (its files) will not be synchronized. The Content Library Service will synchronize the content upon request only. This can cause the first use of the content to have a noticeable delay. Items without synchronized content can be forcefully synchronized in advance using the Subscribed Item Sync call with <code>forceSyncContent} set to true. Once content has been synchronized, the content can removed with the {@link SubscribedItem#evict</code> call. If this value is set to <code>False</code>, all content will be synchronized in advance.</div>
                        <div>- <code>password</code> (str): The password to use when authenticating. The password must be set when using a password-based authentication method; empty strings are not allowed.</div>
                        <div>- <code>ssl_thumbprint</code> (str): An optional SHA-1 hash of the SSL certificate for the remote endpoint. If this value is defined the SSL certificate will be verified by comparing it to the SSL thumbprint. The SSL certificate must verify against the thumbprint. When specified, the standard certificate chain validation behavior is not used. The certificate chain is validated normally if this value is not set.</div>
                        <div>- <code>subscription_url</code> (str): The URL of the endpoint where the metadata for the remotely published library is being served. This URL can be the <code>publish_info.publishUrl</code> of the published library (for example, https://server/path/lib.json). If the source content comes from a published library with <code>publish_info.persistJsonEnabled</code>, the subscription URL can be a URL pointing to the library JSON file on a datastore or remote file system. The supported formats are: vSphere 6.5 &lt;ul&gt; &lt;li&gt;ds:///vmfs/volumes/{uuid}/mylibrary/lib.json (for datastore)&lt;/li&gt; &lt;li&gt;nfs://server/path/mylibrary/lib.json (for NFSv3 server on vCenter Server Appliance)&lt;/li&gt; &lt;li&gt;nfs://server/path/mylibrary/lib.json?version=4 (for NFSv4 server on vCenter Server Appliance) &lt;/li&gt; &lt;li&gt;smb://server/path/mylibrary/lib.json (for SMB server)&lt;/li&gt; &lt;/ul&gt; vSphere 6.0 &lt;ul&gt; &lt;li&gt;file://server/mylibrary/lib.json (for UNC server on vCenter Server for Windows)&lt;/li&gt; &lt;li&gt;file:///path/mylibrary/lib.json (for local file system)&lt;/li&gt; &lt;/ul&gt; When you specify a DS subscription URL, the datastore must be on the same vCenter Server as the subscribed library. When you specify an NFS or SMB subscription URL, the <code>Storage Backing URI</code> of the subscribed library must be on the same remote file server and should share a common parent path with the subscription URL.</div>
                        <div>- <code>user_name</code> (str): The username to use when authenticating. The username must be set when using a password-based authentication method. Empty strings are allowed for usernames.</div>
                        <div>- <code>source_info</code> (dict): Information about the source published library. This field will be set for a subscribed library which is associated with a subscription of the published library.</div>
                        <div>- Accepted keys:</div>
                        <div>- source_library (string): Identifier of the published library.</div>
                        <div>- subscription (string): Identifier of the subscription associated with the subscribed library.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>subscriptions</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The list of subscriptions to publish this library to.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>subscription</code> (str): Identifier of the subscription associated with the subscribed library.</div>
                        <div>This key is required.</div>
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
                        <div>The Library Type defines the type of a Library. The type of a library can be used to determine which additional services can be performed with a library.</div>
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




Examples
--------

.. code-block:: yaml

    - name: Build a list of local libraries
      vmware.vmware_rest.content_locallibrary_info:
      register: result

    - name: Delete all the local libraries
      vmware.vmware_rest.content_locallibrary:
        library_id: '{{ item.id }}'
        state: absent
      with_items: '{{ result.value }}'

    - name: Create a content library pointing on the NFS share
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

    - name: Adjust vpxd configuration
      vmware.vmware_rest.appliance_vmon_service:
        service: vpxd
        startup_type: AUTOMATIC
      register: result

    - name: Set datastore id
      set_fact:
        datastore_id: '{{ result.value[0].datastore }}'

    - name: Create a new local content library
      vmware.vmware_rest.content_locallibrary:
        name: local_library_001
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - datastore_id: '{{ datastore_id }}'
          type: DATASTORE
        state: present
      register: ds_lib




Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
