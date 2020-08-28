.. _vmware.vmware_rest.vcenter_vm_module:


*****************************
vmware.vmware_rest.vcenter_vm
*****************************

**Handle resource of type vcenter_vm**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Handle resource of type vcenter_vm



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
                    <b>bios_uuid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>128-bit SMBIOS UUID of a virtual machine represented as a hexadecimal string in &quot;12345678-abcd-1234-cdef-123456789abc&quot; format.</div>
                        <div>If unset, will be generated.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>boot</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Boot configuration.</div>
                        <div>If unset, guest-specific default values will be used.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>delay</code> (int): Delay in milliseconds before beginning the firmware boot process when the virtual machine is powered on. This delay may be used to provide a time window for users to connect to the virtual machine console and enter BIOS setup mode.</div>
                        <div>If unset, default value is 0.</div>
                        <div>- <code>efi_legacy_boot</code> (bool): Flag indicating whether to use EFI legacy boot mode.</div>
                        <div>If unset, defaults to value that is recommended for the guest OS and is supported for the virtual hardware version.</div>
                        <div>- <code>enter_setup_mode</code> (bool): Flag indicating whether the firmware boot process should automatically enter setup mode the next time the virtual machine boots. Note that this flag will automatically be reset to false once the virtual machine enters setup mode.</div>
                        <div>If unset, the value is unchanged.</div>
                        <div>- <code>network_protocol</code> (str): The Boot.NetworkProtocol enumerated type defines the valid network boot protocols supported when booting a virtual machine with EFI firmware over the network.</div>
                        <div>- <code>retry</code> (bool): Flag indicating whether the virtual machine should automatically retry the boot process after a failure.</div>
                        <div>If unset, default value is false.</div>
                        <div>- <code>retry_delay</code> (int): Delay in milliseconds before retrying the boot process after a failure; applicable only when Boot.Info.retry is true.</div>
                        <div>If unset, default value is 10000.</div>
                        <div>- <code>type</code> (str): The Boot.Type enumerated type defines the valid firmware types for a virtual machine.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>boot_devices</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Boot device configuration.</div>
                        <div>If unset, a server-specific boot sequence will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cdroms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of CD-ROMs.</div>
                        <div>If unset, no CD-ROM devices will be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cpu</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>CPU configuration.</div>
                        <div>If unset, guest-specific default values will be used.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>cores_per_socket</code> (int): New number of CPU cores per socket. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket.</div>
                        <div>If unset, the value is unchanged.</div>
                        <div>- <code>count</code> (int): New number of CPU cores. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket.</div>
                        <div>The supported range of CPU counts is constrained by the configured guest operating system and virtual hardware version of the virtual machine.</div>
                        <div>If the virtual machine is running, the number of CPU cores may only be increased if Cpu.Info.hot-add-enabled is true, and may only be decreased if Cpu.Info.hot-remove-enabled is true.</div>
                        <div>If unset, the value is unchanged.</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding CPUs while the virtual machine is running is enabled.</div>
                        <div>This field may only be modified if the virtual machine is powered off.</div>
                        <div>If unset, the value is unchanged.</div>
                        <div>- <code>hot_remove_enabled</code> (bool): Flag indicating whether removing CPUs while the virtual machine is running is enabled.</div>
                        <div>This field may only be modified if the virtual machine is powered off.</div>
                        <div>If unset, the value is unchanged.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>datastore</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the datastore on which the virtual machine&#x27;s configuration state is stored.</div>
                        <div>If unset, VM.RegisterSpec.path must also be unset and VM.RegisterSpec.datastore-path must be set.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: Datastore. When operations return a value of this structure as a result, the field will be an identifier for the resource type: Datastore.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>datastore_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Datastore path for the virtual machine&#x27;s configuration file in the format &quot;[datastore name] path&quot;. For example &quot;[storage1] Test-VM/Test-VM.vmx&quot;.</div>
                        <div>If unset, both VM.RegisterSpec.datastore and VM.RegisterSpec.path must be set.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disconnect_all_nics</b>
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
                        <div>Indicates whether all NICs on the destination virtual machine should be disconnected from the newtwork</div>
                        <div>If unset, connection status of all NICs on the destination virtual machine will be the same as on the source virtual machine.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disks</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Individual disk relocation map.</div>
                        <div>If unset, all disks will migrate to the datastore specified in the VM.RelocatePlacementSpec.datastore field of VM.RelocateSpec.placement.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be an identifier for the resource type: vcenter.vm.hardware.Disk. When operations return a value of this structure as a result, the key in the field map will be an identifier for the resource type: vcenter.vm.hardware.Disk.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disks_to_remove</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Set of Disks to Remove.</div>
                        <div>If unset, all disks will be copied. If the same identifier is in VM.CloneSpec.disks-to-update InvalidArgument fault will be returned.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain identifiers for the resource type: vcenter.vm.hardware.Disk. When operations return a value of this structure as a result, the field will contain identifiers for the resource type: vcenter.vm.hardware.Disk.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disks_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of Disks to Update.</div>
                        <div>If unset, all disks will copied to the datastore specified in the VM.ClonePlacementSpec.datastore field of VM.CloneSpec.placement. If the same identifier is in VM.CloneSpec.disks-to-remove InvalidArgument fault will be thrown.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be an identifier for the resource type: vcenter.vm.hardware.Disk. When operations return a value of this structure as a result, the key in the field map will be an identifier for the resource type: vcenter.vm.hardware.Disk.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>floppies</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of floppy drives.</div>
                        <div>If unset, no floppy drives will be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>guest_customization_spec</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Guest customization spec to apply to the virtual machine after the virtual machine is deployed.</div>
                        <div>If unset, the guest operating system is not customized after clone.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>name</code> (str): Name of the customization specification.</div>
                        <div>If unset, no guest customization is performed.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>guest_OS</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>AMAZONLINUX2_64</li>
                                    <li>ASIANUX_3</li>
                                    <li>ASIANUX_3_64</li>
                                    <li>ASIANUX_4</li>
                                    <li>ASIANUX_4_64</li>
                                    <li>ASIANUX_5_64</li>
                                    <li>ASIANUX_7_64</li>
                                    <li>ASIANUX_8_64</li>
                                    <li>CENTOS</li>
                                    <li>CENTOS_6</li>
                                    <li>CENTOS_64</li>
                                    <li>CENTOS_6_64</li>
                                    <li>CENTOS_7</li>
                                    <li>CENTOS_7_64</li>
                                    <li>CENTOS_8_64</li>
                                    <li>COREOS_64</li>
                                    <li>CRXPOD_1</li>
                                    <li>DARWIN</li>
                                    <li>DARWIN_10</li>
                                    <li>DARWIN_10_64</li>
                                    <li>DARWIN_11</li>
                                    <li>DARWIN_11_64</li>
                                    <li>DARWIN_12_64</li>
                                    <li>DARWIN_13_64</li>
                                    <li>DARWIN_14_64</li>
                                    <li>DARWIN_15_64</li>
                                    <li>DARWIN_16_64</li>
                                    <li>DARWIN_17_64</li>
                                    <li>DARWIN_18_64</li>
                                    <li>DARWIN_19_64</li>
                                    <li>DARWIN_64</li>
                                    <li>DEBIAN_10</li>
                                    <li>DEBIAN_10_64</li>
                                    <li>DEBIAN_11</li>
                                    <li>DEBIAN_11_64</li>
                                    <li>DEBIAN_4</li>
                                    <li>DEBIAN_4_64</li>
                                    <li>DEBIAN_5</li>
                                    <li>DEBIAN_5_64</li>
                                    <li>DEBIAN_6</li>
                                    <li>DEBIAN_6_64</li>
                                    <li>DEBIAN_7</li>
                                    <li>DEBIAN_7_64</li>
                                    <li>DEBIAN_8</li>
                                    <li>DEBIAN_8_64</li>
                                    <li>DEBIAN_9</li>
                                    <li>DEBIAN_9_64</li>
                                    <li>DOS</li>
                                    <li>ECOMSTATION</li>
                                    <li>ECOMSTATION_2</li>
                                    <li>FEDORA</li>
                                    <li>FEDORA_64</li>
                                    <li>FREEBSD</li>
                                    <li>FREEBSD_11</li>
                                    <li>FREEBSD_11_64</li>
                                    <li>FREEBSD_12</li>
                                    <li>FREEBSD_12_64</li>
                                    <li>FREEBSD_64</li>
                                    <li>GENERIC_LINUX</li>
                                    <li>MANDRAKE</li>
                                    <li>MANDRIVA</li>
                                    <li>MANDRIVA_64</li>
                                    <li>NETWARE_4</li>
                                    <li>NETWARE_5</li>
                                    <li>NETWARE_6</li>
                                    <li>NLD_9</li>
                                    <li>OES</li>
                                    <li>OPENSERVER_5</li>
                                    <li>OPENSERVER_6</li>
                                    <li>OPENSUSE</li>
                                    <li>OPENSUSE_64</li>
                                    <li>ORACLE_LINUX</li>
                                    <li>ORACLE_LINUX_6</li>
                                    <li>ORACLE_LINUX_64</li>
                                    <li>ORACLE_LINUX_6_64</li>
                                    <li>ORACLE_LINUX_7</li>
                                    <li>ORACLE_LINUX_7_64</li>
                                    <li>ORACLE_LINUX_8_64</li>
                                    <li>OS2</li>
                                    <li>OTHER</li>
                                    <li>OTHER_24X_LINUX</li>
                                    <li>OTHER_24X_LINUX_64</li>
                                    <li>OTHER_26X_LINUX</li>
                                    <li>OTHER_26X_LINUX_64</li>
                                    <li>OTHER_3X_LINUX</li>
                                    <li>OTHER_3X_LINUX_64</li>
                                    <li>OTHER_4X_LINUX</li>
                                    <li>OTHER_4X_LINUX_64</li>
                                    <li>OTHER_64</li>
                                    <li>OTHER_LINUX</li>
                                    <li>OTHER_LINUX_64</li>
                                    <li>REDHAT</li>
                                    <li>RHEL_2</li>
                                    <li>RHEL_3</li>
                                    <li>RHEL_3_64</li>
                                    <li>RHEL_4</li>
                                    <li>RHEL_4_64</li>
                                    <li>RHEL_5</li>
                                    <li>RHEL_5_64</li>
                                    <li>RHEL_6</li>
                                    <li>RHEL_6_64</li>
                                    <li>RHEL_7</li>
                                    <li>RHEL_7_64</li>
                                    <li>RHEL_8_64</li>
                                    <li>SJDS</li>
                                    <li>SLES</li>
                                    <li>SLES_10</li>
                                    <li>SLES_10_64</li>
                                    <li>SLES_11</li>
                                    <li>SLES_11_64</li>
                                    <li>SLES_12</li>
                                    <li>SLES_12_64</li>
                                    <li>SLES_15_64</li>
                                    <li>SLES_64</li>
                                    <li>SOLARIS_10</li>
                                    <li>SOLARIS_10_64</li>
                                    <li>SOLARIS_11_64</li>
                                    <li>SOLARIS_6</li>
                                    <li>SOLARIS_7</li>
                                    <li>SOLARIS_8</li>
                                    <li>SOLARIS_9</li>
                                    <li>SUSE</li>
                                    <li>SUSE_64</li>
                                    <li>TURBO_LINUX</li>
                                    <li>TURBO_LINUX_64</li>
                                    <li>UBUNTU</li>
                                    <li>UBUNTU_64</li>
                                    <li>UNIXWARE_7</li>
                                    <li>VMKERNEL</li>
                                    <li>VMKERNEL_5</li>
                                    <li>VMKERNEL_6</li>
                                    <li>VMKERNEL_65</li>
                                    <li>VMKERNEL_7</li>
                                    <li>VMWARE_PHOTON_64</li>
                                    <li>WINDOWS_7</li>
                                    <li>WINDOWS_7_64</li>
                                    <li>WINDOWS_7_SERVER_64</li>
                                    <li>WINDOWS_8</li>
                                    <li>WINDOWS_8_64</li>
                                    <li>WINDOWS_8_SERVER_64</li>
                                    <li>WINDOWS_9</li>
                                    <li>WINDOWS_9_64</li>
                                    <li>WINDOWS_9_SERVER_64</li>
                                    <li>WINDOWS_HYPERV</li>
                                    <li>WINDOWS_SERVER_2019</li>
                                    <li>WIN_2000_ADV_SERV</li>
                                    <li>WIN_2000_PRO</li>
                                    <li>WIN_2000_SERV</li>
                                    <li>WIN_31</li>
                                    <li>WIN_95</li>
                                    <li>WIN_98</li>
                                    <li>WIN_LONGHORN</li>
                                    <li>WIN_LONGHORN_64</li>
                                    <li>WIN_ME</li>
                                    <li>WIN_NET_BUSINESS</li>
                                    <li>WIN_NET_DATACENTER</li>
                                    <li>WIN_NET_DATACENTER_64</li>
                                    <li>WIN_NET_ENTERPRISE</li>
                                    <li>WIN_NET_ENTERPRISE_64</li>
                                    <li>WIN_NET_STANDARD</li>
                                    <li>WIN_NET_STANDARD_64</li>
                                    <li>WIN_NET_WEB</li>
                                    <li>WIN_NT</li>
                                    <li>WIN_VISTA</li>
                                    <li>WIN_VISTA_64</li>
                                    <li>WIN_XP_HOME</li>
                                    <li>WIN_XP_PRO</li>
                                    <li>WIN_XP_PRO_64</li>
                        </ul>
                </td>
                <td>
                        <div>The {@name GuestOS} defines the valid guest operating system types used for configuring a virtual machine. Required with <em>state=[&#x27;create&#x27;]</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hardware_version</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>VMX_03</li>
                                    <li>VMX_04</li>
                                    <li>VMX_06</li>
                                    <li>VMX_07</li>
                                    <li>VMX_08</li>
                                    <li>VMX_09</li>
                                    <li>VMX_10</li>
                                    <li>VMX_11</li>
                                    <li>VMX_12</li>
                                    <li>VMX_13</li>
                                    <li>VMX_14</li>
                                    <li>VMX_15</li>
                                    <li>VMX_16</li>
                                    <li>VMX_17</li>
                        </ul>
                </td>
                <td>
                        <div>The Hardware.Version enumerated type defines the valid virtual hardware versions for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual machine hardware versions (1003746)).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>memory</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Memory configuration.</div>
                        <div>If unset, guest-specific default values will be used.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding memory while the virtual machine is running should be enabled.</div>
                        <div>Some guest operating systems may consume more resources or perform less efficiently when they run on hardware that supports adding memory while the machine is running.</div>
                        <div>This field may only be modified if the virtual machine is not powered on.</div>
                        <div>If unset, the value is unchanged.</div>
                        <div>- <code>size_MiB</code> (int): New memory size in mebibytes.</div>
                        <div>The supported range of memory sizes is constrained by the configured guest operating system and virtual hardware version of the virtual machine.</div>
                        <div>If the virtual machine is running, this value may only be changed if Memory.Info.hot-add-enabled is true, and the new memory size must satisfy the constraints specified by Memory.Info.hot-add-increment-size-mib and Memory.Info.hot-add-limit-mib.</div>
                        <div>If unset, the value is unchanged.</div>
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
                        <div>Virtual machine name.</div>
                        <div>If unset, the display name from the virtual machine&#x27;s configuration file will be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nics</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of Ethernet adapters.</div>
                        <div>If unset, no Ethernet adapters will be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nics_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of NICs to update.</div>
                        <div>If unset, no NICs will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be an identifier for the resource type: vcenter.vm.hardware.Ethernet. When operations return a value of this structure as a result, the key in the field map will be an identifier for the resource type: vcenter.vm.hardware.Ethernet.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parallel_ports</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of parallel ports.</div>
                        <div>If unset, no parallel ports will be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parallel_ports_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of parallel ports to Update.</div>
                        <div>If unset, no parallel ports will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be an identifier for the resource type: vcenter.vm.hardware.ParallelPort. When operations return a value of this structure as a result, the key in the field map will be an identifier for the resource type: vcenter.vm.hardware.ParallelPort.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to the virtual machine&#x27;s configuration file on the datastore corresponding to {@link #datastore).</div>
                        <div>If unset, VM.RegisterSpec.datastore must also be unset and VM.RegisterSpec.datastore-path must be set.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>placement</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual machine placement information.</div>
                        <div>If this field is unset, the system will use the values from the source virtual machine. If specified, each field will be used for placement. If the fields result in disjoint placement the operation will fail. If the fields along with the other existing placement of the virtual machine result in disjoint placement the operation will fail.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>cluster</code> (str): Cluster into which the virtual machine should be placed.</div>
                        <div>If VM.ComputePlacementSpec.cluster and VM.ComputePlacementSpec.resource-pool are both specified, VM.ComputePlacementSpec.resource-pool must belong to VM.ComputePlacementSpec.cluster.</div>
                        <div>If VM.ComputePlacementSpec.cluster and VM.ComputePlacementSpec.host are both specified, VM.ComputePlacementSpec.host must be a member of VM.ComputePlacementSpec.cluster.</div>
                        <div>If VM.ComputePlacementSpec.resource-pool or VM.ComputePlacementSpec.host is specified, it is recommended that this field be unset.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: ClusterComputeResource. When operations return a value of this structure as a result, the field will be an identifier for the resource type: ClusterComputeResource.</div>
                        <div>- <code>datastore</code> (str): Datastore on which the virtual machine&#x27;s configuration state should be stored. This datastore will also be used for any virtual disks that are created as part of the virtual machine creation operation.</div>
                        <div>This field is currently required. In the future, if this field is unset, the system will attempt to choose suitable storage for the virtual machine; if storage cannot be chosen, the virtual machine creation operation will fail.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: Datastore. When operations return a value of this structure as a result, the field will be an identifier for the resource type: Datastore.</div>
                        <div>- <code>folder</code> (str): Virtual machine folder into which the virtual machine should be placed.</div>
                        <div>This field is currently required. In the future, if this field is unset, the system will attempt to choose a suitable folder for the virtual machine; if a folder cannot be chosen, the virtual machine creation operation will fail.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: Folder. When operations return a value of this structure as a result, the field will be an identifier for the resource type: Folder.</div>
                        <div>- <code>host</code> (str): Host onto which the virtual machine should be placed.</div>
                        <div>If VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.resource-pool are both specified, VM.ComputePlacementSpec.resource-pool must belong to VM.ComputePlacementSpec.host.</div>
                        <div>If VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.cluster are both specified, VM.ComputePlacementSpec.host must be a member of VM.ComputePlacementSpec.cluster.</div>
                        <div>This field may be unset if VM.ComputePlacementSpec.resource-pool or VM.ComputePlacementSpec.cluster is specified. If unset, the system will attempt to choose a suitable host for the virtual machine; if a host cannot be chosen, the virtual machine creation operation will fail.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: HostSystem. When operations return a value of this structure as a result, the field will be an identifier for the resource type: HostSystem.</div>
                        <div>- <code>resource_pool</code> (str): Resource pool into which the virtual machine should be placed.</div>
                        <div>This field is currently required if both VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.cluster are unset. In the future, if this field is unset, the system will attempt to choose a suitable resource pool for the virtual machine; if a resource pool cannot be chosen, the virtual machine creation operation will fail.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: ResourcePool. When operations return a value of this structure as a result, the field will be an identifier for the resource type: ResourcePool.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>power_on</b>
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
                        <div>Attempt to perform a VM.CloneSpec.power-on after clone.</div>
                        <div>If unset, the virtual machine will not be powered on.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sata_adapters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SATA adapters.</div>
                        <div>If unset, any adapters necessary to connect the virtual machine&#x27;s storage devices will be created; this includes any devices that explicitly specify a SATA host bus adapter, as well as any devices that do not specify a host bus adapter if the guest&#x27;s preferred adapter type is SATA.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scsi_adapters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SCSI adapters.</div>
                        <div>If unset, any adapters necessary to connect the virtual machine&#x27;s storage devices will be created; this includes any devices that explicitly specify a SCSI host bus adapter, as well as any devices that do not specify a host bus adapter if the guest&#x27;s preferred adapter type is SCSI. The type of the SCSI adapter will be a guest-specific default type.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_ports</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of serial ports.</div>
                        <div>If unset, no serial ports will be created.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_ports_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of serial ports to Update.</div>
                        <div>If unset, no serial ports will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be an identifier for the resource type: vcenter.vm.hardware.SerialPort. When operations return a value of this structure as a result, the key in the field map will be an identifier for the resource type: vcenter.vm.hardware.SerialPort.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Virtual machine to InstantClone from.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: VirtualMachine. When operations return a value of this structure as a result, the field will be an identifier for the resource type: VirtualMachine. Required with <em>state=[&#x27;clone&#x27;, &#x27;instant_clone&#x27;]</em></div>
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
                                    <li>clone</li>
                                    <li>instant_clone</li>
                                    <li>present</li>
                                    <li>register</li>
                                    <li>relocate</li>
                                    <li>unregister</li>
                        </ul>
                </td>
                <td>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>storage_policy</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The VM.StoragePolicySpec structure contains information about the storage policy that is to be associated with the virtual machine home (which contains the configuration and log files).</div>
                        <div>If unset the datastore default storage policy (if applicable) is applied. Currently a default storage policy is only supported by object datastores : VVol and vSAN. For non-object datastores, if unset then no storage policy would be associated with the virtual machine home.</div>
                        <div>Validate attributes are:</div>
                        <div>- <code>policy</code> (str): Identifier of the storage policy which should be associated with the virtual machine.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be an identifier for the resource type: vcenter.StoragePolicy. When operations return a value of this structure as a result, the field will be an identifier for the resource type: vcenter.StoragePolicy.</div>
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
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>vm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the virtual machine to be unregistered.</div>
                        <div>The parameter must be an identifier for the resource type: VirtualMachine. Required with <em>state=[&#x27;delete&#x27;, &#x27;relocate&#x27;, &#x27;unregister&#x27;]</em></div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml+jinja

    - name: _Wait for the vcenter server
      vcenter_vm_info:
      retries: 100
      delay: 3
      register: existing_vms
      until: existing_vms is not failed
    - name: Create a VM
      vcenter_vm:
        placement:
          cluster: '{{ all_the_clusters.value[0].cluster }}'
          datastore: '{{ rw_datastore.datastore }}'
          folder: '{{ my_virtual_machine_folder.folder }}'
          resource_pool: '{{ my_cluster_info.value.resource_pool }}'
        name: test_vm1
        guest_OS: DEBIAN_8_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
    - name: Create a VM (again)
      vcenter_vm:
        placement:
          cluster: '{{ all_the_clusters.value[0].cluster }}'
          datastore: '{{ rw_datastore.datastore }}'
          folder: '{{ my_virtual_machine_folder.folder }}'
          resource_pool: '{{ my_cluster_info.value.resource_pool }}'
        name: test_vm1
        guest_OS: DEBIAN_8_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
    - name: Delete some VM
      vcenter_vm:
        state: absent
        vm: '{{ item.vm }}'
      with_items: '{{ existing_vms.value }}'




Status
------


Authors
~~~~~~~

- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
