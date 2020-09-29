.. _vmware.vmware_rest.vcenter_host_info_module:


************************************
vmware.vmware_rest.vcenter_host_info
************************************

**Collect the information associated with the vCenter hosts**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Collect the information associated with the vCenter hosts



Requirements
------------
The below requirements are needed on the host that executes this module.

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
                    <b>filter_clusters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Clusters that must contain the hosts for the hosts to match the filter.</div>
                        <div>If unset or empty, hosts in any cluster and hosts that are not in a cluster match the filter. If this field is not empty and <em>standalone</em> is true, no hosts will match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_cluster_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_connection_states</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Connection states that a host must be in to match the filter (see I()</div>
                        <div>If unset or empty, hosts in any connection state match the filter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_datacenters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Datacenters that must contain the hosts for the hosts to match the filter.</div>
                        <div>If unset or empty, hosts in any datacenter match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_datacenter_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_folders</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Folders that must contain the hosts for the hosts to match the filter.</div>
                        <div>If unset or empty, hosts in any folder match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_folder_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_hosts</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifiers of hosts that can match the filter.</div>
                        <div>If unset or empty, hosts with any identifier match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_host_info</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Names that hosts must have to match the filter (see <em>name</em>).</div>
                        <div>If unset or empty, hosts with any name match the filter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_standalone</b>
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
                        <div>If true, only hosts that are not part of a cluster can match the filter, and if false, only hosts that are are part of a cluster can match the filter.</div>
                        <div>If unset Hosts can match filter independent of whether they are part of a cluster or not. If this field is true and <em>clusters</em> os not empty, no hosts will match the filter.</div>
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
                        <div>The vSphere vCenter username</div>
                        <div>If the value is not specified in the task, the value of environment variable <code>VMWARE_PASSWORD</code> will be used instead.</div>
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

.. code-block:: yaml+jinja

    - name: Get a list of the hosts
      vcenter_host_info:
      register: my_hosts



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
                            <div>Get a list of the hosts</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;connection_state&#x27;: &#x27;CONNECTED&#x27;, &#x27;host&#x27;: &#x27;host-1367&#x27;, &#x27;name&#x27;: &#x27;esxi1.test&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
