.. _vmware.vmware_rest.vcenter_storage_policies_info_module:


************************************************
vmware.vmware_rest.vcenter_storage_policies_info
************************************************

**Collect the information associated with the vCenter storage policiess**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Collect the information associated with the vCenter storage policiess



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
                    <b>filter_policies</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifiers of storage policies that can match the filter.</div>
                        <div>If unset or empty, storage policies with any identifiers match the filter.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vcenter_storage_policies</span>.</div>
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

    - name: List existing storage policies
      vcenter_storage_policies_info:
      register: storage_policies



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
                            <div>List existing storage policies</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;description&#x27;: &#x27;Management Storage policy used for VMC large cluster&#x27;, &#x27;name&#x27;: &#x27;Management Storage Policy - Large&#x27;, &#x27;policy&#x27;: &#x27;cd8f7c94-3e11-67fc-17f5-4e96d91a5beb&#x27;}, {&#x27;description&#x27;: &#x27;Allow the datastore to determine the best placement strategy for storage objects&#x27;, &#x27;name&#x27;: &#x27;VVol No Requirements Policy&#x27;, &#x27;policy&#x27;: &#x27;f4e5bade-15a2-4805-bf8e-52318c4ce443&#x27;}, {&#x27;description&#x27;: &quot;Sample storage policy for VMware&#x27;s VM and virtual disk encryption&quot;, &#x27;name&#x27;: &#x27;VM Encryption Policy&#x27;, &#x27;policy&#x27;: &#x27;4d5f673c-536f-11e6-beb8-9e71128cae77&#x27;}, {&#x27;description&#x27;: &#x27;Management Storage policy used for encrypting VM&#x27;, &#x27;name&#x27;: &#x27;Management Storage policy - Encryption&#x27;, &#x27;policy&#x27;: &#x27;b1263970-8662-69e2-adc6-fa8ae01abecc&#x27;}, {&#x27;description&#x27;: &#x27;Management Storage policy used for VMC single node cluster&#x27;, &#x27;name&#x27;: &#x27;Management Storage Policy - Single Node&#x27;, &#x27;policy&#x27;: &#x27;a9423670-7455-11e8-adc0-fa7ae01bbebc&#x27;}, {&#x27;description&#x27;: &#x27;Storage policy used as default for Host-local PMem datastores&#x27;, &#x27;name&#x27;: &#x27;Host-local PMem Default Storage Policy&#x27;, &#x27;policy&#x27;: &#x27;c268da1b-b343-49f7-a468-b1deeb7078e0&#x27;}, {&#x27;description&#x27;: &#x27;Storage policy used as default for vSAN datastores&#x27;, &#x27;name&#x27;: &#x27;vSAN Default Storage Policy&#x27;, &#x27;policy&#x27;: &#x27;aa6d5a82-1c88-45da-85d3-3d74b91a5bad&#x27;}, {&#x27;description&#x27;: &#x27;Management Storage policy used for VMC regular cluster&#x27;, &#x27;name&#x27;: &#x27;Management Storage Policy - Regular&#x27;, &#x27;policy&#x27;: &#x27;bb7e6b13-2d99-46eb-96e4-3d85c91a5bde&#x27;}, {&#x27;description&#x27;: &#x27;Management Storage policy used for VMC regular cluster which requires THIN provisioning&#x27;, &#x27;name&#x27;: &#x27;Management Storage policy - Thin&#x27;, &#x27;policy&#x27;: &#x27;b6423670-8552-66e8-adc1-fa6ae01abeac&#x27;}, {&#x27;description&#x27;: &#x27;Management Storage policy used for VMC stretched cluster&#x27;, &#x27;name&#x27;: &#x27;Management Storage Policy - Stretched&#x27;, &#x27;policy&#x27;: &#x27;f31f2442-8247-4517-87c2-8d69d7a6c696&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
