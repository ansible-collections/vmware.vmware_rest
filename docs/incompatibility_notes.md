# Incompatibility Notes

When a module is regenerated, a line in the module's notes section will tell you what version of API the module was generated from, as well as if
the module is compatible with a specific version of vSphere.

This document contains a list of all known incompatiblities with the current modules and specific vSphere versions.

## 8.0.2

### appliance_localaccounts_globalpolicy
  - GET /appliance/local-accounts/global-policy
  - PUT /appliance/local-accounts/global-policy
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'managed_at_fleet' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'fail_interval_between_attempts' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_lowercase_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_special_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'length_of_lockout_period_in_seconds' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_uppercase_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_length' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'failed_attempt_count_before_account_lockout' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_numerics_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'prior_password_remember_count' absent from target request schema

### content_configuration
  - GET /content/configuration
  - PATCH /content/configuration
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'priority_transfer_threads_pool_size' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_nfc_max_concurrent_transfers_per_host' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'maximum_concurrent_item_syncs_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'name' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_refresh_interval' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_throttling_bandwidth_total' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_start_hour_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'priority_transfer_threads_pool_size_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_enabled_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_refresh_interval_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_stop_hour_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'constraints' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_setting_refresh_interval_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_nfc_max_concurrent_transfers_per_host_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_threads_pool_size' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_threads_pool_size_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'reboot_required' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_throttling_bandwidth_total_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_setting_refresh_interval' absent from target request schema

### vcenter_ovf_libraryitem
  - POST /vcenter/ovf/library-item
  - POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy
  - POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'library_item_source_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'folder_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'host_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'resource_pool_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'type' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'library_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'subnet_mappings' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'accept_all_eula' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'library_item_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'tag_params' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'tags' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter: module sends 'library_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter: module sends 'library_item_id' absent from target request schema

### vcenter_vmtemplate_libraryitems
  - GET /vcenter/vm-template/library-items/{template_library_item}
  - POST /vcenter/vm-template/library-items
  - POST /vcenter/vm-template/library-items/{template_library_item}?action=deploy
  - [Body field removed or renamed] POST /vcenter/vm-template/library-items/{template_library_item}?action=deploy: module sends 'tags' absent from target request schema


## 7.0.3

### appliance_localaccounts_globalpolicy
  - GET /appliance/local-accounts/global-policy
  - PUT /appliance/local-accounts/global-policy
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'failed_attempt_count_before_account_lockout' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_special_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'managed_at_fleet' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'fail_interval_between_attempts' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_lowercase_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_numerics_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'length_of_lockout_period_in_seconds' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'prior_password_remember_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_uppercase_char_count' absent from target request schema
  - [Body field removed or renamed] PUT /appliance/local-accounts/global-policy: module sends 'minimum_length' absent from target request schema

### appliance_vmon_service
  - GET /appliance/vmon/service
  - GET /appliance/vmon/service/{service}
  - PATCH /appliance/vmon/service/{service}
  - POST /appliance/vmon/service/{service}/start
  - POST /appliance/vmon/service/{service}/stop
  - [Missing method] PATCH /appliance/vmon/service/{service}: path exists as /rest/appliance/vmon/service but PATCH not supported

### content_configuration
  - GET /content/configuration
  - PATCH /content/configuration
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_setting_refresh_interval_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_stop_hour_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_nfc_max_concurrent_transfers_per_host_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'priority_transfer_threads_pool_size' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_setting_refresh_interval' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_nfc_max_concurrent_transfers_per_host' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_throttling_bandwidth_total_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'priority_transfer_threads_pool_size_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_throttling_bandwidth_total' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'name' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_refresh_interval' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'maximum_concurrent_item_syncs_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_enabled_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_start_hour_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'reboot_required' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'constraints' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'automatic_sync_refresh_interval_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_threads_pool_size_setting' absent from target request schema
  - [Body field removed or renamed] PATCH /content/configuration: module sends 'transfer_threads_pool_size' absent from target request schema

### vcenter_ovf_libraryitem
  - POST /vcenter/ovf/library-item
  - POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy
  - POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'resource_pool_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'host_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'library_item_source_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item: module sends 'folder_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'library_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'vm_config_spec' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'provider' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'tag_params' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'tags' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'accept_all_eula' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'subnet_mappings' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'type' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'xml' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=deploy: module sends 'library_item_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter: module sends 'library_item_id' absent from target request schema
  - [Body field removed or renamed] POST /vcenter/ovf/library-item/{ovf_library_item_id}?action=filter: module sends 'library_id' absent from target request schema

### vcenter_vmtemplate_libraryitems
  - GET /vcenter/vm-template/library-items/{template_library_item}
  - POST /vcenter/vm-template/library-items
  - POST /vcenter/vm-template/library-items/{template_library_item}?action=deploy
  - [Body field removed or renamed] POST /vcenter/vm-template/library-items/{template_library_item}?action=deploy: module sends 'tags' absent from target request schema
