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
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid firmware types for a virtual machine. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- BIOS</div>
                        <div>- EFI</div>
                        <div>- <code>efi_legacy_boot</code> (bool): Flag indicating whether to use EFI legacy boot mode.</div>
                        <div>If unset, defaults to value that is recommended for the guest OS and is supported for the virtual hardware version. ([&#x27;present&#x27;])</div>
                        <div>- <code>network_protocol</code> (str): This option defines the valid network boot protocols supported when booting a virtual machine with EFI firmware over the network. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- IPV4</div>
                        <div>- IPV6</div>
                        <div>- <code>delay</code> (int): Delay in milliseconds before beginning the firmware boot process when the virtual machine is powered on. This delay may be used to provide a time window for users to connect to the virtual machine console and enter BIOS setup mode.</div>
                        <div>If unset, default value is 0. ([&#x27;present&#x27;])</div>
                        <div>- <code>retry</code> (bool): Flag indicating whether the virtual machine should automatically retry the boot process after a failure.</div>
                        <div>If unset, default value is false. ([&#x27;present&#x27;])</div>
                        <div>- <code>retry_delay</code> (int): Delay in milliseconds before retrying the boot process after a failure; applicable only when <em>retry</em> is true.</div>
                        <div>If unset, default value is 10000. ([&#x27;present&#x27;])</div>
                        <div>- <code>enter_setup_mode</code> (bool): Flag indicating whether the firmware boot process should automatically enter setup mode the next time the virtual machine boots. Note that this flag will automatically be reset to false once the virtual machine enters setup mode.</div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, a server-specific boot sequence will be used.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid device types that may be used as bootable devices. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
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
                        <div>If unset, no CD-ROM devices will be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid types of host bus adapters that may be used for attaching a Cdrom to a virtual machine. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- IDE</div>
                        <div>- SATA</div>
                        <div>- <code>ide</code> (dict): Address for attaching the device to a virtual IDE adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- primary (boolean): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>If unset, the server will choose a adapter with an available connection. If no IDE connections are available, the request will be rejected.</div>
                        <div>- master (boolean): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>If unset, the server will choose an available connection type. If no IDE connections are available, the request will be rejected.</div>
                        <div>- <code>sata</code> (dict): Address for attaching the device to a virtual SATA adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual CD-ROM device.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual CD-ROM device.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>CLIENT_DEVICE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>ISO_FILE</code></div>
                        <div>- iso_file (string): Path of the image file that should be used as the virtual CD-ROM device backing.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is ISO_FILE.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual CD-ROM device backing.</div>
                        <div>If unset, the virtual CD-ROM device will be configured to automatically detect a suitable host device.</div>
                        <div>- device_access_type (string): This option defines the valid device access types for a physical device packing of a virtual CD-ROM device.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>EMULATION</code></div>
                        <div>- <code>PASSTHRU</code></div>
                        <div>- <code>PASSTHRU_EXCLUSIVE</code></div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>count</code> (int): New number of CPU cores. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket.</div>
                        <div>The supported range of CPU counts is constrained by the configured guest operating system and virtual hardware version of the virtual machine.</div>
                        <div></div>
                        <div>If the virtual machine is running, the number of CPU cores may only be increased if <em>hot_add_enabled</em> is true, and may only be decreased if <em>hot_remove_enabled</em> is true.</div>
                        <div></div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
                        <div>- <code>cores_per_socket</code> (int): New number of CPU cores per socket. The number of CPU cores in the virtual machine must be a multiple of the number of cores per socket.</div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding CPUs while the virtual machine is running is enabled.</div>
                        <div>This field may only be modified if the virtual machine is powered off.</div>
                        <div></div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
                        <div>- <code>hot_remove_enabled</code> (bool): Flag indicating whether removing CPUs while the virtual machine is running is enabled.</div>
                        <div>This field may only be modified if the virtual machine is powered off.</div>
                        <div></div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, <em>path</em> must also be unset and <em>datastore_path</em> must be set.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_datastore_info</span>.</div>
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
                        <div>If unset, both <em>datastore</em> and <em>path</em> must be set.</div>
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
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Individual disk relocation map.</div>
                        <div>If unset, all disks will migrate to the datastore specified in the <em>datastore</em> field of I()</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_disk</span>.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid types of host bus adapters that may be used for attaching a virtual storage device to a virtual machine. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- IDE</div>
                        <div>- NVME</div>
                        <div>- SATA</div>
                        <div>- SCSI</div>
                        <div>- <code>ide</code> (dict): Address for attaching the device to a virtual IDE adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- primary (boolean): Flag specifying whether the device should be attached to the primary or secondary IDE adapter of the virtual machine.</div>
                        <div>If unset, the server will choose a adapter with an available connection. If no IDE connections are available, the request will be rejected.</div>
                        <div>- master (boolean): Flag specifying whether the device should be the master or slave device on the IDE adapter.</div>
                        <div>If unset, the server will choose an available connection type. If no IDE connections are available, the request will be rejected.</div>
                        <div>- <code>scsi</code> (dict): Address for attaching the device to a virtual SCSI adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                        <div>- <code>sata</code> (dict): Address for attaching the device to a virtual SATA adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                        <div>- <code>nvme</code> (dict): Address for attaching the device to a virtual NVMe adapter.</div>
                        <div>If unset, the server will choose an available address; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- bus (integer): Bus number of the adapter to which the device should be attached.</div>
                        <div>- unit (integer): Unit number of the device.</div>
                        <div>If unset, the server will choose an available unit number on the specified adapter. If there are no available connections on the adapter, the request will be rejected.</div>
                        <div>- <code>backing</code> (dict): Existing physical resource backing for the virtual disk. Exactly one of <em>backing</em> or <em>new_vmdk</em> must be specified.</div>
                        <div>If unset, the virtual disk will not be connected to an existing backing. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual disk.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>VMDK_FILE</code></div>
                        <div>- vmdk_file (string): Path of the VMDK file backing the virtual disk.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is VMDK_FILE.</div>
                        <div>- <code>new_vmdk</code> (dict): Specification for creating a new VMDK backing for the virtual disk. Exactly one of <em>backing</em> or <em>new_vmdk</em> must be specified.</div>
                        <div>If unset, a new VMDK backing will not be created. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- name (string): Base name of the VMDK file. The name should not include the &#x27;.vmdk&#x27; file extension.</div>
                        <div>If unset, a name (derived from the name of the virtual machine) will be chosen by the server.</div>
                        <div>- capacity (integer): Capacity of the virtual disk backing in bytes.</div>
                        <div>If unset, defaults to a guest-specific capacity.</div>
                        <div>- storage_policy (object): The <em>storage_policy_spec</em> structure contains information about the storage policy that is to be associated the with VMDK file.</div>
                        <div>If unset the default storage policy of the target datastore (if applicable) is applied. Currently a default storage policy is only supported by object based datastores : VVol &amp; vSAN. For non- object datastores, if unset then no storage policy would be associated with the VMDK file.</div>
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
                        <div>If unset, all disks will be copied. If the same identifier is in <em>disks_to_update</em> InvalidArgument fault will be returned.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_disk</span>.</div>
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
                        <div>If unset, all disks will copied to the datastore specified in the <em>datastore</em> field of I() If the same identifier is in <em>disks_to_remove</em> InvalidArgument fault will be thrown.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_disk</span>.</div>
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
                        <div>If unset, no floppy drives will be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual floppy drive.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual floppy drive.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>CLIENT_DEVICE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>IMAGE_FILE</code></div>
                        <div>- image_file (string): Path of the image file that should be used as the virtual floppy drive backing.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is IMAGE_FILE.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual floppy drive backing.</div>
                        <div>If unset, the virtual floppy drive will be configured to automatically detect a suitable host device.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>name</code> (str): Name of the customization specification.</div>
                        <div>If unset, no guest customization is performed. ([&#x27;clone&#x27;])</div>
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
                        <div>The GuestOS enumerated type defines the valid guest operating system types used for configuring a virtual machine. Required with <em>state=[&#x27;present&#x27;]</em></div>
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
                        <div>The <em>version</em> enumerated type defines the valid virtual hardware versions for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual machine hardware versions (1003746)).</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>size_MiB</code> (int): New memory size in mebibytes.</div>
                        <div>The supported range of memory sizes is constrained by the configured guest operating system and virtual hardware version of the virtual machine.</div>
                        <div></div>
                        <div>If the virtual machine is running, this value may only be changed if <em>hot_add_enabled</em> is true, and the new memory size must satisfy the constraints specified by <em>hot_add_increment_size_mib</em> and I()</div>
                        <div></div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
                        <div>- <code>hot_add_enabled</code> (bool): Flag indicating whether adding memory while the virtual machine is running should be enabled.</div>
                        <div>Some guest operating systems may consume more resources or perform less efficiently when they run on hardware that supports adding memory while the machine is running.</div>
                        <div></div>
                        <div>This field may only be modified if the virtual machine is not powered on.</div>
                        <div></div>
                        <div>If unset, the value is unchanged. ([&#x27;present&#x27;])</div>
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
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of Ethernet adapters.</div>
                        <div>If unset, no Ethernet adapters will be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid emulation types for a virtual Ethernet adapter. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- E1000</div>
                        <div>- E1000E</div>
                        <div>- PCNET32</div>
                        <div>- VMXNET</div>
                        <div>- VMXNET2</div>
                        <div>- VMXNET3</div>
                        <div>- <code>upt_compatibility_enabled</code> (bool): Flag indicating whether Universal Pass-Through (UPT) compatibility is enabled on this virtual Ethernet adapter.</div>
                        <div>If unset, defaults to false. ([&#x27;present&#x27;])</div>
                        <div>- <code>mac_type</code> (str): This option defines the valid MAC address origins for a virtual Ethernet adapter. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- ASSIGNED</div>
                        <div>- GENERATED</div>
                        <div>- MANUAL</div>
                        <div>- <code>mac_address</code> (str): MAC address.</div>
                        <div>Workaround for PR1459647 ([&#x27;present&#x27;])</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the virtual Ethernet adapter on the PCI bus. If the PCI address is invalid, the server will change when it the VM is started or as the device is hot added.</div>
                        <div>If unset, the server will choose an available address when the virtual machine is powered on. ([&#x27;present&#x27;])</div>
                        <div>- <code>wake_on_lan_enabled</code> (bool): Flag indicating whether wake-on-LAN is enabled on this virtual Ethernet adapter.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual Ethernet adapter.</div>
                        <div>If unset, the system may try to find an appropriate backing. If one is not found, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual Ethernet adapter.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>DISTRIBUTED_PORTGROUP</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>OPAQUE_NETWORK</code></div>
                        <div>- <code>STANDARD_PORTGROUP</code></div>
                        <div>- network (string): Identifier of the network that backs the virtual Ethernet adapter.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is one of STANDARD_PORTGROUP, DISTRIBUTED_PORTGROUP, or OPAQUE_NETWORK.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_network_info</span>.</div>
                        <div>- distributed_port (string): Key of the distributed virtual port that backs the virtual Ethernet adapter. Depending on the type of the Portgroup, the port may be specified using this field. If the portgroup type is early-binding (also known as static), a port is assigned when the Ethernet adapter is configured to use the port. The port may be either automatically or specifically assigned based on the value of this field. If the portgroup type is ephemeral, the port is created and assigned to a virtual machine when it is powered on and the Ethernet adapter is connected. This field cannot be specified as no free ports exist before use.</div>
                        <div>May be used to specify a port when the network specified on the <em>network</em> field is a static or early binding distributed portgroup. If unset, the port will be automatically assigned to the Ethernet adapter based on the policy embodied by the portgroup type.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, no NICs will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_ethernet</span>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>nvme_adapters</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of NVMe adapters.</div>
                        <div>If unset, any adapters necessary to connect the virtual machine&#x27;s storage devices will be created; this includes any devices that explicitly specify a NVMe host bus adapter, as well as any devices that do not specify a host bus adapter if the guest&#x27;s preferred adapter type is NVMe.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>bus</code> (int): NVMe bus number.</div>
                        <div>If unset, the server will choose an available bus number; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the NVMe adapter on the PCI bus.</div>
                        <div>If unset, the server will choose an available address when the virtual machine is powered on. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, no parallel ports will be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual parallel port.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual parallel port.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- file (string): Path of the file that should be used as the virtual parallel port backing.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is FILE.</div>
                        <div>- host_device (string): Name of the device that should be used as the virtual parallel port backing.</div>
                        <div>If unset, the virtual parallel port will be configured to automatically detect a suitable host device.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, no parallel ports will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_parallel</span>.</div>
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
                        <div>If unset, <em>datastore</em> must also be unset and <em>datastore_path</em> must be set.</div>
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
                        <div>Valid attributes are:</div>
                        <div>- <code>folder</code> (str): Virtual machine folder into which the virtual machine should be placed.</div>
                        <div>If this field is unset, the virtual machine will stay in the current folder.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_folder_info</span>. ([&#x27;clone&#x27;, &#x27;instant_clone&#x27;, &#x27;present&#x27;, &#x27;register&#x27;, &#x27;relocate&#x27;])</div>
                        <div>- <code>resource_pool</code> (str): Resource pool into which the virtual machine should be placed.</div>
                        <div>If this field is unset, the virtual machine will stay in the current resource pool.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_resourcepool_info</span>. ([&#x27;clone&#x27;, &#x27;instant_clone&#x27;, &#x27;present&#x27;, &#x27;register&#x27;, &#x27;relocate&#x27;])</div>
                        <div>- <code>host</code> (str): Host onto which the virtual machine should be placed.</div>
                        <div>If <em>host</em> and <em>resource_pool</em> are both specified, <em>resource_pool</em> must belong to <em>host</em>.</div>
                        <div></div>
                        <div>If <em>host</em> and <em>cluster</em> are both specified, <em>host</em> must be a member of <em>cluster</em>.</div>
                        <div></div>
                        <div>If this field is unset, if <em>resource_pool</em> is unset, the virtual machine will remain on the current host. if <em>resource_pool</em> is set, and the target is a standalone host, the host is used. if <em>resource_pool</em> is set, and the target is a DRS cluster, a host will be picked by DRS. if <em>resource_pool</em> is set, and the target is a cluster without DRS, InvalidArgument will be thrown.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_host_info</span>. ([&#x27;clone&#x27;, &#x27;present&#x27;, &#x27;register&#x27;, &#x27;relocate&#x27;])</div>
                        <div>- <code>cluster</code> (str): Cluster into which the virtual machine should be placed.</div>
                        <div>If <em>cluster</em> and <em>resource_pool</em> are both specified, <em>resource_pool</em> must belong to <em>cluster</em>.</div>
                        <div></div>
                        <div>If <em>cluster</em> and <em>host</em> are both specified, <em>host</em> must be a member of <em>cluster</em>.</div>
                        <div></div>
                        <div>If <em>resource_pool</em> or <em>host</em> is specified, it is recommended that this field be unset.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_cluster_info</span>. ([&#x27;clone&#x27;, &#x27;present&#x27;, &#x27;register&#x27;, &#x27;relocate&#x27;])</div>
                        <div>- <code>datastore</code> (str): Datastore on which the virtual machine&#x27;s configuration state should be stored. This datastore will also be used for any virtual disks that are associated with the virtual machine, unless individually overridden.</div>
                        <div>If this field is unset, the virtual machine will remain on the current datastore.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_datastore_info</span>. ([&#x27;clone&#x27;, &#x27;instant_clone&#x27;, &#x27;present&#x27;, &#x27;relocate&#x27;])</div>
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
                        <div>Attempt to perform a <em>power_on</em> after clone.</div>
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
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of SATA adapters.</div>
                        <div>If unset, any adapters necessary to connect the virtual machine&#x27;s storage devices will be created; this includes any devices that explicitly specify a SATA host bus adapter, as well as any devices that do not specify a host bus adapter if the guest&#x27;s preferred adapter type is SATA.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid emulation types for a virtual SATA adapter. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- AHCI</div>
                        <div>- <code>bus</code> (int): SATA bus number.</div>
                        <div>If unset, the server will choose an available bus number; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the SATA adapter on the PCI bus.</div>
                        <div>If unset, the server will choose an available address when the virtual machine is powered on. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, any adapters necessary to connect the virtual machine&#x27;s storage devices will be created; this includes any devices that explicitly specify a SCSI host bus adapter, as well as any devices that do not specify a host bus adapter if the guest&#x27;s preferred adapter type is SCSI. The type of the SCSI adapter will be a guest-specific default type.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>type</code> (str): This option defines the valid emulation types for a virtual SCSI adapter. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- BUSLOGIC</div>
                        <div>- LSILOGIC</div>
                        <div>- LSILOGICSAS</div>
                        <div>- PVSCSI</div>
                        <div>- <code>bus</code> (int): SCSI bus number.</div>
                        <div>If unset, the server will choose an available bus number; if none is available, the request will fail. ([&#x27;present&#x27;])</div>
                        <div>- <code>pci_slot_number</code> (int): Address of the SCSI adapter on the PCI bus. If the PCI address is invalid, the server will change it when the VM is started or as the device is hot added.</div>
                        <div>If unset, the server will choose an available address when the virtual machine is powered on. ([&#x27;present&#x27;])</div>
                        <div>- <code>sharing</code> (str): This option defines the valid bus sharing modes for a virtual SCSI adapter. ([&#x27;present&#x27;])</div>
                        <div>- Accepted values:</div>
                        <div>- NONE</div>
                        <div>- PHYSICAL</div>
                        <div>- VIRTUAL</div>
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
                        <div>If unset, no serial ports will be created.</div>
                        <div>Valid attributes are:</div>
                        <div>- <code>yield_on_poll</code> (bool): CPU yield behavior. If set to true, the virtual machine will periodically relinquish the processor if its sole task is polling the virtual serial port. The amount of time it takes to regain the processor will depend on the degree of other virtual machine activity on the host.</div>
                        <div>If unset, defaults to false. ([&#x27;present&#x27;])</div>
                        <div>- <code>backing</code> (dict): Physical resource backing for the virtual serial port.</div>
                        <div>If unset, defaults to automatic detection of a suitable host device. ([&#x27;present&#x27;])</div>
                        <div>- Accepted keys:</div>
                        <div>- type (string): This option defines the valid backing types for a virtual serial port.</div>
                        <div>Accepted value for this field:</div>
                        <div>- <code>FILE</code></div>
                        <div>- <code>HOST_DEVICE</code></div>
                        <div>- <code>NETWORK_CLIENT</code></div>
                        <div>- <code>NETWORK_SERVER</code></div>
                        <div>- <code>PIPE_CLIENT</code></div>
                        <div>- <code>PIPE_SERVER</code></div>
                        <div>- file (string): Path of the file backing the virtual serial port.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is FILE.</div>
                        <div>- host_device (string): Name of the device backing the virtual serial port.</div>
                        <div></div>
                        <div></div>
                        <div>If unset, the virtual serial port will be configured to automatically detect a suitable host device.</div>
                        <div>- pipe (string): Name of the pipe backing the virtual serial port.</div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is one of PIPE_SERVER or PIPE_CLIENT.</div>
                        <div>- no_rx_loss (boolean): Flag that enables optimized data transfer over the pipe. When the value is true, the host buffers data to prevent data overrun. This allows the virtual machine to read all of the data transferred over the pipe with no data loss.</div>
                        <div>If unset, defaults to false.</div>
                        <div>- network_location (string): URI specifying the location of the network service backing the virtual serial port.</div>
                        <div>- If <em>type</em> is NETWORK_SERVER, this field is the location used by clients to connect to this server. The hostname part of the URI should either be empty or should specify the address of the host on which the virtual machine is running.</div>
                        <div>- If <em>type</em> is NETWORK_CLIENT, this field is the location used by the virtual machine to connect to the remote server.</div>
                        <div></div>
                        <div>This field is optional and it is only relevant when the value of <em>type</em> is one of NETWORK_SERVER or NETWORK_CLIENT.</div>
                        <div>- proxy (string): Proxy service that provides network access to the network backing. If set, the virtual machine initiates a connection with the proxy service and forwards the traffic to the proxy.</div>
                        <div>If unset, no proxy service should be used.</div>
                        <div>- <code>start_connected</code> (bool): Flag indicating whether the virtual device should be connected whenever the virtual machine is powered on.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
                        <div>- <code>allow_guest_control</code> (bool): Flag indicating whether the guest can connect and disconnect the device.</div>
                        <div>Defaults to false if unset. ([&#x27;present&#x27;])</div>
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
                        <div>If unset, no serial ports will be updated.</div>
                        <div>When clients pass a value of this structure as a parameter, the key in the field map must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_hardware_serial</span>.</div>
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
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_info</span>. Required with <em>state=[&#x27;clone&#x27;, &#x27;instant_clone&#x27;]</em></div>
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
                        <div>The <em>storage_policy_spec</em> structure contains information about the storage policy that is to be associated with the virtual machine home (which contains the configuration and log files).</div>
                        <div>If unset the datastore default storage policy (if applicable) is applied. Currently a default storage policy is only supported by object datastores : VVol and vSAN. For non-object datastores, if unset then no storage policy would be associated with the virtual machine home. Required with <em>state=[&#x27;present&#x27;]</em></div>
                        <div>Valid attributes are:</div>
                        <div>- <code>policy</code> (str): Identifier of the storage policy which should be associated with the virtual machine.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_storage_policies</span>. ([&#x27;present&#x27;])</div>
                        <div>This key is required with [&#x27;present&#x27;].</div>
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
                        <div>Identifier of the virtual machine to be unregistered.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vmware.vmware_rest.vcenter_vm_info</span>. Required with <em>state=[&#x27;absent&#x27;, &#x27;relocate&#x27;, &#x27;unregister&#x27;]</em></div>
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

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/rw_datastore') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        name: test_vm1
        guest_OS: RHEL_7_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
      register: my_vm

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        name: test_vm1
        guest_OS: RHEL_7_64
        hardware_version: VMX_11
        memory:
          hot_add_enabled: true
          size_MiB: 1024
        disks:
        - type: SATA
          backing:
            type: VMDK_FILE
            vmdk_file: '[local] test_vm1/{{ disk_name }}.vmdk'
        - type: SATA
          new_vmdk:
            name: second_disk
            capacity: 32000000000
        cdroms:
        - type: SATA
          sata:
            bus: 0
            unit: 2
        nics:
        - backing:
            type: STANDARD_PORTGROUP
            network: "{{ lookup('vmware.vmware_rest.network_moid', '/my_dc/network/VM Network') }}"
      register: my_vm

    - name: Create a content library based on a DataStore
      vmware.vmware_rest.content_locallibrary:
        name: my_library_on_datastore
        description: automated
        publish_info:
          published: true
          authentication_method: NONE
        storage_backings:
        - datastore_id: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          type: DATASTORE
        state: present
      register: nfs_lib

    - name: Get the list of items of the NFS library
      vmware.vmware_rest.content_library_item_info:
        library_id: '{{ nfs_lib.id }}'
      register: lib_items

    - name: Use the name to identify the item
      set_fact:
        my_template_item: "{{ lib_items.value | selectattr('name', 'equalto', 'golden-template')|first }}"

    - name: Deploy a new VM based on the template
      vmware.vmware_rest.vcenter_vmtemplate_libraryitems:
        name: vm-from-template
        library: '{{ nfs_lib.id }}'
        template_library_item: '{{ my_template_item.id }}'
        placement:
          cluster: "{{ lookup('vmware.vmware_rest.cluster_moid', '/my_dc/host/my_cluster') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        state: deploy
      register: my_new_vm

    - name: Retrieve all the details about the new VM
      vmware.vmware_rest.vcenter_vm:
        vm: '{{ my_new_vm.value }}'
      register: my_new_vm_info

    - name: Create an instant clone of a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        source: '{{ my_vm.id }}'
        name: test_vm2
        state: instant_clone
      register: my_instant_clone

    - name: Create a clone of a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: "{{ lookup('vmware.vmware_rest.folder_moid', '/my_dc/vm') }}"
          resource_pool: "{{ lookup('vmware.vmware_rest.resource_pool_moid', '/my_dc/host/my_cluster/Resources') }}"
        source: '{{ my_vm.id }}'
        name: test_vm3
        state: clone
      register: my_clone_vm

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
      ansible.builtin.set_fact:
        my_virtual_machine_folder: '{{ my_folders.value|first }}'

    - name: Create a VM
      vmware.vmware_rest.vcenter_vm:
        placement:
          cluster: '{{ my_cluster_info.id }}'
          datastore: "{{ lookup('vmware.vmware_rest.datastore_moid', '/my_dc/datastore/local') }}"
          folder: '{{ my_virtual_machine_folder.folder }}'
          resource_pool: '{{ my_cluster_info.value.resource_pool }}'
        name: test_vm1
        guest_OS: DEBIAN_7_64
        hardware_version: VMX_10
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">vm-1104</div>
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
                            <div>Create an instant clone of a VM</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;boot&#x27;: {&#x27;delay&#x27;: 0, &#x27;enter_setup_mode&#x27;: 0, &#x27;retry&#x27;: 0, &#x27;retry_delay&#x27;: 10000, &#x27;type&#x27;: &#x27;BIOS&#x27;}, &#x27;boot_devices&#x27;: [], &#x27;cdroms&#x27;: {&#x27;16002&#x27;: {&#x27;allow_guest_control&#x27;: 0, &#x27;backing&#x27;: {&#x27;auto_detect&#x27;: 1, &#x27;device_access_type&#x27;: &#x27;EMULATION&#x27;, &#x27;type&#x27;: &#x27;HOST_DEVICE&#x27;}, &#x27;label&#x27;: &#x27;CD/DVD drive 1&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 2}, &#x27;start_connected&#x27;: 0, &#x27;state&#x27;: &#x27;NOT_CONNECTED&#x27;, &#x27;type&#x27;: &#x27;SATA&#x27;}}, &#x27;cpu&#x27;: {&#x27;cores_per_socket&#x27;: 1, &#x27;count&#x27;: 1, &#x27;hot_add_enabled&#x27;: 0, &#x27;hot_remove_enabled&#x27;: 0}, &#x27;disks&#x27;: {&#x27;16000&#x27;: {&#x27;backing&#x27;: {&#x27;type&#x27;: &#x27;VMDK_FILE&#x27;, &#x27;vmdk_file&#x27;: &#x27;[local] test_vm2/test_vm2_2.vmdk&#x27;}, &#x27;capacity&#x27;: 16106127360, &#x27;label&#x27;: &#x27;Hard disk 1&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 0}, &#x27;type&#x27;: &#x27;SATA&#x27;}, &#x27;16001&#x27;: {&#x27;backing&#x27;: {&#x27;type&#x27;: &#x27;VMDK_FILE&#x27;, &#x27;vmdk_file&#x27;: &#x27;[local] test_vm2/test_vm2_1.vmdk&#x27;}, &#x27;capacity&#x27;: 32000000000, &#x27;label&#x27;: &#x27;Hard disk 2&#x27;, &#x27;sata&#x27;: {&#x27;bus&#x27;: 0, &#x27;unit&#x27;: 1}, &#x27;type&#x27;: &#x27;SATA&#x27;}}, &#x27;floppies&#x27;: {}, &#x27;guest_OS&#x27;: &#x27;RHEL_7_64&#x27;, &#x27;hardware&#x27;: {&#x27;upgrade_policy&#x27;: &#x27;NEVER&#x27;, &#x27;upgrade_status&#x27;: &#x27;NONE&#x27;, &#x27;version&#x27;: &#x27;VMX_11&#x27;}, &#x27;identity&#x27;: {&#x27;bios_uuid&#x27;: &#x27;4231bf8b-3cb4-3a3f-1bfb-18c857ce95b6&#x27;, &#x27;instance_uuid&#x27;: &#x27;5031b322-6030-a020-8e73-1a9ad0fd03ce&#x27;, &#x27;name&#x27;: &#x27;test_vm2&#x27;}, &#x27;instant_clone_frozen&#x27;: 0, &#x27;memory&#x27;: {&#x27;hot_add_enabled&#x27;: 1, &#x27;hot_add_increment_size_MiB&#x27;: 128, &#x27;hot_add_limit_MiB&#x27;: 3072, &#x27;size_MiB&#x27;: 1024}, &#x27;name&#x27;: &#x27;test_vm2&#x27;, &#x27;nics&#x27;: {&#x27;4000&#x27;: {&#x27;allow_guest_control&#x27;: 0, &#x27;backing&#x27;: {&#x27;network&#x27;: &#x27;network-1095&#x27;, &#x27;network_name&#x27;: &#x27;VM Network&#x27;, &#x27;type&#x27;: &#x27;STANDARD_PORTGROUP&#x27;}, &#x27;label&#x27;: &#x27;Network adapter 1&#x27;, &#x27;mac_address&#x27;: &#x27;00:50:56:b1:26:0c&#x27;, &#x27;mac_type&#x27;: &#x27;ASSIGNED&#x27;, &#x27;pci_slot_number&#x27;: 160, &#x27;start_connected&#x27;: 0, &#x27;state&#x27;: &#x27;NOT_CONNECTED&#x27;, &#x27;type&#x27;: &#x27;VMXNET3&#x27;, &#x27;upt_compatibility_enabled&#x27;: 0, &#x27;wake_on_lan_enabled&#x27;: 0}}, &#x27;nvme_adapters&#x27;: {}, &#x27;parallel_ports&#x27;: {}, &#x27;power_state&#x27;: &#x27;POWERED_ON&#x27;, &#x27;sata_adapters&#x27;: {&#x27;15000&#x27;: {&#x27;bus&#x27;: 0, &#x27;label&#x27;: &#x27;SATA controller 0&#x27;, &#x27;pci_slot_number&#x27;: 32, &#x27;type&#x27;: &#x27;AHCI&#x27;}}, &#x27;scsi_adapters&#x27;: {}, &#x27;serial_ports&#x27;: {}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
