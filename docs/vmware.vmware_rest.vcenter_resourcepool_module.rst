.. _vmware.vmware_rest.vcenter_resourcepool_module:


***************************************
vmware.vmware_rest.vcenter_resourcepool
***************************************

**Creates a resource pool.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a resource pool.



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
                    <b>cpu_allocation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Resource allocation for CPU.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>reservation</code> (int): Amount of resource that is guaranteed available to a resource pool. Reserved resources are not wasted if they are not used. If the utilization is less than the reservation, the resources can be utilized by other running virtual machines. Units are MB fo memory, and MHz for CPU. ([&#x27;present&#x27;])</div>
                        <div>- <code>expandable_reservation</code> (bool): In a resource pool with an expandable reservation, the reservation can grow beyond the specified value, if the parent resource pool has unreserved resources. A non-expandable reservation is called a fixed reservation. ([&#x27;present&#x27;])</div>
                        <div>- <code>limit</code> (int): The utilization of a resource pool will not exceed this limit, even if there are available resources. This is typically used to ensure a consistent performance of resource pools independent of available resources. If set to -1, then there is no fixed limit on resource usage (only bounded by available resources and shares). Units are MB for memory, and MHz for CPU. ([&#x27;present&#x27;])</div>
                        <div>- <code>shares</code> (dict): Shares are used in case of resource contention. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- level (string): The <code>level</code> defines the possible values for the allocation level.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>CUSTOM</code></div>
                        <div>- <code>HIGH</code></div>
                        <div>- <code>LOW</code></div>
                        <div>- <code>NORMAL</code></div>
                        <div>- shares (integer): When {@link #level} is set to CUSTOM, it is the number of shares allocated. Otherwise, this value is ignored. There is no unit for this value. It is a relative measure based on the settings for other resource pools.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>memory_allocation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Resource allocation for CPU.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>reservation</code> (int): Amount of resource that is guaranteed available to a resource pool. Reserved resources are not wasted if they are not used. If the utilization is less than the reservation, the resources can be utilized by other running virtual machines. Units are MB fo memory, and MHz for CPU. ([&#x27;present&#x27;])</div>
                        <div>- <code>expandable_reservation</code> (bool): In a resource pool with an expandable reservation, the reservation can grow beyond the specified value, if the parent resource pool has unreserved resources. A non-expandable reservation is called a fixed reservation. ([&#x27;present&#x27;])</div>
                        <div>- <code>limit</code> (int): The utilization of a resource pool will not exceed this limit, even if there are available resources. This is typically used to ensure a consistent performance of resource pools independent of available resources. If set to -1, then there is no fixed limit on resource usage (only bounded by available resources and shares). Units are MB for memory, and MHz for CPU. ([&#x27;present&#x27;])</div>
                        <div>- <code>shares</code> (dict): Shares are used in case of resource contention. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- level (string): The <code>level</code> defines the possible values for the allocation level.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>CUSTOM</code></div>
                        <div>- <code>HIGH</code></div>
                        <div>- <code>LOW</code></div>
                        <div>- <code>NORMAL</code></div>
                        <div>- shares (integer): When {@link #level} is set to CUSTOM, it is the number of shares allocated. Otherwise, this value is ignored. There is no unit for this value. It is a relative measure based on the settings for other resource pools.</div>
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
                        <div>Name of the resource pool. Required with <em>state=[&#x27;present&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parent</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Parent of the created resource pool. Required with <em>state=[&#x27;present&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>resource_pool</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the resource pool to be deleted. Required with <em>state=[&#x27;absent&#x27;, &#x27;present&#x27;]</em></div>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
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

    - name: Get the existing resource pools
      vmware.vmware_rest.vcenter_resourcepool_info:
      register: resource_pools

    - name: Create an Ad hoc resource pool
      vmware.vmware_rest.vcenter_resourcepool:
        name: my_resource_pool
        parent: '{{ resource_pools.value[0].resource_pool }}'
        cpu_allocation:
        expandable_reservation: true
        limit: 40
        reservation: 0
        shares:
            level: NORMAL
        memory_allocation:
        expandable_reservation: false
        limit: 2000
        reservation: 0
        shares:
            level: NORMAL
      register: my_resource_pool

    - name: Remove a resource pool
      vmware.vmware_rest.vcenter_resourcepool:
        resource_pool: '{{ my_resource_pool.id }}'
        state: absent

    - name: Create a generic resource pool
      vmware.vmware_rest.vcenter_resourcepool:
        name: my_resource_pool
        parent: '{{ resource_pools.value[0].resource_pool }}'
      register: my_resource_pool

    - name: Modify a resource pool
      vmware.vmware_rest.vcenter_resourcepool:
        resource_pool: '{{ my_resource_pool.id }}'
        cpu_allocation:
        expandable_reservation: true
        limit: -1
        reservation: 0
        shares:
            level: NORMAL
        memory_allocation:
        expandable_reservation: false
        limit: 1000
        reservation: 0
        shares:
            level: NORMAL



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">resgroup-1009</div>
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
                            <div>Create a generic resource pool</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;cpu_allocation&#x27;: {&#x27;expandable_reservation&#x27;: 1, &#x27;limit&#x27;: -1, &#x27;reservation&#x27;: 0, &#x27;shares&#x27;: {&#x27;level&#x27;: &#x27;NORMAL&#x27;}}, &#x27;memory_allocation&#x27;: {&#x27;expandable_reservation&#x27;: 1, &#x27;limit&#x27;: -1, &#x27;reservation&#x27;: 0, &#x27;shares&#x27;: {&#x27;level&#x27;: &#x27;NORMAL&#x27;}}, &#x27;name&#x27;: &#x27;my_resource_pool&#x27;, &#x27;resource_pools&#x27;: []}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
