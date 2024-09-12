This test is temporary until automated testing can be put in place.

To run:

1. Create a `vars.yml` in this directory with variables specific to your environment. Possible variables to set can be found in `vmware_lookup/defaults/main.yml`, plus `vcenter_hostname`, `vcenter_username`, `vcenter_password`. Alternatively, you can set the authentication variables as env vars. For example, `VCENTER_HOSTNAME`, `VCENTER_USERNAME`, `VCENTER_PASSWORD`
2. Run `./runme.sh`
