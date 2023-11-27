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

- vSphere 7.0.3 or greater
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
                        <div>- <code>windows_config</code> (dict): Guest customization specification for a Windows guest operating system</div>
                        <div>If unset, ConfigurationSpec.linux-config or ConfigurationSpec.cloud-config must be set. Otherwise, an appropriate fault will be thrown. ([&#x27;set&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- reboot (string): This option specifies what should be done to the guest after the customization.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>NO_REBOOT</code></div>
                        <div>- <code>REBOOT</code></div>
                        <div>- <code>SHUTDOWN</code></div>
                        <div>- sysprep (object): Customization settings like user details, administrator details, etc for the windows guest operating system. Exactly one of WindowsConfiguration.sysprep or WindowsConfiguration.sysprep-xml must be specified.</div>
                        <div>If unset, sysprep settings will not be applied to the windows guest operating system.</div>
                        <div>- sysprep_xml (string): All settings specified in a XML format. This is the content of a typical answer.xml file that is used by System administrators during the Windows image customization. Check https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/update-windows-settings-and-scripts-create-your-own-answer-file-sxs Exactly one of WindowsConfiguration.sysprep or WindowsConfiguration.sysprep-xml must be specified.</div>
                        <div>If unset, sysprep settings will not be applied to the windows guest operating system.</div>
                        <div>- <code>linux_config</code> (dict): Guest customization specification for a linux guest operating system</div>
                        <div>If unset, ConfigurationSpec.windows-config or ConfigurationSpec.cloud-config must be set. Otherwise, an appropriate fault will be thrown. ([&#x27;set&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- hostname (object): The computer name of the (Windows) virtual machine. A computer name may contain letters (A-Z), numbers(0-9) and hyphens (-) but no spaces or periods (.). The name may not consist entirely of digits. A computer name is restricted to 15 characters in length. If the computer name is longer than 15 characters, it will be truncated to 15 characters. Check HostnameGenerator for various options.</div>
                        <div>- domain (string): The fully qualified domain name.</div>
                        <div>- time_zone (string): The case-sensitive time zone, such as Europe/Sofia. Valid time zone values are based on the tz (time zone) database used by Linux. The values are strings (string) in the form &quot;Area/Location,&quot; in which Area is a continent or ocean name, and Location is the city, island, or other regional designation.</div>
                        <div>See the https://kb.vmware.com/kb/2145518 for a list of supported time zones for different versions in Linux.</div>
                        <div></div>
                        <div>If unset, time zone is not modified inside guest operating system.</div>
                        <div>- script_text (string): The script to run before and after Linux guest customization.</div>
                        <div>The max size of the script is 1500 bytes. As long as the script (shell, perl, python...) has the right &quot;#!&quot; in the header, it is supported. The caller should not assume any environment variables when the script is run.</div>
                        <div>The script is invoked by the customization engine using the command line: 1) with argument &quot;precustomization&quot; before customization, 2) with argument &quot;postcustomization&quot; after customization. The script should parse this argument and implement pre-customization or post-customization task code details in the corresponding block.</div>
                        <div></div>
                        <div>A Linux shell script example:</div>
                        <div></div>
                        <div>#!/bin/sh</div>
                        <div>if [ x$1 == x&quot;precustomization&quot; ]; then</div>
                        <div>echo &quot;Do Precustomization tasks&quot;</div>
                        <div>#code for pre-customization actions...</div>
                        <div>elif [ x$1 == x&quot;postcustomization&quot; ]; then</div>
                        <div>echo &quot;Do Postcustomization tasks&quot;</div>
                        <div>#code for post-customization actions...</div>
                        <div>fi</div>
                        <div></div>
                        <div></div>
                        <div>If unset, no script will be executed.</div>
                        <div>- <code>cloud_config</code> (dict): Guest customization specification with cloud configuration.</div>
                        <div>If unset, ConfigurationSpec.windows-config or ConfigurationSpec.linux-config must be set. Otherwise, an appropriate fault will be thrown. ([&#x27;set&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option specifies different types of the cloud configuration.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>CLOUDINIT</code></div>
                        <div>- cloudinit (object): cloud-init configuration</div>
                        <div>This field is optional and it is only relevant when the value of CloudConfiguration.type is CLOUDINIT.</div>
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
                        <div>- <code>dns_suffix_list</code> (list): List of name resolution suffixes for the virtual network adapter. This list applies to both Windows and Linux guest customization. For Linux, this setting is global, whereas in Windows, this setting is listed on a per-adapter basis.</div>
                        <div>If unset, no DNS suffixes are set. ([&#x27;set&#x27;])</div>
                        <div>- <code>dns_servers</code> (list): List of DNS servers, for a virtual network adapter with a static IP address. If this list is empty, then the guest operating system is expected to use a DHCP server to get its DNS server settings. These settings configure the virtual machine to use the specified DNS servers. These DNS server settings are listed in the order of preference.</div>
                        <div>If unset, no DNS servers are set. ([&#x27;set&#x27;])</div>
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
                        <div>IP settings that are specific to a particular virtual network adapter. The AdapterMapping structure maps a network adapter&#x27;s MAC address to its IPSettings. May be empty if there are no network adapters, else should match number of network adapters configured for the VM. This parameter is mandatory.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>mac_address</code> (str): The MAC address of a network adapter being customized.</div>
                        <div>If unset, the customization process maps the the settings from the list of <em>i_p_settings</em> in the CustomizationSpec.interfaces to the virtual machine&#x27;s network adapters, in PCI slot order. The first virtual network adapter on the PCI bus is assigned interfaces[0].IPSettings, the second adapter is assigned interfaces[1].IPSettings, and so on. ([&#x27;set&#x27;])</div>
                        <div>- <code>adapter</code> (dict): The IP settings for the associated virtual network adapter. ([&#x27;set&#x27;])</div>
                        <div>This key is required with [&#x27;set&#x27;].</div>
                        <div>- Accepted keys:</div>
                        <div>- ipv4 (object): Specification to configure IPv4 address, subnet mask and gateway info for this virtual network adapter.</div>
                        <div>If unset, no IPv4 addresses are set.</div>
                        <div>- ipv6 (object): Specification to configure IPv6 address, subnet mask and gateway info for this virtual network adapter.</div>
                        <div>If unset, no IPv6 addresses are set.</div>
                        <div>- windows (object): Windows settings to be configured for this specific virtual Network adapter. This is valid only for Windows guest operating systems.</div>
                        <div>If unset, no specific Windows settings are set.</div>
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
                                    <li><div style="color: blue"><b>set</b>&nbsp;&larr;</div></li>
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
                        <div>The unique identifier of the virtual machine that needs to be customized.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_info</span>. This parameter is mandatory.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.3



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
