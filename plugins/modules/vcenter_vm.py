#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
module: vcenter_vm
short_description: Handle resource of type vcenter_vm
description: Handle resource of type vcenter_vm
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
    - 'Validate attributes are:'
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
    - ' - C(network_protocol) (str): The Boot.NetworkProtocol enumerated type defines
      the valid network boot protocols supported when booting a virtual machine with
      EFI firmware over the network.'
    - ' - C(retry) (bool): Flag indicating whether the virtual machine should automatically
      retry the boot process after a failure.'
    - If unset, default value is false.
    - ' - C(retry_delay) (int): Delay in milliseconds before retrying the boot process
      after a failure; applicable only when Boot.Info.retry is true.'
    - If unset, default value is 10000.
    - ' - C(type) (str): The Boot.Type enumerated type defines the valid firmware
      types for a virtual machine.'
    type: dict
  boot_devices:
    description:
    - Boot device configuration.
    - If unset, a server-specific boot sequence will be used.
    elements: str
    type: list
  cdroms:
    description:
    - List of CD-ROMs.
    - If unset, no CD-ROM devices will be created.
    elements: str
    type: list
  cpu:
    description:
    - CPU configuration.
    - If unset, guest-specific default values will be used.
    - 'Validate attributes are:'
    - ' - C(cores_per_socket) (int): New number of CPU cores per socket. The number
      of CPU cores in the virtual machine must be a multiple of the number of cores
      per socket.'
    - If unset, the value is unchanged.
    - ' - C(count) (int): New number of CPU cores. The number of CPU cores in the
      virtual machine must be a multiple of the number of cores per socket. '
    - ' The supported range of CPU counts is constrained by the configured guest operating
      system and virtual hardware version of the virtual machine. '
    - ' If the virtual machine is running, the number of CPU cores may only be increased
      if Cpu.Info.hot-add-enabled is true, and may only be decreased if Cpu.Info.hot-remove-enabled
      is true.'
    - If unset, the value is unchanged.
    - ' - C(hot_add_enabled) (bool): Flag indicating whether adding CPUs while the
      virtual machine is running is enabled. '
    - ' This field may only be modified if the virtual machine is powered off.'
    - If unset, the value is unchanged.
    - ' - C(hot_remove_enabled) (bool): Flag indicating whether removing CPUs while
      the virtual machine is running is enabled. '
    - ' This field may only be modified if the virtual machine is powered off.'
    - If unset, the value is unchanged.
    type: dict
  datastore:
    description:
    - Identifier of the datastore on which the virtual machine's configuration state
      is stored.
    - If unset, VM.RegisterSpec.path must also be unset and VM.RegisterSpec.datastore-path
      must be set.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Datastore. When operations return a
      value of this structure as a result, the field will be an identifier for the
      resource type: Datastore.'
    type: str
  datastore_path:
    description:
    - Datastore path for the virtual machine's configuration file in the format "[datastore
      name] path". For example "[storage1] Test-VM/Test-VM.vmx".
    - If unset, both VM.RegisterSpec.datastore and VM.RegisterSpec.path must be set.
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
    - If unset, all disks will migrate to the datastore specified in the VM.RelocatePlacementSpec.datastore
      field of VM.RelocateSpec.placement.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be an identifier for the resource type: vcenter.vm.hardware.Disk.
      When operations return a value of this structure as a result, the key in the
      field map will be an identifier for the resource type: vcenter.vm.hardware.Disk.'
    elements: str
    type: list
  disks_to_remove:
    description:
    - Set of Disks to Remove.
    - If unset, all disks will be copied. If the same identifier is in VM.CloneSpec.disks-to-update
      InvalidArgument fault will be returned.
    - 'When clients pass a value of this structure as a parameter, the field must
      contain identifiers for the resource type: vcenter.vm.hardware.Disk. When operations
      return a value of this structure as a result, the field will contain identifiers
      for the resource type: vcenter.vm.hardware.Disk.'
    elements: str
    type: list
  disks_to_update:
    description:
    - Map of Disks to Update.
    - If unset, all disks will copied to the datastore specified in the VM.ClonePlacementSpec.datastore
      field of VM.CloneSpec.placement. If the same identifier is in VM.CloneSpec.disks-to-remove
      InvalidArgument fault will be thrown.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be an identifier for the resource type: vcenter.vm.hardware.Disk.
      When operations return a value of this structure as a result, the key in the
      field map will be an identifier for the resource type: vcenter.vm.hardware.Disk.'
    elements: str
    type: list
  floppies:
    description:
    - List of floppy drives.
    - If unset, no floppy drives will be created.
    elements: str
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
      configuring a virtual machine. Required with I(state=['create'])
    type: str
  guest_customization_spec:
    description:
    - Guest customization spec to apply to the virtual machine after the virtual machine
      is deployed.
    - If unset, the guest operating system is not customized after clone.
    - 'Validate attributes are:'
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
    - The Hardware.Version enumerated type defines the valid virtual hardware versions
      for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual
      machine hardware versions (1003746)).
    type: str
  memory:
    description:
    - Memory configuration.
    - If unset, guest-specific default values will be used.
    - 'Validate attributes are:'
    - ' - C(hot_add_enabled) (bool): Flag indicating whether adding memory while the
      virtual machine is running should be enabled. '
    - ' Some guest operating systems may consume more resources or perform less efficiently
      when they run on hardware that supports adding memory while the machine is running. '
    - ' This field may only be modified if the virtual machine is not powered on.'
    - If unset, the value is unchanged.
    - ' - C(size_MiB) (int): New memory size in mebibytes. '
    - ' The supported range of memory sizes is constrained by the configured guest
      operating system and virtual hardware version of the virtual machine. '
    - ' If the virtual machine is running, this value may only be changed if Memory.Info.hot-add-enabled
      is true, and the new memory size must satisfy the constraints specified by Memory.Info.hot-add-increment-size-mib
      and Memory.Info.hot-add-limit-mib.'
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
    elements: str
    type: list
  nics_to_update:
    description:
    - Map of NICs to update.
    - If unset, no NICs will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be an identifier for the resource type: vcenter.vm.hardware.Ethernet.
      When operations return a value of this structure as a result, the key in the
      field map will be an identifier for the resource type: vcenter.vm.hardware.Ethernet.'
    elements: str
    type: list
  parallel_ports:
    description:
    - List of parallel ports.
    - If unset, no parallel ports will be created.
    elements: str
    type: list
  parallel_ports_to_update:
    description:
    - Map of parallel ports to Update.
    - If unset, no parallel ports will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be an identifier for the resource type: vcenter.vm.hardware.ParallelPort.
      When operations return a value of this structure as a result, the key in the
      field map will be an identifier for the resource type: vcenter.vm.hardware.ParallelPort.'
    elements: str
    type: list
  path:
    description:
    - 'Path to the virtual machine''s configuration file on the datastore corresponding
      to {@link #datastore).'
    - If unset, VM.RegisterSpec.datastore must also be unset and VM.RegisterSpec.datastore-path
      must be set.
    type: str
  placement:
    description:
    - Virtual machine placement information.
    - If this field is unset, the system will use the values from the source virtual
      machine. If specified, each field will be used for placement. If the fields
      result in disjoint placement the operation will fail. If the fields along with
      the other existing placement of the virtual machine result in disjoint placement
      the operation will fail.
    - 'Validate attributes are:'
    - ' - C(cluster) (str): Cluster into which the virtual machine should be placed. '
    - ' If VM.ComputePlacementSpec.cluster and VM.ComputePlacementSpec.resource-pool
      are both specified, VM.ComputePlacementSpec.resource-pool must belong to VM.ComputePlacementSpec.cluster. '
    - ' If VM.ComputePlacementSpec.cluster and VM.ComputePlacementSpec.host are both
      specified, VM.ComputePlacementSpec.host must be a member of VM.ComputePlacementSpec.cluster.'
    - If VM.ComputePlacementSpec.resource-pool or VM.ComputePlacementSpec.host is
      specified, it is recommended that this field be unset.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: ClusterComputeResource. When operations
      return a value of this structure as a result, the field will be an identifier
      for the resource type: ClusterComputeResource.'
    - ' - C(datastore) (str): Datastore on which the virtual machine''s configuration
      state should be stored. This datastore will also be used for any virtual disks
      that are created as part of the virtual machine creation operation.'
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose suitable storage for the virtual machine; if storage
      cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Datastore. When operations return a
      value of this structure as a result, the field will be an identifier for the
      resource type: Datastore.'
    - ' - C(folder) (str): Virtual machine folder into which the virtual machine should
      be placed.'
    - This field is currently required. In the future, if this field is unset, the
      system will attempt to choose a suitable folder for the virtual machine; if
      a folder cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: Folder. When operations return a value
      of this structure as a result, the field will be an identifier for the resource
      type: Folder.'
    - ' - C(host) (str): Host onto which the virtual machine should be placed. '
    - ' If VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.resource-pool
      are both specified, VM.ComputePlacementSpec.resource-pool must belong to VM.ComputePlacementSpec.host. '
    - ' If VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.cluster are both
      specified, VM.ComputePlacementSpec.host must be a member of VM.ComputePlacementSpec.cluster.'
    - This field may be unset if VM.ComputePlacementSpec.resource-pool or VM.ComputePlacementSpec.cluster
      is specified. If unset, the system will attempt to choose a suitable host for
      the virtual machine; if a host cannot be chosen, the virtual machine creation
      operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: HostSystem. When operations return a
      value of this structure as a result, the field will be an identifier for the
      resource type: HostSystem.'
    - ' - C(resource_pool) (str): Resource pool into which the virtual machine should
      be placed.'
    - This field is currently required if both VM.ComputePlacementSpec.host and VM.ComputePlacementSpec.cluster
      are unset. In the future, if this field is unset, the system will attempt to
      choose a suitable resource pool for the virtual machine; if a resource pool
      cannot be chosen, the virtual machine creation operation will fail.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: ResourcePool. When operations return
      a value of this structure as a result, the field will be an identifier for the
      resource type: ResourcePool.'
    type: dict
  power_on:
    description:
    - Attempt to perform a VM.CloneSpec.power-on after clone.
    - If unset, the virtual machine will not be powered on.
    type: bool
  sata_adapters:
    description:
    - List of SATA adapters.
    - If unset, any adapters necessary to connect the virtual machine's storage devices
      will be created; this includes any devices that explicitly specify a SATA host
      bus adapter, as well as any devices that do not specify a host bus adapter if
      the guest's preferred adapter type is SATA.
    elements: str
    type: list
  scsi_adapters:
    description:
    - List of SCSI adapters.
    - If unset, any adapters necessary to connect the virtual machine's storage devices
      will be created; this includes any devices that explicitly specify a SCSI host
      bus adapter, as well as any devices that do not specify a host bus adapter if
      the guest's preferred adapter type is SCSI. The type of the SCSI adapter will
      be a guest-specific default type.
    elements: str
    type: list
  serial_ports:
    description:
    - List of serial ports.
    - If unset, no serial ports will be created.
    elements: str
    type: list
  serial_ports_to_update:
    description:
    - Map of serial ports to Update.
    - If unset, no serial ports will be updated.
    - 'When clients pass a value of this structure as a parameter, the key in the
      field map must be an identifier for the resource type: vcenter.vm.hardware.SerialPort.
      When operations return a value of this structure as a result, the key in the
      field map will be an identifier for the resource type: vcenter.vm.hardware.SerialPort.'
    elements: str
    type: list
  source:
    description:
    - Virtual machine to InstantClone from.
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: VirtualMachine. When operations return
      a value of this structure as a result, the field will be an identifier for the
      resource type: VirtualMachine. Required with I(state=[''clone'', ''instant_clone''])'
    type: str
  state:
    choices:
    - clone
    - create
    - delete
    - instant_clone
    - register
    - relocate
    - unregister
    description: []
    type: str
  storage_policy:
    description:
    - The VM.StoragePolicySpec structure contains information about the storage policy
      that is to be associated with the virtual machine home (which contains the configuration
      and log files).
    - 'If unset the datastore default storage policy (if applicable) is applied. Currently
      a default storage policy is only supported by object datastores : VVol and vSAN.
      For non-object datastores, if unset then no storage policy would be associated
      with the virtual machine home.'
    - 'Validate attributes are:'
    - ' - C(policy) (str): Identifier of the storage policy which should be associated
      with the virtual machine.'
    - 'When clients pass a value of this structure as a parameter, the field must
      be an identifier for the resource type: vcenter.StoragePolicy. When operations
      return a value of this structure as a result, the field will be an identifier
      for the resource type: vcenter.StoragePolicy.'
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
    - 'The parameter must be an identifier for the resource type: VirtualMachine.
      Required with I(state=[''delete'', ''relocate'', ''unregister''])'
    type: str
author:
- Goneri Le Bouder (@goneri) <goneri@lebouder.net>
version_added: 1.0.0
requirements:
- python >= 3.6
- aiohttp
"""

EXAMPLES = """
- name: _Wait for the vcenter server
  vcenter_vm_info:
  retries: 1
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
    state: create
- name: Delete some VM
  vcenter_vm:
    state: delete
    vm: '{{ item.vm }}'
  with_items: '{{ existing_vms.value }}'
"""

IN_QUERY_PARAMETER = []

import socket
import json
from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
    get_device_info,
    list_devices,
    exists,
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
    }

    argument_spec["bios_uuid"] = {"type": "str"}
    argument_spec["boot"] = {"type": "dict"}
    argument_spec["boot_devices"] = {"type": "list", "elements": "str"}
    argument_spec["cdroms"] = {"type": "list", "elements": "str"}
    argument_spec["cpu"] = {"type": "dict"}
    argument_spec["datastore"] = {"type": "str"}
    argument_spec["datastore_path"] = {"type": "str"}
    argument_spec["disconnect_all_nics"] = {"type": "bool"}
    argument_spec["disks"] = {"type": "list", "elements": "str"}
    argument_spec["disks_to_remove"] = {"type": "list", "elements": "str"}
    argument_spec["disks_to_update"] = {"type": "list", "elements": "str"}
    argument_spec["floppies"] = {"type": "list", "elements": "str"}
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
    argument_spec["nics"] = {"type": "list", "elements": "str"}
    argument_spec["nics_to_update"] = {"type": "list", "elements": "str"}
    argument_spec["parallel_ports"] = {"type": "list", "elements": "str"}
    argument_spec["parallel_ports_to_update"] = {"type": "list", "elements": "str"}
    argument_spec["path"] = {"type": "str"}
    argument_spec["placement"] = {"type": "dict"}
    argument_spec["power_on"] = {"type": "bool"}
    argument_spec["sata_adapters"] = {"type": "list", "elements": "str"}
    argument_spec["scsi_adapters"] = {"type": "list", "elements": "str"}
    argument_spec["serial_ports"] = {"type": "list", "elements": "str"}
    argument_spec["serial_ports_to_update"] = {"type": "list", "elements": "str"}
    argument_spec["source"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": [
            "clone",
            "create",
            "delete",
            "instant_clone",
            "register",
            "relocate",
            "unregister",
        ],
    }
    argument_spec["storage_policy"] = {"type": "dict"}
    argument_spec["vm"] = {"type": "str"}

    return argument_spec


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def build_url(params):

    return ("https://{vcenter_hostname}" "/rest/vcenter/vm").format(**params)


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _clone(params, session):
    accepted_fields = [
        "disks_to_remove",
        "disks_to_update",
        "guest_customization_spec",
        "name",
        "placement",
        "power_on",
        "source",
    ]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm?action=clone&vmw-task=true".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "clone")


async def _create(params, session):
    accepted_fields = [
        "boot",
        "boot_devices",
        "cdroms",
        "cpu",
        "disks",
        "floppies",
        "guest_OS",
        "hardware_version",
        "memory",
        "name",
        "nics",
        "parallel_ports",
        "placement",
        "sata_adapters",
        "scsi_adapters",
        "serial_ports",
        "storage_policy",
    ]
    _json = await exists(params, session, build_url(params))
    if _json:
        return await update_changed_flag(_json, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm".format(**params)
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (resp.status in [200, 201]) and ("value" in _json):
            if isinstance(_json["value"], dict):
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = await get_device_info(params, session, _url, _id)
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}".format(
        **params
    ) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _instant_clone(params, session):
    accepted_fields = [
        "bios_uuid",
        "disconnect_all_nics",
        "name",
        "nics_to_update",
        "parallel_ports_to_update",
        "placement",
        "serial_ports_to_update",
        "source",
    ]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm?action=instant-clone".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "instant_clone")


async def _register(params, session):
    accepted_fields = ["datastore", "datastore_path", "name", "path", "placement"]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm?action=register".format(**params)
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "register")


async def _relocate(params, session):
    accepted_fields = ["disks", "placement"]
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}?action=relocate&vmw-task=true".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "relocate")


async def _unregister(params, session):
    _url = "https://{vcenter_hostname}/rest/vcenter/vm/{vm}?action=unregister".format(
        **params
    ) + gen_args(params, IN_QUERY_PARAMETER)
    async with session.post(_url) as resp:
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
