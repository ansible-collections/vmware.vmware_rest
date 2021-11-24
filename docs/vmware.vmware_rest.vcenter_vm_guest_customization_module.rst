.. _vmware.vmware_rest.vcenter_vm_guest_customization_module:


*************************************************
vmware.vmware_rest.vcenter_vm_guest_customization
*************************************************

**Applies a customization specification on the virtual machine**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Applies a customization specification on the virtual machine in {@param.name vm}. The actual customization happens inside the guest when the virtual machine is powered on. If there is a pending customization for the virtual machine and a new one is set, then the existing customization setting will be overwritten with the new settings.



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
                    <b>configuration_spec</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Settings to be applied to the guest during the customization. This parameter is mandatory.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>windows_config</code> (dict): Guest customization specification for a Windows guest operating system ([&#x27;set&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- reboot (string): The <code>reboot_option</code> specifies what should be done to the guest after the customization.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>NO_REBOOT</code></div>
                        <div>- <code>REBOOT</code></div>
                        <div>- <code>SHUTDOWN</code></div>
                        <div>- sysprep (object): Customization settings like user details, administrator details, etc for the windows guest operating system. Exactly one of <code>#sysprep</code> or <code>#sysprep_xml</code> must be specified.</div>
                        <div>- sysprep_xml (string): All settings specified in a XML format. This is the content of a typical answer.xml file that is used by System administrators during the Windows image customization. Check https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/update-windows-settings-and-scripts-create-your-own-answer-file-sxs Exactly one of <code>#sysprep</code> or <code>#sysprep_xml</code> must be specified.</div>
                        <div>- <code>linux_config</code> (dict): Guest customization specification for a linux guest operating system ([&#x27;set&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- hostname (object): The computer name of the (Windows) virtual machine. A computer name may contain letters (A-Z), numbers(0-9) and hyphens (-) but no spaces or periods (.). The name may not consist entirely of digits. A computer name is restricted to 15 characters in length. If the computer name is longer than 15 characters, it will be truncated to 15 characters. Check {@link HostnameGenerator} for various options.</div>
                        <div>- domain (string): The fully qualified domain name.</div>
                        <div>- time_zone (string): The case-sensitive time zone, such as Europe/Sofia. Valid time zone values are based on the tz (time zone) database used by Linux. The values are strings  in the form &quot;Area/Location,&quot; in which Area is a continent or ocean name, and Location is the city, island, or other regional designation. See the https://kb.vmware.com/kb/2145518 for a list of supported time zones for different versions in Linux.</div>
                        <div>- script_text (string): The script to run before and after Linux guest customization.&lt;br&gt; The max size of the script is 1500 bytes. As long as the script (shell, perl, python...) has the right &quot;#!&quot; in the header, it is supported. The caller should not assume any environment variables when the script is run. The script is invoked by the customization engine using the command line: 1) with argument &quot;precustomization&quot; before customization, 2) with argument &quot;postcustomization&quot; after customization. The script should parse this argument and implement pre-customization or post-customization task code details in the corresponding block. A Linux shell script example: &lt;code&gt; #!/bin/sh&lt;br&gt; if [ x$1 == x&quot;precustomization&quot; ]; then&lt;br&gt; echo &quot;Do Precustomization tasks&quot;&lt;br&gt; #code for pre-customization actions...&lt;br&gt; elif [ x$1 == x&quot;postcustomization&quot; ]; then&lt;br&gt; echo &quot;Do Postcustomization tasks&quot;&lt;br&gt; #code for post-customization actions...&lt;br&gt; fi&lt;br&gt; &lt;/code&gt;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>global_DNS_settings</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Global DNS settings constitute the DNS settings that are not specific to a particular virtual network adapter. This parameter is mandatory.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>dns_suffix_list</code> (list): List of name resolution suffixes for the virtual network adapter. This list applies to both Windows and Linux guest customization. For Linux, this setting is global, whereas in Windows, this setting is listed on a per-adapter basis. ([&#x27;set&#x27;])</div>
                        <div>- <code>dns_servers</code> (list): List of DNS servers, for a virtual network adapter with a static IP address. If this list is empty, then the guest operating system is expected to use a DHCP server to get its DNS server settings. These settings configure the virtual machine to use the specified DNS servers. These DNS server settings are listed in the order of preference. ([&#x27;set&#x27;])</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>interfaces</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>IP settings that are specific to a particular virtual network adapter. The {@link AdapterMapping} {@term structure} maps a network adapter&#x27;s MAC address to its {@link IPSettings}. May be empty if there are no network adapters, else should match number of network adapters configured for the VM. This parameter is mandatory.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>mac_address</code> (str): The MAC address of a network adapter being customized. ([&#x27;set&#x27;])</div>
                        <div>- <code>adapter</code> (dict): The IP settings for the associated virtual network adapter. ([&#x27;set&#x27;])</div>
                        <div>This key is required with [&#x27;set&#x27;].</div>
                        <div>- Accepted keys:</div>
                        <div>- ipv4 (object): Specification to configure IPv4 address, subnet mask and gateway info for this virtual network adapter.</div>
                        <div>- ipv6 (object): Specification to configure IPv6 address, subnet mask and gateway info for this virtual network adapter.</div>
                        <div>- windows (object): Windows settings to be configured for this specific virtual Network adapter. This is valid only for Windows guest operating systems.</div>
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
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The unique identifier of the virtual machine that needs to be customized. This parameter is mandatory.</div>
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

    - name: Customize the VM
      vmware.vmware_rest.vcenter_vm_guest_customization:
        vm: "{{ lookup('vmware.vmware_rest.vm_moid', '/my_dc/vm/test_vm1') }}"
        configuration_spec:
          linux_config:
            domain: mydomain
            hostname:
              fixed_name: foobar
              type: FIXED
        interfaces:
        - adapter:
            ipv4:
              type: STATIC
              gateways:
              - 192.168.123.1
              ip_address: 192.168.123.50
              prefix: 24
        global_DNS_settings:
          dns_suffix_list: []
          dns_servers:
          - 1.1.1.1



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
                            <div>Customize the VM</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
