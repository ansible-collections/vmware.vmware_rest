#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: DEFAULT_MODULE

DOCUMENTATION = """
module: vcenter_vm
short_description: Manage the vm of a vCenter
description: Manage the vm of a vCenter
options:
  bios_uuid:
    description:
    - 128-bit SMBIOS UUID of a virtual machine represented as a hexadecimal string
      in "12345678-abcd-1234-cdef-123456789abc" format.
    - If unset, will be generated.
    type: str
  boot:
    description:
    - Boot configuration.
    - If unset, guest-specific default values will be used.
    - 'Valide attributes are:'
    - ' - C(delay) (int): Delay in milliseconds before beginning the firmware boot
      process when the virtual machine is powered on. This delay may be used to provide
      a time window for users to connect to the virtual machine console and enter
      BIOS setup mode.'
    - If unset, default value is 0.
    - ' - C(efi_legacy_boot) (bool): Flag indicating whether to use EFI legacy boot
      mode.'
    - If unset, defaults to value that is recommended for the guest OS and is supported
      for the virtual hardware version.
    - ' - C(enter_setup_mode) (bool): Flag indicating whether the firmware boot process
      should automatically enter setup mode the next time the virtual machine boots.
      Note that this flag will automatically be reset to false once the virtual machine
      enters setup mode.'
    - If unset, the value is unchanged.
    - ' - C(network_protocol) (str): This option defines the valid network boot protocols
      supported when booting a virtual machine with EFI firmware over the network.'
    - '   - Accepted values:'
    - '     - IPV4'
    - '     - IPV6'
    - ' - C(retry) (bool): Flag indicating whether the virtual machine should automatically
      retry the boot process after a failure.'
    - If unset, default value is false.
    - ' - C(retry_delay) (int): Delay in milliseconds before retrying the boot process
      after a failure; applicable only when I(retry) is true.'
    - If unset, default value is 10000.
    - ' - C(type) (str): This option defines the valid firmware types for a virtual
      machine.'
    - '   - Accepted values:'
    - '     - BIOS'
    - '     - EFI'
    type: dict
  boot_devices:
    description:
    - Boot device configuration.
    - If unset, a server-specific boot sequence will be used.
    - 'Valide attributes are:'
    - ' - C(type) (str): This option defines the valid device types that may be used
      as bootable devices.'
    - '   - Accepted values:'
    - '     - CDROM'
    - '     - DISK'
    - '     - ETHERNET'
    - '     - FLOPPY'
    elements: dict
    type: list
  cdroms:
    description:
    - List of CD-ROMs.
    - If unset, no CD-ROM devices will be created.
    - 'Valide attributes are:'
    - ' - C(allow_guest_control) (bool): Flag indicating whether the guest can connect
      and disconnect the device.'
    - Defaults to false if unset.
    - ' - C(backing) (dict): Physical resource backing for the virtual CD-ROM device.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '   - Accepted keys:'
    - '     - device_access_type (string): This option defines the valid device access
      types for a physical device packing of a virtual CD-ROM device.'
    - 'Accepted value for this field:'
    - '       - C(EMULATION)'
    - '       - C(PASSTHRU)'
    - '       - C(PASSTHRU_EXCLUSIVE)'
    - '     - host_device (string): Name of the device that should be used as the
      virtual CD-ROM device backing.'
    - If unset, the virtual CD-ROM device will be configured to automatically detect
      a suitable host device.
    - '     - iso_file (string): Path of the image file that should be used as the
      virtual CD-ROM device backing.'
    - This field is optional and it is only relevant when the value of I(type) is
      ISO_FILE.
    - '     - type (string): This option defines the valid backing types for a virtual
      CD-ROM device.'
    - 'Accepted value for this field:'
    - '       - C(ISO_FILE)'
    - '       - C(HOST_DEVICE)'
    - '       - C(CLIENT_DEVICE)'
    - ' - C(ide) (dict): Address for attaching the device to a virtual IDE adapter.'
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - '   - Accepted keys:'
    - '     - master (boolean): Flag specifying whether the device should be the master
      or slave device on the IDE adapter.'
    - If unset, the server will choose an available connection type. If no IDE connections
      are available, the request will be rejected.
    - '     - primary (boolean): Flag specifying whether the device should be attached
      to the primary or secondary IDE adapter of the virtual machine.'
    - If unset, the server will choose a adapter with an available connection. If
      no IDE connections are available, the request will be rejected.
    - ' - C(sata) (dict): Address for attaching the device to a virtual SATA adapter.'
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - '   - Accepted keys:'
    - '     - bus (integer): Bus number of the adapter to which the device should
      be attached.'
    - '     - unit (integer): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    - ' - C(start_connected) (bool): Flag indicating whether the virtual device should
      be connected whenever the virtual machine is powered on.'
    - Defaults to false if unset.
    - ' - C(type) (str): This option defines the valid types of host bus adapters
      that may be used for attaching a Cdrom to a virtual machine.'
    - '   - Accepted values:'
    - '     - IDE'
    - '     - SATA'
    elements: dict
    type: list
  cpu:
    description:
    - CPU configuration.
    - If unset, guest-specific default values will be used.
    - 'Valide attributes are:'
    - ' - C(cores_per_socket) (int): New number of CPU cores per socket. The number
      of CPU cores in the virtual machine must be a multiple of the number of cores
      per socket.'
    - If unset, the value is unchanged.
    - ' - C(count) (int): New number of CPU cores. The number of CPU cores in the
      virtual machine must be a multiple of the number of cores per socket. '
    - ' The supported range of CPU counts is constrained by the configured guest operating
      system and virtual hardware version of the virtual machine. '
    - ''
    - ' If the virtual machine is running, the number of CPU cores may only be increased
      if I(hot_add_enabled) is true, and may only be decreased if I(hot_remove_enabled)
      is true.'
    - ''
    - If unset, the value is unchanged.
    - ' - C(hot_add_enabled) (bool): Flag indicating whether adding CPUs while the
      virtual machine is running is enabled. '
    - ' This field may only be modified if the virtual machine is powered off.'
    - ''
    - If unset, the value is unchanged.
    - ' - C(hot_remove_enabled) (bool): Flag indicating whether removing CPUs while
      the virtual machine is running is enabled. '
    - ' This field may only be modified if the virtual machine is powered off.'
    - ''
    - If unset, the value is unchanged.
    type: dict
  datastore:
    description:
    - Identifier of the datastore on which the virtual machine's configuration state
      is stored.
    - If unset, I(path) must also be unset and I(datastore_path) must be set.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_datastore_info). '
    type: str
  datastore_path:
    description:
    - Datastore path for the virtual machine's configuration file in the format "[datastore
      name] path". For example "[storage1] Test-VM/Test-VM.vmx".
    - If unset, both I(datastore) and I(path) must be set.
    type: str
  disconnect_all_nics:
    description:
    - Indicates whether all NICs on the destination virtual machine should be disconnected
      from the newtwork
    - If unset, connection status of all NICs on the destination virtual machine will
      be the same as on the source virtual machine.
    type: bool
  disks:
    description:
    - Individual disk relocation map.
    - If unset, all disks will migrate to the datastore specified in the I(datastore)
      field of I()
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_disk). '
    - 'Valide attributes are:'
    - ' - C(backing) (dict): Existing physical resource backing for the virtual disk.
      Exactly one of I(backing) or I(new_vmdk) must be specified.'
    - If unset, the virtual disk will not be connected to an existing backing.
    - '   - Accepted keys:'
    - '     - type (string): This option defines the valid backing types for a virtual
      disk.'
    - 'Accepted value for this field:'
    - '       - C(VMDK_FILE)'
    - '     - vmdk_file (string): Path of the VMDK file backing the virtual disk.'
    - This field is optional and it is only relevant when the value of I(type) is
      VMDK_FILE.
    - ' - C(ide) (dict): Address for attaching the device to a virtual IDE adapter.'
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - '   - Accepted keys:'
    - '     - master (boolean): Flag specifying whether the device should be the master
      or slave device on the IDE adapter.'
    - If unset, the server will choose an available connection type. If no IDE connections
      are available, the request will be rejected.
    - '     - primary (boolean): Flag specifying whether the device should be attached
      to the primary or secondary IDE adapter of the virtual machine.'
    - If unset, the server will choose a adapter with an available connection. If
      no IDE connections are available, the request will be rejected.
    - ' - C(new_vmdk) (dict): Specification for creating a new VMDK backing for the
      virtual disk. Exactly one of I(backing) or I(new_vmdk) must be specified.'
    - If unset, a new VMDK backing will not be created.
    - '   - Accepted keys:'
    - '     - capacity (integer): Capacity of the virtual disk backing in bytes.'
    - If unset, defaults to a guest-specific capacity.
    - '     - name (string): Base name of the VMDK file. The name should not include
      the ''.vmdk'' file extension.'
    - If unset, a name (derived from the name of the virtual machine) will be chosen
      by the server.
    - '     - storage_policy (object): The I(storage_policy_spec) structure contains
      information about the storage policy that is to be associated the with VMDK
      file.'
    - 'If unset the default storage policy of the target datastore (if applicable)
      is applied. Currently a default storage policy is only supported by object based
      datastores : VVol & vSAN. For non- object datastores, if unset then no storage
      policy would be associated with the VMDK file.'
    - ' - C(sata) (dict): Address for attaching the device to a virtual SATA adapter.'
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - '   - Accepted keys:'
    - '     - bus (integer): Bus number of the adapter to which the device should
      be attached.'
    - '     - unit (integer): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    - ' - C(scsi) (dict): Address for attaching the device to a virtual SCSI adapter.'
    - If unset, the server will choose an available address; if none is available,
      the request will fail.
    - '   - Accepted keys:'
    - '     - bus (integer): Bus number of the adapter to which the device should
      be attached.'
    - '     - unit (integer): Unit number of the device.'
    - If unset, the server will choose an available unit number on the specified adapter.
      If there are no available connections on the adapter, the request will be rejected.
    - ' - C(type) (str): This option defines the valid types of host bus adapters
      that may be used for attaching a virtual storage device to a virtual machine.'
    - '   - Accepted values:'
    - '     - IDE'
    - '     - SCSI'
    - '     - SATA'
    elements: dict
    type: list
  disks_to_remove:
    description:
    - Set of Disks to Remove.
    - If unset, all disks will be copied. If the same identifier is in I(disks_to_update)
      InvalidArgument fault will be returned.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain the id of resources returned by M(vcenter_vm_hardware_disk). '
    elements: str
    type: list
  disks_to_update:
    description:
    - Map of Disks to Update.
    - If unset, all disks will copied to the datastore specified in the I(datastore)
      field of I() If the same identifier is in I(disks_to_remove) InvalidArgument
      fault will be thrown.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_disk). '
    - 'Valide attributes are:'
    - ' - C(key) (str): '
    - ' - C(value) (dict): '
    - '   - Accepted keys:'
    - '     - datastore (string): Destination datastore to clone disk.'
    - This field is currently required. In the future, if this field is unset disk
      will be copied to the datastore specified in the I(datastore) field of I()
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_datastore_info). '
    elements: dict
    type: list
  floppies:
    description:
    - List of floppy drives.
    - If unset, no floppy drives will be created.
    - 'Valide attributes are:'
    - ' - C(allow_guest_control) (bool): Flag indicating whether the guest can connect
      and disconnect the device.'
    - Defaults to false if unset.
    - ' - C(backing) (dict): Physical resource backing for the virtual floppy drive.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '   - Accepted keys:'
    - '     - host_device (string): Name of the device that should be used as the
      virtual floppy drive backing.'
    - If unset, the virtual floppy drive will be configured to automatically detect
      a suitable host device.
    - '     - image_file (string): Path of the image file that should be used as the
      virtual floppy drive backing.'
    - This field is optional and it is only relevant when the value of I(type) is
      IMAGE_FILE.
    - '     - type (string): This option defines the valid backing types for a virtual
      floppy drive.'
    - 'Accepted value for this field:'
    - '       - C(IMAGE_FILE)'
    - '       - C(HOST_DEVICE)'
    - '       - C(CLIENT_DEVICE)'
    - ' - C(start_connected) (bool): Flag indicating whether the virtual device should
      be connected whenever the virtual machine is powered on.'
    - Defaults to false if unset.
    elements: dict
    type: list
  guest_OS:
    choices:
    - AMAZONLINUX2_64
    - ASIANUX_3
    - ASIANUX_3_64
    - ASIANUX_4
    - ASIANUX_4_64
    - ASIANUX_5_64
    - ASIANUX_7_64
    - ASIANUX_8_64
    - CENTOS
    - CENTOS_6
    - CENTOS_64
    - CENTOS_6_64
    - CENTOS_7
    - CENTOS_7_64
    - CENTOS_8_64
    - COREOS_64
    - CRXPOD_1
    - DARWIN
    - DARWIN_10
    - DARWIN_10_64
    - DARWIN_11
    - DARWIN_11_64
    - DARWIN_12_64
    - DARWIN_13_64
    - DARWIN_14_64
    - DARWIN_15_64
    - DARWIN_16_64
    - DARWIN_17_64
    - DARWIN_18_64
    - DARWIN_19_64
    - DARWIN_64
    - DEBIAN_10
    - DEBIAN_10_64
    - DEBIAN_11
    - DEBIAN_11_64
    - DEBIAN_4
    - DEBIAN_4_64
    - DEBIAN_5
    - DEBIAN_5_64
    - DEBIAN_6
    - DEBIAN_6_64
    - DEBIAN_7
    - DEBIAN_7_64
    - DEBIAN_8
    - DEBIAN_8_64
    - DEBIAN_9
    - DEBIAN_9_64
    - DOS
    - ECOMSTATION
    - ECOMSTATION_2
    - FEDORA
    - FEDORA_64
    - FREEBSD
    - FREEBSD_11
    - FREEBSD_11_64
    - FREEBSD_12
    - FREEBSD_12_64
    - FREEBSD_64
    - GENERIC_LINUX
    - MANDRAKE
    - MANDRIVA
    - MANDRIVA_64
    - NETWARE_4
    - NETWARE_5
    - NETWARE_6
    - NLD_9
    - OES
    - OPENSERVER_5
    - OPENSERVER_6
    - OPENSUSE
    - OPENSUSE_64
    - ORACLE_LINUX
    - ORACLE_LINUX_6
    - ORACLE_LINUX_64
    - ORACLE_LINUX_6_64
    - ORACLE_LINUX_7
    - ORACLE_LINUX_7_64
    - ORACLE_LINUX_8_64
    - OS2
    - OTHER
    - OTHER_24X_LINUX
    - OTHER_24X_LINUX_64
    - OTHER_26X_LINUX
    - OTHER_26X_LINUX_64
    - OTHER_3X_LINUX
    - OTHER_3X_LINUX_64
    - OTHER_4X_LINUX
    - OTHER_4X_LINUX_64
    - OTHER_64
    - OTHER_LINUX
    - OTHER_LINUX_64
    - REDHAT
    - RHEL_2
    - RHEL_3
    - RHEL_3_64
    - RHEL_4
    - RHEL_4_64
    - RHEL_5
    - RHEL_5_64
    - RHEL_6
    - RHEL_6_64
    - RHEL_7
    - RHEL_7_64
    - RHEL_8_64
    - SJDS
    - SLES
    - SLES_10
    - SLES_10_64
    - SLES_11
    - SLES_11_64
    - SLES_12
    - SLES_12_64
    - SLES_15_64
    - SLES_64
    - SOLARIS_10
    - SOLARIS_10_64
    - SOLARIS_11_64
    - SOLARIS_6
    - SOLARIS_7
    - SOLARIS_8
    - SOLARIS_9
    - SUSE
    - SUSE_64
    - TURBO_LINUX
    - TURBO_LINUX_64
    - UBUNTU
    - UBUNTU_64
    - UNIXWARE_7
    - VMKERNEL
    - VMKERNEL_5
    - VMKERNEL_6
    - VMKERNEL_65
    - VMKERNEL_7
    - VMWARE_PHOTON_64
    - WINDOWS_7
    - WINDOWS_7_64
    - WINDOWS_7_SERVER_64
    - WINDOWS_8
    - WINDOWS_8_64
    - WINDOWS_8_SERVER_64
    - WINDOWS_9
    - WINDOWS_9_64
    - WINDOWS_9_SERVER_64
    - WINDOWS_HYPERV
    - WINDOWS_SERVER_2019
    - WIN_2000_ADV_SERV
    - WIN_2000_PRO
    - WIN_2000_SERV
    - WIN_31
    - WIN_95
    - WIN_98
    - WIN_LONGHORN
    - WIN_LONGHORN_64
    - WIN_ME
    - WIN_NET_BUSINESS
    - WIN_NET_DATACENTER
    - WIN_NET_DATACENTER_64
    - WIN_NET_ENTERPRISE
    - WIN_NET_ENTERPRISE_64
    - WIN_NET_STANDARD
    - WIN_NET_STANDARD_64
    - WIN_NET_WEB
    - WIN_NT
    - WIN_VISTA
    - WIN_VISTA_64
    - WIN_XP_HOME
    - WIN_XP_PRO
    - WIN_XP_PRO_64
    description:
    - The {@name GuestOS} defines the valid guest operating system types used for
      configuring a virtual machine. Required with I(state=['present'])
    type: str
  guest_customization_spec:
    description:
    - Guest customization spec to apply to the virtual machine after the virtual machine
      is deployed.
    - If unset, the guest operating system is not customized after clone.
    - 'Valide attributes are:'
    - ' - C(name) (str): Name of the customization specification.'
    - If unset, no guest customization is performed.
    type: dict
  hardware_version:
    choices:
    - VMX_03
    - VMX_04
    - VMX_06
    - VMX_07
    - VMX_08
    - VMX_09
    - VMX_10
    - VMX_11
    - VMX_12
    - VMX_13
    - VMX_14
    - VMX_15
    - VMX_16
    - VMX_17
    description:
    - The I(version) enumerated type defines the valid virtual hardware versions for
      a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual machine
      hardware versions (1003746)).
    type: str
  memory:
    description:
    - Memory configuration.
    - If unset, guest-specific default values will be used.
    - 'Valide attributes are:'
    - ' - C(hot_add_enabled) (bool): Flag indicating whether adding memory while the
      virtual machine is running should be enabled. '
    - ' Some guest operating systems may consume more resources or perform less efficiently
      when they run on hardware that supports adding memory while the machine is running. '
    - ''
    - ' This field may only be modified if the virtual machine is not powered on.'
    - ''
    - If unset, the value is unchanged.
    - ' - C(size_MiB) (int): New memory size in mebibytes. '
    - ' The supported range of memory sizes is constrained by the configured guest
      operating system and virtual hardware version of the virtual machine. '
    - ''
    - ' If the virtual machine is running, this value may only be changed if I(hot_add_enabled)
      is true, and the new memory size must satisfy the constraints specified by I(hot_add_increment_size_mib)
      and I()'
    - ''
    - If unset, the value is unchanged.
    type: dict
  name:
    description:
    - Virtual machine name.
    - If unset, the display name from the virtual machine's configuration file will
      be used.
    type: str
  nics:
    description:
    - List of Ethernet adapters.
    - If unset, no Ethernet adapters will be created.
    - 'Valide attributes are:'
    - ' - C(allow_guest_control) (bool): Flag indicating whether the guest can connect
      and disconnect the device.'
    - Defaults to false if unset.
    - ' - C(backing) (dict): Physical resource backing for the virtual Ethernet adapter.'
    - If unset, the system may try to find an appropriate backing. If one is not found,
      the request will fail.
    - '   - Accepted keys:'
    - '     - distributed_port (string): Key of the distributed virtual port that
      backs the virtual Ethernet adapter. Depending on the type of the Portgroup,
      the port may be specified using this field. If the portgroup type is early-binding
      (also known as static), a port is assigned when the Ethernet adapter is configured
      to use the port. The port may be either automatically or specifically assigned
      based on the value of this field. If the portgroup type is ephemeral, the port
      is created and assigned to a virtual machine when it is powered on and the Ethernet
      adapter is connected. This field cannot be specified as no free ports exist
      before use.'
    - May be used to specify a port when the network specified on the I(network) field
      is a static or early binding distributed portgroup. If unset, the port will
      be automatically assigned to the Ethernet adapter based on the policy embodied
      by the portgroup type.
    - '     - network (string): Identifier of the network that backs the virtual Ethernet
      adapter.'
    - This field is optional and it is only relevant when the value of I(type) is
      one of STANDARD_PORTGROUP, DISTRIBUTED_PORTGROUP, or OPAQUE_NETWORK.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_network_info). '
    - '     - type (string): This option defines the valid backing types for a virtual
      Ethernet adapter.'
    - 'Accepted value for this field:'
    - '       - C(STANDARD_PORTGROUP)'
    - '       - C(HOST_DEVICE)'
    - '       - C(DISTRIBUTED_PORTGROUP)'
    - '       - C(OPAQUE_NETWORK)'
    - ' - C(mac_address) (str): MAC address.'
    - Workaround for PR1459647
    - ' - C(mac_type) (str): This option defines the valid MAC address origins for
      a virtual Ethernet adapter.'
    - '   - Accepted values:'
    - '     - MANUAL'
    - '     - GENERATED'
    - '     - ASSIGNED'
    - ' - C(pci_slot_number) (int): Address of the virtual Ethernet adapter on the
      PCI bus. If the PCI address is invalid, the server will change when it the VM
      is started or as the device is hot added.'
    - If unset, the server will choose an available address when the virtual machine
      is powered on.
    - ' - C(start_connected) (bool): Flag indicating whether the virtual device should
      be connected whenever the virtual machine is powered on.'
    - Defaults to false if unset.
    - ' - C(type) (str): This option defines the valid emulation types for a virtual
      Ethernet adapter.'
    - '   - Accepted values:'
    - '     - E1000'
    - '     - E1000E'
    - '     - PCNET32'
    - '     - VMXNET'
    - '     - VMXNET2'
    - '     - VMXNET3'
    - ' - C(upt_compatibility_enabled) (bool): Flag indicating whether Universal Pass-Through
      (UPT) compatibility is enabled on this virtual Ethernet adapter.'
    - If unset, defaults to false.
    - ' - C(wake_on_lan_enabled) (bool): Flag indicating whether wake-on-LAN is enabled
      on this virtual Ethernet adapter.'
    - Defaults to false if unset.
    elements: dict
    type: list
  nics_to_update:
    description:
    - Map of NICs to update.
    - If unset, no NICs will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_ethernet). '
    - 'Valide attributes are:'
    - ' - C(key) (str): '
    - ' - C(value) (dict): '
    - '   - Accepted keys:'
    - '     - allow_guest_control (boolean): Flag indicating whether the guest can
      connect and disconnect the device.'
    - If unset, the value is unchanged.
    - '     - backing (object): Physical resource backing for the virtual Ethernet
      adapter.'
    - If unset, the system may try to find an appropriate backing. If one is not found,
      the request will fail.
    - '     - mac_address (string): MAC address. '
    - ' This field may be modified at any time, and changes will be applied the next
      time the virtual machine is powered on.'
    - ''
    - If unset, the value is unchanged. Must be specified if I(mac_type) is MANUAL.
      Must be unset if the MAC address type is not MANUAL.
    - '     - mac_type (string): This option defines the valid MAC address origins
      for a virtual Ethernet adapter.'
    - 'Accepted value for this field:'
    - '       - C(MANUAL)'
    - '       - C(GENERATED)'
    - '       - C(ASSIGNED)'
    - '     - start_connected (boolean): Flag indicating whether the virtual device
      should be connected whenever the virtual machine is powered on.'
    - If unset, the value is unchanged.
    - '     - upt_compatibility_enabled (boolean): Flag indicating whether Universal
      Pass-Through (UPT) compatibility should be enabled on this virtual Ethernet
      adapter. '
    - ' This field may be modified at any time, and changes will be applied the next
      time the virtual machine is powered on.'
    - ''
    - If unset, the value is unchanged. Must be unset if the emulation type of the
      virtual Ethernet adapter is not VMXNET3.
    - '     - wake_on_lan_enabled (boolean): Flag indicating whether wake-on-LAN shoud
      be enabled on this virtual Ethernet adapter. '
    - ' This field may be modified at any time, and changes will be applied the next
      time the virtual machine is powered on.'
    - ''
    - If unset, the value is unchanged.
    elements: dict
    type: list
  parallel_ports:
    description:
    - List of parallel ports.
    - If unset, no parallel ports will be created.
    - 'Valide attributes are:'
    - ' - C(allow_guest_control) (bool): Flag indicating whether the guest can connect
      and disconnect the device.'
    - Defaults to false if unset.
    - ' - C(backing) (dict): Physical resource backing for the virtual parallel port.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '   - Accepted keys:'
    - '     - file (string): Path of the file that should be used as the virtual parallel
      port backing.'
    - This field is optional and it is only relevant when the value of I(type) is
      FILE.
    - '     - host_device (string): Name of the device that should be used as the
      virtual parallel port backing.'
    - If unset, the virtual parallel port will be configured to automatically detect
      a suitable host device.
    - '     - type (string): This option defines the valid backing types for a virtual
      parallel port.'
    - 'Accepted value for this field:'
    - '       - C(FILE)'
    - '       - C(HOST_DEVICE)'
    - ' - C(start_connected) (bool): Flag indicating whether the virtual device should
      be connected whenever the virtual machine is powered on.'
    - Defaults to false if unset.
    elements: dict
    type: list
  parallel_ports_to_update:
    description:
    - Map of parallel ports to Update.
    - If unset, no parallel ports will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_parallel). '
    - 'Valide attributes are:'
    - ' - C(key) (str): '
    - ' - C(value) (dict): '
    - '   - Accepted keys:'
    - '     - allow_guest_control (boolean): Flag indicating whether the guest can
      connect and disconnect the device.'
    - If unset, the value is unchanged.
    - '     - backing (object): Physical resource backing for the virtual parallel
      port.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '     - start_connected (boolean): Flag indicating whether the virtual device
      should be connected whenever the virtual machine is powered on.'
    - If unset, the value is unchanged.
    elements: dict
    type: list
  path:
    description:
    - 'Path to the virtual machine''s configuration file on the datastore corresponding
      to {@link #datastore).'
    - If unset, I(datastore) must also be unset and I(datastore_path) must be set.
    type: str
  placement:
    description:
    - Virtual machine placement information.
    - If this field is unset, the system will use the values from the source virtual
      machine. If specified, each field will be used for placement. If the fields
      result in disjoint placement the operation will fail. If the fields along with
      the other existing placement of the virtual machine result in disjoint placement
      the operation will fail.
    - 'Valide attributes are:'
    - ' - C(cluster) (str): Cluster into which the virtual machine should be placed. '
    - ' If I(cluster) and I(resource_pool) are both specified, I(resource_pool) must
      belong to I(cluster). '
    - ''
    - ' If I(cluster) and I(host) are both specified, I(host) must be a member of
      I(cluster).'
    - ''
    - If I(resource_pool) or I(host) is specified, it is recommended that this field
      be unset.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_cluster_info). '
    - ' - C(datastore) (str): Datastore on which the virtual machine''s configuration
      state should be stored. This datastore will also be used for any virtual disks
      that are created as part of the virtual machine creation operation.'
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose suitable storage for the virtual machine; if storage
      cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_datastore_info). '
    - ' - C(folder) (str): Virtual machine folder into which the virtual machine should
      be placed.'
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose a suitable folder for the virtual machine; if
      a folder cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_folder_info). '
    - ' - C(host) (str): Host onto which the virtual machine should be placed. '
    - ' If I(host) and I(resource_pool) are both specified, I(resource_pool) must
      belong to I(host). '
    - ''
    - ' If I(host) and I(cluster) are both specified, I(host) must be a member of
      I(cluster).'
    - ''
    - This field may be unset if I(resource_pool) or I(cluster) is specified. If unset,
      the system will attempt to choose a suitable host for the virtual machine; if
      a host cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_host_info). '
    - ' - C(resource_pool) (str): Resource pool into which the virtual machine should
      be placed.'
    - This field is currently required if both I(host) and I(cluster) are unset. In
      the future, if this field is unset, the system will attempt to choose a suitable
      resource pool for the virtual machine; if a resource pool cannot be chosen,
      the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_resourcepool_info). '
    type: dict
  power_on:
    description:
    - Attempt to perform a I(power_on) after clone.
    - If unset, the virtual machine will not be powered on.
    type: bool
  sata_adapters:
    description:
    - List of SATA adapters.
    - If unset, any adapters necessary to connect the virtual machine's storage devices
      will be created; this includes any devices that explicitly specify a SATA host
      bus adapter, as well as any devices that do not specify a host bus adapter if
      the guest's preferred adapter type is SATA.
    - 'Valide attributes are:'
    - ' - C(bus) (int): SATA bus number.'
    - If unset, the server will choose an available bus number; if none is available,
      the request will fail.
    - ' - C(pci_slot_number) (int): Address of the SATA adapter on the PCI bus.'
    - If unset, the server will choose an available address when the virtual machine
      is powered on.
    - ' - C(type) (str): This option defines the valid emulation types for a virtual
      SATA adapter.'
    - '   - Accepted values:'
    - '     - AHCI'
    elements: dict
    type: list
  scsi_adapters:
    description:
    - List of SCSI adapters.
    - If unset, any adapters necessary to connect the virtual machine's storage devices
      will be created; this includes any devices that explicitly specify a SCSI host
      bus adapter, as well as any devices that do not specify a host bus adapter if
      the guest's preferred adapter type is SCSI. The type of the SCSI adapter will
      be a guest-specific default type.
    - 'Valide attributes are:'
    - ' - C(bus) (int): SCSI bus number.'
    - If unset, the server will choose an available bus number; if none is available,
      the request will fail.
    - ' - C(pci_slot_number) (int): Address of the SCSI adapter on the PCI bus. If
      the PCI address is invalid, the server will change it when the VM is started
      or as the device is hot added.'
    - If unset, the server will choose an available address when the virtual machine
      is powered on.
    - ' - C(sharing) (str): This option defines the valid bus sharing modes for a
      virtual SCSI adapter.'
    - '   - Accepted values:'
    - '     - NONE'
    - '     - VIRTUAL'
    - '     - PHYSICAL'
    - ' - C(type) (str): This option defines the valid emulation types for a virtual
      SCSI adapter.'
    - '   - Accepted values:'
    - '     - BUSLOGIC'
    - '     - LSILOGIC'
    - '     - LSILOGICSAS'
    - '     - PVSCSI'
    elements: dict
    type: list
  serial_ports:
    description:
    - List of serial ports.
    - If unset, no serial ports will be created.
    - 'Valide attributes are:'
    - ' - C(allow_guest_control) (bool): Flag indicating whether the guest can connect
      and disconnect the device.'
    - Defaults to false if unset.
    - ' - C(backing) (dict): Physical resource backing for the virtual serial port.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '   - Accepted keys:'
    - '     - file (string): Path of the file backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of I(type) is
      FILE.
    - '     - host_device (string): Name of the device backing the virtual serial
      port. '
    - ''
    - ''
    - If unset, the virtual serial port will be configured to automatically detect
      a suitable host device.
    - '     - network_location (string): URI specifying the location of the network
      service backing the virtual serial port. '
    - '   - If I(type) is NETWORK_SERVER, this field is the location used by clients
      to connect to this server. The hostname part of the URI should either be empty
      or should specify the address of the host on which the virtual machine is running.'
    - '   - If I(type) is NETWORK_CLIENT, this field is the location used by the virtual
      machine to connect to the remote server.'
    - ' '
    - This field is optional and it is only relevant when the value of I(type) is
      one of NETWORK_SERVER or NETWORK_CLIENT.
    - '     - no_rx_loss (boolean): Flag that enables optimized data transfer over
      the pipe. When the value is true, the host buffers data to prevent data overrun.
      This allows the virtual machine to read all of the data transferred over the
      pipe with no data loss.'
    - If unset, defaults to false.
    - '     - pipe (string): Name of the pipe backing the virtual serial port.'
    - This field is optional and it is only relevant when the value of I(type) is
      one of PIPE_SERVER or PIPE_CLIENT.
    - '     - proxy (string): Proxy service that provides network access to the network
      backing. If set, the virtual machine initiates a connection with the proxy service
      and forwards the traffic to the proxy.'
    - If unset, no proxy service should be used.
    - '     - type (string): This option defines the valid backing types for a virtual
      serial port.'
    - 'Accepted value for this field:'
    - '       - C(FILE)'
    - '       - C(HOST_DEVICE)'
    - '       - C(PIPE_SERVER)'
    - '       - C(PIPE_CLIENT)'
    - '       - C(NETWORK_SERVER)'
    - '       - C(NETWORK_CLIENT)'
    - ' - C(start_connected) (bool): Flag indicating whether the virtual device should
      be connected whenever the virtual machine is powered on.'
    - Defaults to false if unset.
    - ' - C(yield_on_poll) (bool): CPU yield behavior. If set to true, the virtual
      machine will periodically relinquish the processor if its sole task is polling
      the virtual serial port. The amount of time it takes to regain the processor
      will depend on the degree of other virtual machine activity on the host.'
    - If unset, defaults to false.
    elements: dict
    type: list
  serial_ports_to_update:
    description:
    - Map of serial ports to Update.
    - If unset, no serial ports will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be the id of a resource returned by M(vcenter_vm_hardware_serial). '
    - 'Valide attributes are:'
    - ' - C(key) (str): '
    - ' - C(value) (dict): '
    - '   - Accepted keys:'
    - '     - allow_guest_control (boolean): Flag indicating whether the guest can
      connect and disconnect the device.'
    - If unset, the value is unchanged.
    - '     - backing (object): Physical resource backing for the virtual serial port.'
    - If unset, defaults to automatic detection of a suitable host device.
    - '     - start_connected (boolean): Flag indicating whether the virtual device
      should be connected whenever the virtual machine is powered on.'
    - If unset, the value is unchanged.
    - '     - yield_on_poll (boolean): CPU yield behavior. If set to true, the virtual
      machine will periodically relinquish the processor if its sole task is polling
      the virtual serial port. The amount of time it takes to regain the processor
      will depend on the degree of other virtual machine activity on the host. '
    - ' This field may be modified at any time, and changes applied to a connected
      virtual serial port take effect immediately.'
    - ''
    - If unset, the value is unchanged.
    elements: dict
    type: list
  source:
    description:
    - Virtual machine to InstantClone from.
    - When clients pass a value of this structure as a parameter, the field must be
      the id of a resource returned by M(vcenter_vm_info). Required with I(state=['clone',
      'instant_clone'])
    type: str
  state:
    choices:
    - absent
    - clone
    - instant_clone
    - present
    - register
    - relocate
    - unregister
    default: present
    description: []
    type: str
  storage_policy:
    description:
    - The I(storage_policy_spec) structure contains information about the storage
      policy that is to be associated with the virtual machine home (which contains
      the configuration and log files).
    - 'If unset the datastore default storage policy (if applicable) is applied. Currently
      a default storage policy is only supported by object datastores : VVol and vSAN.
      For non-object datastores, if unset then no storage policy would be associated
      with the virtual machine home.'
    - 'Valide attributes are:'
    - ' - C(policy) (str): Identifier of the storage policy which should be associated
      with the virtual machine.'
    - 'When clients pass a value of this structure as a parameter, the field must
      be the id of a resource returned by M(vcenter_storage_policies). '
    type: dict
  vcenter_hostname:
    description:
    - The hostname or IP address of the vSphere vCenter
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_HOST) will be used instead.
    required: true
    type: str
  vcenter_password:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_PASSWORD) will be used instead.
    required: true
    type: str
  vcenter_rest_log_file:
    description:
    - 'You can use this optional parameter to set the location of a log file. '
    - 'This file will be used to record the HTTP REST interaction. '
    - 'The file will be stored on the host that run the module. '
    - 'If the value is not specified in the task, the value of '
    - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
    type: str
  vcenter_username:
    description:
    - The vSphere vCenter username
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_USER) will be used instead.
    required: true
    type: str
  vcenter_validate_certs:
    default: true
    description:
    - Allows connection when SSL certificates are not valid. Set to C(false) when
      certificates are not trusted.
    - If the value is not specified in the task, the value of environment variable
      C(VMWARE_VALIDATE_CERTS) will be used instead.
    type: bool
  vm:
    description:
    - Identifier of the virtual machine to be unregistered.
    - The parameter must be the id of a resource returned by M(vcenter_vm_info). Required
      with I(state=['absent', 'relocate', 'unregister'])
    type: str
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = r"""
- name: Collect the list of the existing VM
  vmware.vmware_rest.vcenter_vm_info:
  register: existing_vms
  until: existing_vms is not failed
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
- name: Delete some VM
  vmware.vmware_rest.vcenter_vm:
    state: absent
    vm: '{{ item.vm }}'
  with_items: '{{ existing_vms.value }}'
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Create a VM
id:
  description: moid of the resource
  returned: On success
  sample: vm-1021
  type: str
value:
  description: Create a VM
  returned: On success
  sample:
    boot:
      delay: 0
      enter_setup_mode: 0
      retry: 0
      retry_delay: 10000
      type: BIOS
    boot_devices: []
    cdroms: []
    cpu:
      cores_per_socket: 1
      count: 1
      hot_add_enabled: 0
      hot_remove_enabled: 0
    disks:
    - key: '2000'
      value:
        backing:
          type: VMDK_FILE
          vmdk_file: '[rw_datastore] test_vm1/test_vm1.vmdk'
        capacity: 17179869184
        label: Hard disk 1
        scsi:
          bus: 0
          unit: 0
        type: SCSI
    floppies: []
    guest_OS: DEBIAN_8_64
    hardware:
      upgrade_policy: NEVER
      upgrade_status: NONE
      version: VMX_11
    identity:
      bios_uuid: 42331fc7-6db1-b2c5-3018-cd5145dbf960
      instance_uuid: 5033ed7f-b14b-e3c3-9dbe-18816989cf99
      name: test_vm1
    instant_clone_frozen: 0
    memory:
      hot_add_enabled: 1
      size_MiB: 1024
    name: test_vm1
    nics: []
    nvme_adapters: []
    parallel_ports: []
    power_state: POWERED_OFF
    sata_adapters: []
    scsi_adapters:
    - key: '1000'
      value:
        label: SCSI controller 0
        scsi:
          bus: 0
          unit: 7
        sharing: NONE
        type: PVSCSI
    serial_ports: []
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "list": {
        "query": {
            "filter.clusters": "filter.clusters",
            "filter.datacenters": "filter.datacenters",
            "filter.folders": "filter.folders",
            "filter.hosts": "filter.hosts",
            "filter.names": "filter.names",
            "filter.power_states": "filter.power_states",
            "filter.resource_pools": "filter.resource_pools",
            "filter.vms": "filter.vms",
        },
        "body": {},
        "path": {},
    },
    "create": {
        "query": {},
        "body": {
            "boot": "spec/boot",
            "boot_devices": "spec/boot_devices",
            "cdroms": "spec/cdroms",
            "cpu": "spec/cpu",
            "disks": "spec/disks",
            "floppies": "spec/floppies",
            "guest_OS": "spec/guest_OS",
            "hardware_version": "spec/hardware_version",
            "memory": "spec/memory",
            "name": "spec/name",
            "nics": "spec/nics",
            "parallel_ports": "spec/parallel_ports",
            "placement": "spec/placement",
            "sata_adapters": "spec/sata_adapters",
            "scsi_adapters": "spec/scsi_adapters",
            "serial_ports": "spec/serial_ports",
            "storage_policy": "spec/storage_policy",
        },
        "path": {},
    },
    "delete": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "get": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "relocate": {
        "query": {},
        "body": {"disks": "spec/disks", "placement": "spec/placement"},
        "path": {"vm": "vm"},
    },
    "unregister": {"query": {}, "body": {}, "path": {"vm": "vm"}},
    "clone": {
        "query": {},
        "body": {
            "disks_to_remove": "spec/disks_to_remove",
            "disks_to_update": "spec/disks_to_update",
            "guest_customization_spec": "spec/guest_customization_spec",
            "name": "spec/name",
            "placement": "spec/placement",
            "power_on": "spec/power_on",
            "source": "spec/source",
        },
        "path": {},
    },
    "instant_clone": {
        "query": {},
        "body": {
            "bios_uuid": "spec/bios_uuid",
            "disconnect_all_nics": "spec/disconnect_all_nics",
            "name": "spec/name",
            "nics_to_update": "spec/nics_to_update",
            "parallel_ports_to_update": "spec/parallel_ports_to_update",
            "placement": "spec/placement",
            "serial_ports_to_update": "spec/serial_ports_to_update",
            "source": "spec/source",
        },
        "path": {},
    },
    "register": {
        "query": {},
        "body": {
            "datastore": "spec/datastore",
            "datastore_path": "spec/datastore_path",
            "name": "spec/name",
            "path": "spec/path",
            "placement": "spec/placement",
        },
        "path": {},
    },
}

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    build_full_device_list,
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    list_devices,
    open_session,
    prepare_payload,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str", required=True, fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
    }

    argument_spec["bios_uuid"] = {"type": "str"}
    argument_spec["boot"] = {"type": "dict"}
    argument_spec["boot_devices"] = {"type": "list", "elements": "dict"}
    argument_spec["cdroms"] = {"type": "list", "elements": "dict"}
    argument_spec["cpu"] = {"type": "dict"}
    argument_spec["datastore"] = {"type": "str"}
    argument_spec["datastore_path"] = {"type": "str"}
    argument_spec["disconnect_all_nics"] = {"type": "bool"}
    argument_spec["disks"] = {"type": "list", "elements": "dict"}
    argument_spec["disks_to_remove"] = {"type": "list", "elements": "str"}
    argument_spec["disks_to_update"] = {"type": "list", "elements": "dict"}
    argument_spec["floppies"] = {"type": "list", "elements": "dict"}
    argument_spec["guest_OS"] = {
        "type": "str",
        "choices": [
            "AMAZONLINUX2_64",
            "ASIANUX_3",
            "ASIANUX_3_64",
            "ASIANUX_4",
            "ASIANUX_4_64",
            "ASIANUX_5_64",
            "ASIANUX_7_64",
            "ASIANUX_8_64",
            "CENTOS",
            "CENTOS_6",
            "CENTOS_64",
            "CENTOS_6_64",
            "CENTOS_7",
            "CENTOS_7_64",
            "CENTOS_8_64",
            "COREOS_64",
            "CRXPOD_1",
            "DARWIN",
            "DARWIN_10",
            "DARWIN_10_64",
            "DARWIN_11",
            "DARWIN_11_64",
            "DARWIN_12_64",
            "DARWIN_13_64",
            "DARWIN_14_64",
            "DARWIN_15_64",
            "DARWIN_16_64",
            "DARWIN_17_64",
            "DARWIN_18_64",
            "DARWIN_19_64",
            "DARWIN_64",
            "DEBIAN_10",
            "DEBIAN_10_64",
            "DEBIAN_11",
            "DEBIAN_11_64",
            "DEBIAN_4",
            "DEBIAN_4_64",
            "DEBIAN_5",
            "DEBIAN_5_64",
            "DEBIAN_6",
            "DEBIAN_6_64",
            "DEBIAN_7",
            "DEBIAN_7_64",
            "DEBIAN_8",
            "DEBIAN_8_64",
            "DEBIAN_9",
            "DEBIAN_9_64",
            "DOS",
            "ECOMSTATION",
            "ECOMSTATION_2",
            "FEDORA",
            "FEDORA_64",
            "FREEBSD",
            "FREEBSD_11",
            "FREEBSD_11_64",
            "FREEBSD_12",
            "FREEBSD_12_64",
            "FREEBSD_64",
            "GENERIC_LINUX",
            "MANDRAKE",
            "MANDRIVA",
            "MANDRIVA_64",
            "NETWARE_4",
            "NETWARE_5",
            "NETWARE_6",
            "NLD_9",
            "OES",
            "OPENSERVER_5",
            "OPENSERVER_6",
            "OPENSUSE",
            "OPENSUSE_64",
            "ORACLE_LINUX",
            "ORACLE_LINUX_6",
            "ORACLE_LINUX_64",
            "ORACLE_LINUX_6_64",
            "ORACLE_LINUX_7",
            "ORACLE_LINUX_7_64",
            "ORACLE_LINUX_8_64",
            "OS2",
            "OTHER",
            "OTHER_24X_LINUX",
            "OTHER_24X_LINUX_64",
            "OTHER_26X_LINUX",
            "OTHER_26X_LINUX_64",
            "OTHER_3X_LINUX",
            "OTHER_3X_LINUX_64",
            "OTHER_4X_LINUX",
            "OTHER_4X_LINUX_64",
            "OTHER_64",
            "OTHER_LINUX",
            "OTHER_LINUX_64",
            "REDHAT",
            "RHEL_2",
            "RHEL_3",
            "RHEL_3_64",
            "RHEL_4",
            "RHEL_4_64",
            "RHEL_5",
            "RHEL_5_64",
            "RHEL_6",
            "RHEL_6_64",
            "RHEL_7",
            "RHEL_7_64",
            "RHEL_8_64",
            "SJDS",
            "SLES",
            "SLES_10",
            "SLES_10_64",
            "SLES_11",
            "SLES_11_64",
            "SLES_12",
            "SLES_12_64",
            "SLES_15_64",
            "SLES_64",
            "SOLARIS_10",
            "SOLARIS_10_64",
            "SOLARIS_11_64",
            "SOLARIS_6",
            "SOLARIS_7",
            "SOLARIS_8",
            "SOLARIS_9",
            "SUSE",
            "SUSE_64",
            "TURBO_LINUX",
            "TURBO_LINUX_64",
            "UBUNTU",
            "UBUNTU_64",
            "UNIXWARE_7",
            "VMKERNEL",
            "VMKERNEL_5",
            "VMKERNEL_6",
            "VMKERNEL_65",
            "VMKERNEL_7",
            "VMWARE_PHOTON_64",
            "WINDOWS_7",
            "WINDOWS_7_64",
            "WINDOWS_7_SERVER_64",
            "WINDOWS_8",
            "WINDOWS_8_64",
            "WINDOWS_8_SERVER_64",
            "WINDOWS_9",
            "WINDOWS_9_64",
            "WINDOWS_9_SERVER_64",
            "WINDOWS_HYPERV",
            "WINDOWS_SERVER_2019",
            "WIN_2000_ADV_SERV",
            "WIN_2000_PRO",
            "WIN_2000_SERV",
            "WIN_31",
            "WIN_95",
            "WIN_98",
            "WIN_LONGHORN",
            "WIN_LONGHORN_64",
            "WIN_ME",
            "WIN_NET_BUSINESS",
            "WIN_NET_DATACENTER",
            "WIN_NET_DATACENTER_64",
            "WIN_NET_ENTERPRISE",
            "WIN_NET_ENTERPRISE_64",
            "WIN_NET_STANDARD",
            "WIN_NET_STANDARD_64",
            "WIN_NET_WEB",
            "WIN_NT",
            "WIN_VISTA",
            "WIN_VISTA_64",
            "WIN_XP_HOME",
            "WIN_XP_PRO",
            "WIN_XP_PRO_64",
        ],
    }
    argument_spec["guest_customization_spec"] = {"type": "dict"}
    argument_spec["hardware_version"] = {
        "type": "str",
        "choices": [
            "VMX_03",
            "VMX_04",
            "VMX_06",
            "VMX_07",
            "VMX_08",
            "VMX_09",
            "VMX_10",
            "VMX_11",
            "VMX_12",
            "VMX_13",
            "VMX_14",
            "VMX_15",
            "VMX_16",
            "VMX_17",
        ],
    }
    argument_spec["memory"] = {"type": "dict"}
    argument_spec["name"] = {"type": "str"}
    argument_spec["nics"] = {"type": "list", "elements": "dict"}
    argument_spec["nics_to_update"] = {"type": "list", "elements": "dict"}
    argument_spec["parallel_ports"] = {"type": "list", "elements": "dict"}
    argument_spec["parallel_ports_to_update"] = {"type": "list", "elements": "dict"}
    argument_spec["path"] = {"type": "str"}
    argument_spec["placement"] = {"type": "dict"}
    argument_spec["power_on"] = {"type": "bool"}
    argument_spec["sata_adapters"] = {"type": "list", "elements": "dict"}
    argument_spec["scsi_adapters"] = {"type": "list", "elements": "dict"}
    argument_spec["serial_ports"] = {"type": "list", "elements": "dict"}
    argument_spec["serial_ports_to_update"] = {"type": "list", "elements": "dict"}
    argument_spec["source"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": [
            "absent",
            "clone",
            "instant_clone",
            "present",
            "register",
            "relocate",
            "unregister",
        ],
        "default": "present",
    }
    argument_spec["storage_policy"] = {"type": "dict"}
    argument_spec["vm"] = {"type": "str"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
        validate_certs=module.params["vcenter_validate_certs"],
        log_file=module.params["vcenter_rest_log_file"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: URL
def build_url(params):
    return ("https://{vcenter_hostname}" "/rest/vcenter/vm").format(**params)


# template: main_content
async def entry_point(module, session):
    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]
    return await func(module.params, session)


# template: FUNC_WITH_DATA_TPL
async def _clone(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["clone"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["clone"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm?action=clone&vmw-task=true")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm?action=clone&vmw-task=true"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "clone")


# FUNC_WITH_DATA_CREATE_TPL
async def _create(params, session):
    if params["vm"]:
        _json = await get_device_info(session, build_url(params), params["vm"])
    else:
        _json = await exists(params, session, build_url(params), ["vm"])
    if _json:
        if "_update" in globals():
            params["vm"] = _json["id"]
            return await globals()["_update"](params, session)
        else:
            return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm").format(**params)
    async with session.post(_url, json=payload) as resp:
        if resp.status == 500:
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {await resp.text()}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        # Update the value field with all the details
        if (resp.status in [200, 201]) and "value" in _json:
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(session, _url, _id)

        return await update_changed_flag(_json, resp.status, "create")


# template: FUNC_WITH_DATA_DELETE_TPL
async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}").format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


# template: FUNC_WITH_DATA_TPL
async def _instant_clone(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["instant_clone"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["instant_clone"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm?action=instant-clone")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm?action=instant-clone"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "instant_clone")


# template: FUNC_WITH_DATA_TPL
async def _register(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["register"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["register"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm?action=register")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = ("https://{vcenter_hostname}" "/rest/vcenter/vm?action=register").format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "register")


# template: FUNC_WITH_DATA_TPL
async def _relocate(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["relocate"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["relocate"])
    subdevice_type = get_subdevice_type(
        "/rest/vcenter/vm/{vm}?action=relocate&vmw-task=true"
    )
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}"
        "/rest/vcenter/vm/{vm}?action=relocate&vmw-task=true"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "relocate")


# template: FUNC_WITH_DATA_TPL
async def _unregister(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["unregister"]["query"].keys()
    payload = payload = prepare_payload(params, PAYLOAD_FORMAT["unregister"])
    subdevice_type = get_subdevice_type("/rest/vcenter/vm/{vm}?action=unregister")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/rest/vcenter/vm/{vm}?action=unregister"
    ).format(**params) + gen_args(params, _in_query_parameters)
    async with session.post(_url, json=payload) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "unregister")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
