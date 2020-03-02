Missing features
================

- folder: there is no `create` operation for `/vcenter/folder`. As a result we cannot provide a `vcenter_folder` module.
- cluster: same problem
- datastore: same problem. For instance, we cannot mount a NFS volume
- network modules (vswitch, dvswitch, portgroup), those are covered by the NSX-T API.

Also
====

- when we try the same resource two time in a row, the second call fails with `com.vmware.vapi.std.errors.already_exists`. But the endpoint does not resource the ID of the existing resource. So we need to do another operation to retrieve it.
- OpenAPI 3, e.g: https://koumoul.com/s/tileserver/api/v1/api-docs.json https://apis.guru/awesome-openapi3/category.html
- Some module names conflict with community.vmware, e.g: vcenter_folder
