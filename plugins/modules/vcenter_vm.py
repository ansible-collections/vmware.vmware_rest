from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = "author:\n- Ansible VMware team\ndescription: Handle resource of type vcenter_vm\nextends_documentation_fragment: []\nmodule: vcenter_vm\nnotes:\n- Tested on vSphere 7.0\noptions:\n  bios_uuid:\n    description:\n    - '128-bit SMBIOS UUID of a virtual machine represented as a hexadecimal string\n      in \"12345678-abcd-1234-cdef-123456789abc\" format.\n\n      If unset, will be generated.'\n    type: str\n  boot:\n    description:\n    - 'Boot configuration.\n\n      If unset, guest-specific default values will be used.'\n    - 'Validate attributes are:'\n    - ' - C(delay) (int): Delay in milliseconds before beginning the firmware boot\n      process when the virtual machine is powered on. This delay may be used to provide\n      a time window for users to connect to the virtual machine console and enter\n      BIOS setup mode.\n\n      If unset, default value is 0.'\n    - ' - C(efi_legacy_boot) (bool): Flag indicating whether to use EFI legacy boot\n      mode.\n\n      If unset, defaults to value that is recommended for the guest OS and is supported\n      for the virtual hardware version.'\n    - ' - C(enter_setup_mode) (bool): Flag indicating whether the firmware boot process\n      should automatically enter setup mode the next time the virtual machine boots.\n      Note that this flag will automatically be reset to false once the virtual machine\n      enters setup mode.\n\n      If unset, the value is unchanged.'\n    - ' - C(network_protocol) (str): The Boot.NetworkProtocol enumerated type defines\n      the valid network boot protocols supported when booting a virtual machine with\n      EFI firmware over the network.'\n    - ' - C(retry) (bool): Flag indicating whether the virtual machine should automatically\n      retry the boot process after a failure.\n\n      If unset, default value is false.'\n    - ' - C(retry_delay) (int): Delay in milliseconds before retrying the boot process\n      after a failure; applicable only when Boot.Info.retry is true.\n\n      If unset, default value is 10000.'\n    - ' - C(type) (str): The Boot.Type enumerated type defines the valid firmware\n      types for a virtual machine.'\n    type: dict\n  boot_devices:\n    description:\n    - 'Boot device configuration.\n\n      If unset, a server-specific boot sequence will be used.'\n    type: list\n  cdroms:\n    description:\n    - 'List of CD-ROMs.\n\n      If unset, no CD-ROM devices will be created.'\n    type: list\n  cpu:\n    description:\n    - 'CPU configuration.\n\n      If unset, guest-specific default values will be used.'\n    - 'Validate attributes are:'\n    - ' - C(cores_per_socket) (int): New number of CPU cores per socket. The number\n      of CPU cores in the virtual machine must be a multiple of the number of cores\n      per socket.\n\n      If unset, the value is unchanged.'\n    - \" - C(count) (int): New number of CPU cores. The number of CPU cores in the\\\n      \\ virtual machine must be a multiple of the number of cores per socket. \\n The\\\n      \\ supported range of CPU counts is constrained by the configured guest operating\\\n      \\ system and virtual hardware version of the virtual machine. \\n\\n If the virtual\\\n      \\ machine is running, the number of CPU cores may only be increased if Cpu.Info.hot-add-enabled\\\n      \\ is true, and may only be decreased if Cpu.Info.hot-remove-enabled is true.\\n\\\n      \\nIf unset, the value is unchanged.\"\n    - \" - C(hot_add_enabled) (bool): Flag indicating whether adding CPUs while the\\\n      \\ virtual machine is running is enabled. \\n This field may only be modified\\\n      \\ if the virtual machine is powered off.\\n\\nIf unset, the value is unchanged.\"\n    - \" - C(hot_remove_enabled) (bool): Flag indicating whether removing CPUs while\\\n      \\ the virtual machine is running is enabled. \\n This field may only be modified\\\n      \\ if the virtual machine is powered off.\\n\\nIf unset, the value is unchanged.\"\n    type: dict\n  datastore:\n    description:\n    - 'Identifier of the datastore on which the virtual machine''s configuration state\n      is stored.\n\n      If unset, VM.RegisterSpec.path must also be unset and VM.RegisterSpec.datastore-path\n      must be set.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: Datastore. When operations return a value\n      of this structure as a result, the field will be an identifier for the resource\n      type: Datastore.'\n    type: str\n  datastore_path:\n    description:\n    - 'Datastore path for the virtual machine''s configuration file in the format\n      \"[datastore name] path\". For example \"[storage1] Test-VM/Test-VM.vmx\".\n\n      If unset, both VM.RegisterSpec.datastore and VM.RegisterSpec.path must be set.'\n    type: str\n  disconnect_all_nics:\n    description:\n    - 'Indicates whether all NICs on the destination virtual machine should be disconnected\n      from the newtwork\n\n      If unset, connection status of all NICs on the destination virtual machine will\n      be the same as on the source virtual machine.'\n    type: bool\n  disks:\n    description:\n    - 'Individual disk relocation map.\n\n      If unset, all disks will migrate to the datastore specified in the VM.RelocatePlacementSpec.datastore\n      field of VM.RelocateSpec.placement.\n\n      When clients pass a value of this structure as a parameter, the key in the field\n      map must be an identifier for the resource type: vcenter.vm.hardware.Disk. When\n      operations return a value of this structure as a result, the key in the field\n      map will be an identifier for the resource type: vcenter.vm.hardware.Disk.'\n    type: list\n  disks_to_remove:\n    description:\n    - 'Set of Disks to Remove.\n\n      If unset, all disks will be copied. If the same identifier is in VM.CloneSpec.disks-to-update\n      InvalidArgument fault will be returned.\n\n      When clients pass a value of this structure as a parameter, the field must contain\n      identifiers for the resource type: vcenter.vm.hardware.Disk. When operations\n      return a value of this structure as a result, the field will contain identifiers\n      for the resource type: vcenter.vm.hardware.Disk.'\n    type: list\n  disks_to_update:\n    description:\n    - 'Map of Disks to Update.\n\n      If unset, all disks will copied to the datastore specified in the VM.ClonePlacementSpec.datastore\n      field of VM.CloneSpec.placement. If the same identifier is in VM.CloneSpec.disks-to-remove\n      InvalidArgument fault will be thrown.\n\n      When clients pass a value of this structure as a parameter, the key in the field\n      map must be an identifier for the resource type: vcenter.vm.hardware.Disk. When\n      operations return a value of this structure as a result, the key in the field\n      map will be an identifier for the resource type: vcenter.vm.hardware.Disk.'\n    type: list\n  floppies:\n    description:\n    - 'List of floppy drives.\n\n      If unset, no floppy drives will be created.'\n    type: list\n  guest_OS:\n    choices:\n    - DOS\n    - WIN_31\n    - WIN_95\n    - WIN_98\n    - WIN_ME\n    - WIN_NT\n    - WIN_2000_PRO\n    - WIN_2000_SERV\n    - WIN_2000_ADV_SERV\n    - WIN_XP_HOME\n    - WIN_XP_PRO\n    - WIN_XP_PRO_64\n    - WIN_NET_WEB\n    - WIN_NET_STANDARD\n    - WIN_NET_ENTERPRISE\n    - WIN_NET_DATACENTER\n    - WIN_NET_BUSINESS\n    - WIN_NET_STANDARD_64\n    - WIN_NET_ENTERPRISE_64\n    - WIN_LONGHORN\n    - WIN_LONGHORN_64\n    - WIN_NET_DATACENTER_64\n    - WIN_VISTA\n    - WIN_VISTA_64\n    - WINDOWS_7\n    - WINDOWS_7_64\n    - WINDOWS_7_SERVER_64\n    - WINDOWS_8\n    - WINDOWS_8_64\n    - WINDOWS_8_SERVER_64\n    - WINDOWS_9\n    - WINDOWS_9_64\n    - WINDOWS_9_SERVER_64\n    - WINDOWS_HYPERV\n    - WINDOWS_SERVER_2019\n    - FREEBSD\n    - FREEBSD_64\n    - FREEBSD_11\n    - FREEBSD_12\n    - FREEBSD_11_64\n    - FREEBSD_12_64\n    - REDHAT\n    - RHEL_2\n    - RHEL_3\n    - RHEL_3_64\n    - RHEL_4\n    - RHEL_4_64\n    - RHEL_5\n    - RHEL_5_64\n    - RHEL_6\n    - RHEL_6_64\n    - RHEL_7\n    - RHEL_7_64\n    - RHEL_8_64\n    - CENTOS\n    - CENTOS_64\n    - CENTOS_6\n    - CENTOS_6_64\n    - CENTOS_7\n    - CENTOS_7_64\n    - CENTOS_8_64\n    - ORACLE_LINUX\n    - ORACLE_LINUX_64\n    - ORACLE_LINUX_6\n    - ORACLE_LINUX_6_64\n    - ORACLE_LINUX_7\n    - ORACLE_LINUX_7_64\n    - ORACLE_LINUX_8_64\n    - SUSE\n    - SUSE_64\n    - SLES\n    - SLES_64\n    - SLES_10\n    - SLES_10_64\n    - SLES_11\n    - SLES_11_64\n    - SLES_12\n    - SLES_12_64\n    - SLES_15_64\n    - NLD_9\n    - OES\n    - SJDS\n    - MANDRAKE\n    - MANDRIVA\n    - MANDRIVA_64\n    - TURBO_LINUX\n    - TURBO_LINUX_64\n    - UBUNTU\n    - UBUNTU_64\n    - DEBIAN_4\n    - DEBIAN_4_64\n    - DEBIAN_5\n    - DEBIAN_5_64\n    - DEBIAN_6\n    - DEBIAN_6_64\n    - DEBIAN_7\n    - DEBIAN_7_64\n    - DEBIAN_8\n    - DEBIAN_8_64\n    - DEBIAN_9\n    - DEBIAN_9_64\n    - DEBIAN_10\n    - DEBIAN_10_64\n    - DEBIAN_11\n    - DEBIAN_11_64\n    - ASIANUX_3\n    - ASIANUX_3_64\n    - ASIANUX_4\n    - ASIANUX_4_64\n    - ASIANUX_5_64\n    - ASIANUX_7_64\n    - ASIANUX_8_64\n    - OPENSUSE\n    - OPENSUSE_64\n    - FEDORA\n    - FEDORA_64\n    - COREOS_64\n    - VMWARE_PHOTON_64\n    - OTHER_24X_LINUX\n    - OTHER_24X_LINUX_64\n    - OTHER_26X_LINUX\n    - OTHER_26X_LINUX_64\n    - OTHER_3X_LINUX\n    - OTHER_3X_LINUX_64\n    - OTHER_4X_LINUX\n    - OTHER_4X_LINUX_64\n    - OTHER_LINUX\n    - GENERIC_LINUX\n    - OTHER_LINUX_64\n    - SOLARIS_6\n    - SOLARIS_7\n    - SOLARIS_8\n    - SOLARIS_9\n    - SOLARIS_10\n    - SOLARIS_10_64\n    - SOLARIS_11_64\n    - OS2\n    - ECOMSTATION\n    - ECOMSTATION_2\n    - NETWARE_4\n    - NETWARE_5\n    - NETWARE_6\n    - OPENSERVER_5\n    - OPENSERVER_6\n    - UNIXWARE_7\n    - DARWIN\n    - DARWIN_64\n    - DARWIN_10\n    - DARWIN_10_64\n    - DARWIN_11\n    - DARWIN_11_64\n    - DARWIN_12_64\n    - DARWIN_13_64\n    - DARWIN_14_64\n    - DARWIN_15_64\n    - DARWIN_16_64\n    - DARWIN_17_64\n    - DARWIN_18_64\n    - DARWIN_19_64\n    - VMKERNEL\n    - VMKERNEL_5\n    - VMKERNEL_6\n    - VMKERNEL_65\n    - VMKERNEL_7\n    - AMAZONLINUX2_64\n    - CRXPOD_1\n    - OTHER\n    - OTHER_64\n    description:\n    - The {@name GuestOS} defines the valid guest operating system types used for\n      configuring a virtual machine. Required with I(state=['create'])\n    type: str\n  guest_customization_spec:\n    description:\n    - 'Guest customization spec to apply to the virtual machine after the virtual\n      machine is deployed.\n\n      If unset, the guest operating system is not customized after clone.'\n    - 'Validate attributes are:'\n    - ' - C(name) (str): Name of the customization specification.\n\n      If unset, no guest customization is performed.'\n    type: dict\n  hardware_version:\n    choices:\n    - VMX_03\n    - VMX_04\n    - VMX_06\n    - VMX_07\n    - VMX_08\n    - VMX_09\n    - VMX_10\n    - VMX_11\n    - VMX_12\n    - VMX_13\n    - VMX_14\n    - VMX_15\n    - VMX_16\n    - VMX_17\n    description:\n    - The Hardware.Version enumerated type defines the valid virtual hardware versions\n      for a virtual machine. See https://kb.vmware.com/s/article/1003746 (Virtual\n      machine hardware versions (1003746)).\n    type: str\n  memory:\n    description:\n    - 'Memory configuration.\n\n      If unset, guest-specific default values will be used.'\n    - 'Validate attributes are:'\n    - \" - C(hot_add_enabled) (bool): Flag indicating whether adding memory while the\\\n      \\ virtual machine is running should be enabled. \\n Some guest operating systems\\\n      \\ may consume more resources or perform less efficiently when they run on hardware\\\n      \\ that supports adding memory while the machine is running. \\n\\n This field\\\n      \\ may only be modified if the virtual machine is not powered on.\\n\\nIf unset,\\\n      \\ the value is unchanged.\"\n    - \" - C(size_MiB) (int): New memory size in mebibytes. \\n The supported range\\\n      \\ of memory sizes is constrained by the configured guest operating system and\\\n      \\ virtual hardware version of the virtual machine. \\n\\n If the virtual machine\\\n      \\ is running, this value may only be changed if Memory.Info.hot-add-enabled\\\n      \\ is true, and the new memory size must satisfy the constraints specified by\\\n      \\ Memory.Info.hot-add-increment-size-mib and Memory.Info.hot-add-limit-mib.\\n\\\n      \\nIf unset, the value is unchanged.\"\n    type: dict\n  name:\n    description:\n    - Name of the new virtual machine. Required with I(state=['clone', 'create', 'register',\n      'instant_clone'])\n    type: str\n  nics:\n    description:\n    - 'List of Ethernet adapters.\n\n      If unset, no Ethernet adapters will be created.'\n    type: list\n  nics_to_update:\n    description:\n    - 'Map of NICs to update.\n\n      If unset, no NICs will be updated.\n\n      When clients pass a value of this structure as a parameter, the key in the field\n      map must be an identifier for the resource type: vcenter.vm.hardware.Ethernet.\n      When operations return a value of this structure as a result, the key in the\n      field map will be an identifier for the resource type: vcenter.vm.hardware.Ethernet.'\n    type: list\n  parallel_ports:\n    description:\n    - 'List of parallel ports.\n\n      If unset, no parallel ports will be created.'\n    type: list\n  parallel_ports_to_update:\n    description:\n    - 'Map of parallel ports to Update.\n\n      If unset, no parallel ports will be updated.\n\n      When clients pass a value of this structure as a parameter, the key in the field\n      map must be an identifier for the resource type: vcenter.vm.hardware.ParallelPort.\n      When operations return a value of this structure as a result, the key in the\n      field map will be an identifier for the resource type: vcenter.vm.hardware.ParallelPort.'\n    type: list\n  path:\n    description:\n    - 'Path to the virtual machine''s configuration file on the datastore corresponding\n      to {@link #datastore).\n\n      If unset, VM.RegisterSpec.datastore must also be unset and VM.RegisterSpec.datastore-path\n      must be set.'\n    type: str\n  placement:\n    description:\n    - 'Virtual machine placement information.\n\n      If this field is unset, the system will use the values from the source virtual\n      machine. If specified, each field will be used for placement. If the fields\n      result in disjoint placement the operation will fail. If the fields along with\n      the placement values of the source virtual machine result in disjoint placement\n      the operation will fail.'\n    - 'Validate attributes are:'\n    - ' - C(datastore) (str): Datastore on which the InstantCloned virtual machine''s\n      configuration state should be stored. This datastore will also be used for any\n      virtual disks that are created as part of the virtual machine InstantClone operation.\n\n      If field is unset, the system will use the datastore of the source virtual machine.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: Datastore. When operations return a value\n      of this structure as a result, the field will be an identifier for the resource\n      type: Datastore.'\n    - ' - C(folder) (str): Virtual machine folder into which the InstantCloned virtual\n      machine should be placed.\n\n      If field is unset, the system will use the virtual machine folder of the source\n      virtual machine.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: Folder. When operations return a value\n      of this structure as a result, the field will be an identifier for the resource\n      type: Folder.'\n    - ' - C(resource_pool) (str): Resource pool into which the InstantCloned virtual\n      machine should be placed.\n\n      If field is unset, the system will use the resource pool of the source virtual\n      machine.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: ResourcePool. When operations return a\n      value of this structure as a result, the field will be an identifier for the\n      resource type: ResourcePool.'\n    type: dict\n  power_on:\n    description:\n    - 'Attempt to perform a VM.CloneSpec.power-on after clone.\n\n      If unset, the virtual machine will not be powered on.'\n    type: bool\n  sata_adapters:\n    description:\n    - 'List of SATA adapters.\n\n      If unset, any adapters necessary to connect the virtual machine''s storage devices\n      will be created; this includes any devices that explicitly specify a SATA host\n      bus adapter, as well as any devices that do not specify a host bus adapter if\n      the guest''s preferred adapter type is SATA.'\n    type: list\n  scsi_adapters:\n    description:\n    - 'List of SCSI adapters.\n\n      If unset, any adapters necessary to connect the virtual machine''s storage devices\n      will be created; this includes any devices that explicitly specify a SCSI host\n      bus adapter, as well as any devices that do not specify a host bus adapter if\n      the guest''s preferred adapter type is SCSI. The type of the SCSI adapter will\n      be a guest-specific default type.'\n    type: list\n  serial_ports:\n    description:\n    - 'List of serial ports.\n\n      If unset, no serial ports will be created.'\n    type: list\n  serial_ports_to_update:\n    description:\n    - 'Map of serial ports to Update.\n\n      If unset, no serial ports will be updated.\n\n      When clients pass a value of this structure as a parameter, the key in the field\n      map must be an identifier for the resource type: vcenter.vm.hardware.SerialPort.\n      When operations return a value of this structure as a result, the key in the\n      field map will be an identifier for the resource type: vcenter.vm.hardware.SerialPort.'\n    type: list\n  source:\n    description:\n    - 'Virtual machine to InstantClone from.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: VirtualMachine. When operations return\n      a value of this structure as a result, the field will be an identifier for the\n      resource type: VirtualMachine. Required with I(state=[''clone'', ''instant_clone''])'\n    type: str\n  state:\n    choices:\n    - instant_clone\n    - register\n    - clone\n    - relocate\n    - create\n    - unregister\n    - delete\n    description: []\n    type: str\n  storage_policy:\n    description:\n    - 'The VM.StoragePolicySpec structure contains information about the storage policy\n      that is to be associated with the virtual machine home (which contains the configuration\n      and log files).\n\n      If unset the datastore default storage policy (if applicable) is applied. Currently\n      a default storage policy is only supported by object datastores : VVol and vSAN.\n      For non-object datastores, if unset then no storage policy would be associated\n      with the virtual machine home.'\n    - 'Validate attributes are:'\n    - ' - C(policy) (str): Identifier of the storage policy which should be associated\n      with the virtual machine.\n\n      When clients pass a value of this structure as a parameter, the field must be\n      an identifier for the resource type: vcenter.StoragePolicy. When operations\n      return a value of this structure as a result, the field will be an identifier\n      for the resource type: vcenter.StoragePolicy.'\n    type: dict\n  vm:\n    description:\n    - 'Existing Virtual machine to relocate.\n\n      The parameter must be an identifier for the resource type: VirtualMachine. Required\n      with I(state=[''unregister'', ''delete'', ''relocate''])'\n    type: str\nrequirements:\n- python >= 3.6\nshort_description: Handle resource of type vcenter_vm\nversion_added: 1.0.0\n"
IN_QUERY_PARAMETER = []
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"])
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"])
        ),
        "vcenter_password": dict(
            type="str",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_certs": dict(
            type="bool",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }
    argument_spec["vm"] = {
        "type": "str",
        "operationIds": ["delete", "relocate", "unregister"],
    }
    argument_spec["storage_policy"] = {"type": "dict", "operationIds": ["create"]}
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
    argument_spec["source"] = {
        "type": "str",
        "operationIds": ["clone", "instant_clone"],
    }
    argument_spec["serial_ports_to_update"] = {
        "type": "list",
        "operationIds": ["instant_clone"],
    }
    argument_spec["serial_ports"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["scsi_adapters"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["sata_adapters"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["power_on"] = {"type": "bool", "operationIds": ["clone"]}
    argument_spec["placement"] = {
        "type": "dict",
        "operationIds": ["clone", "create", "instant_clone", "register", "relocate"],
    }
    argument_spec["path"] = {"type": "str", "operationIds": ["register"]}
    argument_spec["parallel_ports_to_update"] = {
        "type": "list",
        "operationIds": ["instant_clone"],
    }
    argument_spec["parallel_ports"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["nics_to_update"] = {
        "type": "list",
        "operationIds": ["instant_clone"],
    }
    argument_spec["nics"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["name"] = {
        "type": "str",
        "operationIds": ["clone", "create", "instant_clone", "register"],
    }
    argument_spec["memory"] = {"type": "dict", "operationIds": ["create"]}
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
        "operationIds": ["create"],
    }
    argument_spec["guest_customization_spec"] = {
        "type": "dict",
        "operationIds": ["clone"],
    }
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
        "operationIds": ["create"],
    }
    argument_spec["floppies"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["disks_to_update"] = {"type": "list", "operationIds": ["clone"]}
    argument_spec["disks_to_remove"] = {"type": "list", "operationIds": ["clone"]}
    argument_spec["disks"] = {"type": "list", "operationIds": ["create", "relocate"]}
    argument_spec["disconnect_all_nics"] = {
        "type": "bool",
        "operationIds": ["instant_clone"],
    }
    argument_spec["datastore_path"] = {"type": "str", "operationIds": ["register"]}
    argument_spec["datastore"] = {"type": "str", "operationIds": ["register"]}
    argument_spec["cpu"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["cdroms"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["boot_devices"] = {"type": "list", "operationIds": ["create"]}
    argument_spec["boot"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["bios_uuid"] = {"type": "str", "operationIds": ["instant_clone"]}
    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(((_url + "/") + _key)) as resp:
        _json = await resp.json()
        entry = _json["value"]
        entry["_key"] = _key
        return entry


async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if (params.get(k) is not None) and (device.get(k) != params.get(k)):
                break
        else:
            return device


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


def url(params):
    return "https://{vcenter_hostname}/rest/vcenter/vm".format(**params)


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
    if "clone" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
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
        if ("clone" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
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
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
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
        if ("create" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
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
    if "instant_clone" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
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
        if ("instant_clone" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "instant_clone")


async def _register(params, session):
    accepted_fields = ["datastore", "datastore_path", "name", "path", "placement"]
    if "register" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
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
        if ("register" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "register")


async def _relocate(params, session):
    accepted_fields = ["disks", "placement"]
    if "relocate" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
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
        if ("relocate" == "create") and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
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
