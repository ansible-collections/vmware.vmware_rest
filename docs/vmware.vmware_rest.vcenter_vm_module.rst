.. _vmware.vmware_rest.vcenter_vm_module:


*****************************
vmware.vmware_rest.vcenter_vm
*****************************

**Creates a virtual machine.**


Version added: 0.1.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Creates a virtual machine.



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
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name Type} defines the valid firmware types for a virtual machine.</div>
                        <div>- Accepted values:</div>
                        <div>- BIOS</div>
                        <div>- EFI</div>
                        <div>- <code>efi_legacy_boot</code> (bool): Flag indicating whether to use EFI legacy boot mode.</div>
                        <div>- <code>network_protocol</code> (str): The {@name NetworkProtocol} defines the valid network boot protocols supported when booting a virtual machine with {@link Type#EFI} firmware over the network.</div>
                        <div>- Accepted values:</div>
                        <div>- IPV4</div>
                        <div>- IPV6</div>
                        <div>- <code>delay</code> (int): Delay in milliseconds before beginning the firmware boot process when the virtual machine is powered on.  This delay may be used to provide a time window for users to connect to the virtual machine console and enter BIOS setup mode.</div>
                        <div>- <code>retry</code> (bool): Flag indicating whether the virtual machine should automatically retry the boot process after a failure.</div>
                        <div>- <code>retry_delay</code> (int): Delay in milliseconds before retrying the boot process after a failure; applicable only when {@link Info#retry} is true.</div>
                        <div>- <code>enter_setup_mode</code> (bool): Flag indicating whether the firmware boot process should automatically enter setup mode the next time the virtual machine boots.  Note that this flag will automatically be reset to false once the virtual machine enters setup mode.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>boot_devices</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Boot device configuration.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name Type} defines the valid device types that may be used as bootable devices.</div>
                        <div>This key is required.</div>
                        <div>- Accepted values:</div>
                        <div>- CDROM</div>
                        <div>- DISK</div>
                        <div>- ETHERNET</div>
                        <div>- FLOPPY</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>cdroms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of CD-ROMs.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name HostBusAdapterType} defines the valid types of host bus adapters that may be used for attaching a Cdrom to a virtual machine.</div>
                        <div>- Accepted values:</div>
                        <div>- IDE</div>
                        <div>- SATA</div>
                        <div>- <code>ide</code> (dict): Address for attaching the device to a virtual IDE adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- primary (boolean): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>- master (boolean): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>- <code>sata</code> (dict): Address for attaching the device to a virtual SATA adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual CD-ROM device.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual CD-ROM device.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>ISO_FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>CLIENT_DEVICE</code></div>
                        <div>- iso_file (string): Path of the image file that should be used as the virtual CD-ROM device backing.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual CD-ROM device backing.</div>
                        <div>- device_access_type (string): The {@name DeviceAccessType} defines the valid device access types for a physical device packing of a virtual CD-ROM device.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>EMULATION</code></div>
                        <div>- <code>PASSTHRU</code></div>
                        <div>- <code>PASSTHRU_EXCLUSIVE</code></div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>count</code> (int): New number of CPU cores.  The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket. The supported range of CPU counts is constrained by the configured guest operating system and virtual hardware version of the virtual machine. If the virtual machine is running, the number of CPU cores may only be increased if {@link Info#hotAddEnabled} is true, and may only be decreased if {@link Info#hotRemoveEnabled} is true.</div>
                        <div>- <code>cores_per_socket</code> (int): New number of CPU cores per socket.  The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket.</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding CPUs while the virtual machine is running is enabled. This field may only be modified if the virtual machine is powered off.</div>
                        <div>- <code>hot_remove_enabled</code> (bool): Flag indicating whether removing CPUs while the virtual machine is running is enabled. This field may only be modified if the virtual machine is powered off.</div>
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
                        <div>Datastore path for the virtual machine&#x27;s configuration file in the format &quot;[datastore name] path&quot;.  For example &quot;[storage1] Test-VM/Test-VM.vmx&quot;.</div>
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
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disks</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Individual disk relocation map.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name HostBusAdapterType} defines the valid types of host bus adapters that may be used for attaching a virtual storage device to a virtual machine.</div>
                        <div>- Accepted values:</div>
                        <div>- IDE</div>
                        <div>- SCSI</div>
                        <div>- SATA</div>
                        <div>- <code>ide</code> (dict): Address for attaching the device to a virtual IDE adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- primary (boolean): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>- master (boolean): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>- <code>scsi</code> (dict): Address for attaching the device to a virtual SCSI adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>- <code>sata</code> (dict): Address for attaching the device to a virtual SATA adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>- <code>backing</code> (dict): Existing physical resource backing for the virtual disk. Exactly one of {@name #backing} or {@name #newVmdk} must be specified.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual disk.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>VMDK_FILE</code></div>
                        <div>- vmdk_file (string): Path of the VMDK file backing the virtual disk.</div>
                        <div>- <code>new_vmdk</code> (dict): Specification for creating a new VMDK backing for the virtual disk.  Exactly one of {@name #backing} or {@name #newVmdk} must be specified.</div>
                        <div>- Accepted keys:</div>
                        <div>- name (string): Base name of the VMDK file.  The name should not include the &#x27;.vmdk&#x27; file extension.</div>
                        <div>- capacity (integer): Capacity of the virtual disk backing in bytes.</div>
                        <div>- storage_policy (object): The {@name StoragePolicySpec} {@term structure} contains information about the storage policy that is to be associated the with VMDK file.</div>
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
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>disks_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of Disks to Update.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>floppies</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of floppy drives.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual floppy drive.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual floppy drive.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>IMAGE_FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>CLIENT_DEVICE</code></div>
                        <div>- image_file (string): Path of the image file that should be used as the virtual floppy drive backing.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual floppy drive backing.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Name of the customization specification.</div>
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
                                    <li>AMAZONLINUX3_64</li>
                                    <li>ASIANUX_3</li>
                                    <li>ASIANUX_3_64</li>
                                    <li>ASIANUX_4</li>
                                    <li>ASIANUX_4_64</li>
                                    <li>ASIANUX_5_64</li>
                                    <li>ASIANUX_7_64</li>
                                    <li>ASIANUX_8_64</li>
                                    <li>ASIANUX_9_64</li>
                                    <li>CENTOS</li>
                                    <li>CENTOS_6</li>
                                    <li>CENTOS_64</li>
                                    <li>CENTOS_6_64</li>
                                    <li>CENTOS_7</li>
                                    <li>CENTOS_7_64</li>
                                    <li>CENTOS_8_64</li>
                                    <li>CENTOS_9_64</li>
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
                                    <li>DARWIN_20_64</li>
                                    <li>DARWIN_21_64</li>
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
                                    <li>FREEBSD_13</li>
                                    <li>FREEBSD_13_64</li>
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
                                    <li>ORACLE_LINUX_9_64</li>
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
                                    <li>OTHER_5X_LINUX</li>
                                    <li>OTHER_5X_LINUX_64</li>
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
                                    <li>RHEL_9_64</li>
                                    <li>SJDS</li>
                                    <li>SLES</li>
                                    <li>SLES_10</li>
                                    <li>SLES_10_64</li>
                                    <li>SLES_11</li>
                                    <li>SLES_11_64</li>
                                    <li>SLES_12</li>
                                    <li>SLES_12_64</li>
                                    <li>SLES_15_64</li>
                                    <li>SLES_16_64</li>
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
                                    <li>WINDOWS_SERVER_2021</li>
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
                        <div>The {@name GuestOS} defines the valid guest operating system types used for configuring a virtual machine. Required with <em>state=[&#x27;present&#x27;]</em></div>
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
                                    <li>VMX_18</li>
                                    <li>VMX_19</li>
                        </ul>
                </td>
                <td>
                        <div>The {@name Version} defines the valid virtual hardware versions for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual machine hardware versions (1003746)).</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>size_MiB</code> (int): New memory size in mebibytes. The supported range of memory sizes is constrained by the configured guest operating system and virtual hardware version of the virtual machine. If the virtual machine is running, this value may only be changed if {@link Info#hotAddEnabled} is true, and the new memory size must satisfy the constraints specified by {@link Info#hotAddIncrementSizeMiB} and {@link Info#hotAddLimitMiB}.</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding memory while the virtual machine is running should be enabled. Some guest operating systems may consume more resources or perform less efficiently when they run on hardware that supports adding memory while the machine is running. This field may only be modified if the virtual machine is not powered on.</div>
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
                        <div>Name of the new virtual machine.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nics</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of Ethernet adapters.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name EmulationType} defines the valid emulation types for a virtual Ethernet adapter.</div>
                        <div>- Accepted values:</div>
                        <div>- E1000</div>
                        <div>- E1000E</div>
                        <div>- PCNET32</div>
                        <div>- VMXNET</div>
                        <div>- VMXNET2</div>
                        <div>- VMXNET3</div>
                        <div>- <code>upt_compatibility_enabled</code> (bool): Flag indicating whether Universal Pass-Through (UPT) compatibility is enabled on this virtual Ethernet adapter.</div>
                        <div>- <code>mac_type</code> (str): The {@name MacAddressType} defines the valid MAC address origins for a virtual Ethernet adapter.</div>
                        <div>- Accepted values:</div>
                        <div>- MANUAL</div>
                        <div>- GENERATED</div>
                        <div>- ASSIGNED</div>
                        <div>- <code>mac_address</code> (str): MAC address.</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the virtual Ethernet adapter on the PCI bus.  If the PCI address is invalid, the server will change when it the VM is started or as the device is hot added.</div>
                        <div>- <code>wake_on_lan_enabled</code> (bool): Flag indicating whether wake-on-LAN is enabled on this virtual Ethernet adapter.</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual Ethernet adapter.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual Ethernet adapter.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>STANDARD_PORTGROUP</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>DISTRIBUTED_PORTGROUP</code></div>
                        <div>- <code>OPAQUE_NETWORK</code></div>
                        <div>- network (string): Identifier of the network that backs the virtual Ethernet adapter.</div>
                        <div>- distributed_port (string): Key of the distributed virtual port that backs the virtual Ethernet adapter.  Depending on the type of the Portgroup, the port may be specified using this field. If the portgroup type is early-binding (also known as static), a port is assigned when the Ethernet adapter is configured to use the port. The port may be either automatically or specifically assigned based on the value of this field. If the portgroup type is ephemeral, the port is created and assigned to a virtual machine when it is powered on and the Ethernet adapter is connected.  This field cannot be specified as no free ports exist before use.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nics_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of NICs to update.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parallel_ports</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of parallel ports.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual parallel port.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual parallel port.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- file (string): Path of the file that should be used as the virtual parallel port backing.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual parallel port backing.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>parallel_ports_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of parallel ports to Update.</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>folder</code> (str): Virtual machine folder into which the virtual machine should be placed.</div>
                        <div>- <code>resource_pool</code> (str): Resource pool into which the virtual machine should be placed.</div>
                        <div>- <code>host</code> (str): Host onto which the virtual machine should be placed. If {@name #host} and {@name #resourcePool} are both specified, {@name #resourcePool} must belong to {@name #host}. If {@name #host} and {@name #cluster} are both specified, {@name #host} must be a member of {@name #cluster}.</div>
                        <div>- <code>cluster</code> (str): Cluster into which the virtual machine should be placed. If {@name #cluster} and {@name #resourcePool} are both specified, {@name #resourcePool} must belong to {@name #cluster}. If {@name #cluster} and {@name #host} are both specified, {@name #host} must be a member of {@name #cluster}.</div>
                        <div>- <code>datastore</code> (str): Datastore on which the virtual machine&#x27;s configuration state should be stored.  This datastore will also be used for any virtual disks that are created as part of the virtual machine creation operation.</div>
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
                        <div>Attempt to perform a {@link #powerOn} after clone.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>sata_adapters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SATA adapters.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name Type} defines the valid emulation types for a virtual SATA adapter.</div>
                        <div>- Accepted values:</div>
                        <div>- AHCI</div>
                        <div>- <code>bus</code> (int): SATA bus number.</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the SATA adapter on the PCI bus.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scsi_adapters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SCSI adapters.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): The {@name Type} defines the valid emulation types for a virtual SCSI adapter.</div>
                        <div>- Accepted values:</div>
                        <div>- BUSLOGIC</div>
                        <div>- LSILOGIC</div>
                        <div>- LSILOGICSAS</div>
                        <div>- PVSCSI</div>
                        <div>- <code>bus</code> (int): SCSI bus number.</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the SCSI adapter on the PCI bus.  If the PCI address is invalid, the server will change it when the VM is started or as the device is hot added.</div>
                        <div>- <code>sharing</code> (str): The {@name Sharing} defines the valid bus sharing modes for a virtual SCSI adapter.</div>
                        <div>- Accepted values:</div>
                        <div>- NONE</div>
                        <div>- VIRTUAL</div>
                        <div>- PHYSICAL</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_ports</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of serial ports.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>yield_on_poll</code> (bool): CPU yield behavior. If set to true, the virtual machine will periodically relinquish the processor if its sole task is polling the virtual serial port. The amount of time it takes to regain the processor will depend on the degree of other virtual machine activity on the host.</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual serial port.</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): The {@name BackingType} defines the valid backing types for a virtual serial port.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>PIPE_SERVER</code></div>
                        <div>- <code>PIPE_CLIENT</code></div>
                        <div>- <code>NETWORK_SERVER</code></div>
                        <div>- <code>NETWORK_CLIENT</code></div>
                        <div>- file (string): Path of the file backing the virtual serial port.</div>
                        <div>- host_device (string): Name of the device backing the virtual serial port. &lt;p&gt;</div>
                        <div>- pipe (string): Name of the pipe backing the virtual serial port.</div>
                        <div>- no_rx_loss (boolean): Flag that enables optimized data transfer over the pipe. When the value is true, the host buffers data to prevent data overrun.  This allows the virtual machine to read all of the data transferred over the pipe with no data loss.</div>
                        <div>- network_location (string): URI specifying the location of the network service backing the virtual serial port. &lt;ul&gt; &lt;li&gt;If {@link #type} is {@link BackingType#NETWORK_SERVER}, this field is the location used by clients to connect to this server.  The hostname part of the URI should either be empty or should specify the address of the host on which the virtual machine is running.&lt;/li&gt; &lt;li&gt;If {@link #type} is {@link BackingType#NETWORK_CLIENT}, this field is the location used by the virtual machine to connect to the remote server.&lt;/li&gt; &lt;/ul&gt;</div>
                        <div>- proxy (string): Proxy service that provides network access to the network backing.  If set, the virtual machine initiates a connection with the proxy service and forwards the traffic to the proxy.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>serial_ports_to_update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Map of serial ports to Update.</div>
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
                        <div>Virtual machine to InstantClone from. Required with <em>state=[&#x27;clone&#x27;, &#x27;instant_clone&#x27;]</em></div>
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
                                    <li><div style="color: blue"><b>present</b>&nbsp;&larr;</div></li>
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
                        <div>The {@name StoragePolicySpec} {@term structure} contains information about the storage policy that is to be associated with the virtual machine home (which contains the configuration and log files). Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>policy</code> (str): Identifier of the storage policy which should be associated with the virtual machine.</div>
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
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Identifier of the virtual machine to be unregistered. Required with <em>state=[&#x27;absent&#x27;, &#x27;relocate&#x27;, &#x27;unregister&#x27;]</em></div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Collect the list of the existing VM
      vmware.vmware_rest.vcenter_vm_info:
      register: existing_vms
      until: existing_vms is not failed

    - name: Delete some VM
      vmware.vmware_rest.vcenter_vm:
        state: absent
        vm: '{{ item.vm }}'
      with_items: '{{ existing_vms.value }}'

    - name: Build a list of all the clusters
      vmware.vmware_rest.vcenter_cluster_info:
      register: all_the_clusters

    - name: Retrieve details about the first cluster
      vmware.vmware_rest.vcenter_cluster_info:
        cluster: '{{ all_the_clusters.value[0].cluster }}'
      register: my_cluster_info

    - name: Build a list of all the folders with the type VIRTUAL_MACHINE and called vm
      vmware.vmware_rest.vcenter_folder_info:
        filter_type: VIRTUAL_MACHINE
        filter_names:
        - vm
      register: my_folders

    - name: Set my_virtual_machine_folder
      set_fact:
        my_virtual_machine_folder: '{{ my_folders.value|first }}'

    - name: We can also use filter to limit the number of result
      vmware.vmware_rest.vcenter_datastore_info:
        filter_names:
        - rw_datastore
      register: my_datastores

    - name: Set my_datastore
      set_fact:
        my_datastore: '{{ my_datastores.value|first }}'

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: '{{ my_cluster_info.id }}'
          datastore: '{{ my_datastore.datastore }}'
          folder: '{{ my_virtual_machine_folder.folder }}'
          resource_pool: '{{ my_cluster_info.value.resource_pool }}'
        name: test_vm1
        guest_OS: DEBIAN_8_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
      register: my_vm



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
                            <div>Delete some VM</div>
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
                            <div>Delete some VM</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;_ansible_item_label&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 128, &#x27;name&#x27;: &#x27;vCLS (1)&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1103&#x27;}, &#x27;_ansible_no_log&#x27;: 0, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 1, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;bios_uuid&#x27;: None, &#x27;boot&#x27;: None, &#x27;boot_devices&#x27;: None, &#x27;cdroms&#x27;: None, &#x27;cpu&#x27;: None, &#x27;datastore&#x27;: None, &#x27;datastore_path&#x27;: None, &#x27;disconnect_all_nics&#x27;: None, &#x27;disks&#x27;: None, &#x27;disks_to_remove&#x27;: None, &#x27;disks_to_update&#x27;: None, &#x27;floppies&#x27;: None, &#x27;guest_OS&#x27;: None, &#x27;guest_customization_spec&#x27;: None, &#x27;hardware_version&#x27;: None, &#x27;memory&#x27;: None, &#x27;name&#x27;: None, &#x27;nics&#x27;: None, &#x27;nics_to_update&#x27;: None, &#x27;parallel_ports&#x27;: None, &#x27;parallel_ports_to_update&#x27;: None, &#x27;path&#x27;: None, &#x27;placement&#x27;: None, &#x27;power_on&#x27;: None, &#x27;sata_adapters&#x27;: None, &#x27;scsi_adapters&#x27;: None, &#x27;serial_ports&#x27;: None, &#x27;serial_ports_to_update&#x27;: None, &#x27;source&#x27;: None, &#x27;state&#x27;: &#x27;absent&#x27;, &#x27;storage_policy&#x27;: None, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: None, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;vm&#x27;: &#x27;vm-1103&#x27;}}, &#x27;item&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 128, &#x27;name&#x27;: &#x27;vCLS (1)&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1103&#x27;}, &#x27;value&#x27;: {}}, {&#x27;_ansible_item_label&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1080, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;, &#x27;vm&#x27;: &#x27;vm-1107&#x27;}, &#x27;_ansible_no_log&#x27;: 0, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 1, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;bios_uuid&#x27;: None, &#x27;boot&#x27;: None, &#x27;boot_devices&#x27;: None, &#x27;cdroms&#x27;: None, &#x27;cpu&#x27;: None, &#x27;datastore&#x27;: None, &#x27;datastore_path&#x27;: None, &#x27;disconnect_all_nics&#x27;: None, &#x27;disks&#x27;: None, &#x27;disks_to_remove&#x27;: None, &#x27;disks_to_update&#x27;: None, &#x27;floppies&#x27;: None, &#x27;guest_OS&#x27;: None, &#x27;guest_customization_spec&#x27;: None, &#x27;hardware_version&#x27;: None, &#x27;memory&#x27;: None, &#x27;name&#x27;: None, &#x27;nics&#x27;: None, &#x27;nics_to_update&#x27;: None, &#x27;parallel_ports&#x27;: None, &#x27;parallel_ports_to_update&#x27;: None, &#x27;path&#x27;: None, &#x27;placement&#x27;: None, &#x27;power_on&#x27;: None, &#x27;sata_adapters&#x27;: None, &#x27;scsi_adapters&#x27;: None, &#x27;serial_ports&#x27;: None, &#x27;serial_ports_to_update&#x27;: None, &#x27;source&#x27;: None, &#x27;state&#x27;: &#x27;absent&#x27;, &#x27;storage_policy&#x27;: None, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: None, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;vm&#x27;: &#x27;vm-1107&#x27;}}, &#x27;item&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1080, &#x27;name&#x27;: &#x27;test_vm1&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;, &#x27;vm&#x27;: &#x27;vm-1107&#x27;}, &#x27;value&#x27;: {}}, {&#x27;_ansible_item_label&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1024, &#x27;name&#x27;: &#x27;my_vm_from_ovf&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1108&#x27;}, &#x27;_ansible_no_log&#x27;: 0, &#x27;ansible_loop_var&#x27;: &#x27;item&#x27;, &#x27;changed&#x27;: 1, &#x27;failed&#x27;: 0, &#x27;invocation&#x27;: {&#x27;module_args&#x27;: {&#x27;bios_uuid&#x27;: None, &#x27;boot&#x27;: None, &#x27;boot_devices&#x27;: None, &#x27;cdroms&#x27;: None, &#x27;cpu&#x27;: None, &#x27;datastore&#x27;: None, &#x27;datastore_path&#x27;: None, &#x27;disconnect_all_nics&#x27;: None, &#x27;disks&#x27;: None, &#x27;disks_to_remove&#x27;: None, &#x27;disks_to_update&#x27;: None, &#x27;floppies&#x27;: None, &#x27;guest_OS&#x27;: None, &#x27;guest_customization_spec&#x27;: None, &#x27;hardware_version&#x27;: None, &#x27;memory&#x27;: None, &#x27;name&#x27;: None, &#x27;nics&#x27;: None, &#x27;nics_to_update&#x27;: None, &#x27;parallel_ports&#x27;: None, &#x27;parallel_ports_to_update&#x27;: None, &#x27;path&#x27;: None, &#x27;placement&#x27;: None, &#x27;power_on&#x27;: None, &#x27;sata_adapters&#x27;: None, &#x27;scsi_adapters&#x27;: None, &#x27;serial_ports&#x27;: None, &#x27;serial_ports_to_update&#x27;: None, &#x27;source&#x27;: None, &#x27;state&#x27;: &#x27;absent&#x27;, &#x27;storage_policy&#x27;: None, &#x27;vcenter_hostname&#x27;: &#x27;vcenter.test&#x27;, &#x27;vcenter_password&#x27;: &#x27;VALUE_SPECIFIED_IN_NO_LOG_PARAMETER&#x27;, &#x27;vcenter_rest_log_file&#x27;: None, &#x27;vcenter_username&#x27;: &#x27;administrator@vsphere.local&#x27;, &#x27;vcenter_validate_certs&#x27;: 0, &#x27;vm&#x27;: &#x27;vm-1108&#x27;}}, &#x27;item&#x27;: {&#x27;cpu_count&#x27;: 1, &#x27;memory_size_MiB&#x27;: 1024, &#x27;name&#x27;: &#x27;my_vm_from_ovf&#x27;, &#x27;power_state&#x27;: &#x27;POWERED_OFF&#x27;, &#x27;vm&#x27;: &#x27;vm-1108&#x27;}, &#x27;value&#x27;: {}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
