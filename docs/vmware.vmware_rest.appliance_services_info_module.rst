.. _vmware.vmware_rest.appliance_services_info_module:


******************************************
vmware.vmware_rest.appliance_services_info
******************************************

**Returns the state of a service.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Returns the state of a service.



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
                    <b>service</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>identifier of the service whose state is being queried. Required with <em>state=[&#x27;get&#x27;]</em></div>
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
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: List all the services
      vmware.vmware_rest.appliance_services_info:
      register: result

    - name: Get information about ntpd
      vmware.vmware_rest.appliance_services_info:
        service: ntpd
      register: result



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
                            <div>List all the services</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;appliance-shutdown&#x27;: {&#x27;description&#x27;: &#x27;/etc/rc.local.shutdown Compatibility&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;atftpd&#x27;: {&#x27;description&#x27;: &#x27;The tftp server serves files using the trivial file transfer protocol.&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;auditd&#x27;: {&#x27;description&#x27;: &#x27;Security Auditing Service&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;cloud-config&#x27;: {&#x27;description&#x27;: &#x27;Apply the settings specified in cloud-config&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;cloud-init&#x27;: {&#x27;description&#x27;: &#x27;Initial cloud-init job (metadata service crawler)&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;cloud-init-local&#x27;: {&#x27;description&#x27;: &#x27;Initial cloud-init job (pre-networking)&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;crond&#x27;: {&#x27;description&#x27;: &#x27;Command Scheduler&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;dbus&#x27;: {&#x27;description&#x27;: &#x27;D-Bus System Message Bus&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;dm-event&#x27;: {&#x27;description&#x27;: &#x27;Device-mapper event daemon&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dnsmasq&#x27;: {&#x27;description&#x27;: &#x27;A lightweight, caching DNS proxy&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;dracut-cmdline&#x27;: {&#x27;description&#x27;: &#x27;dracut cmdline hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-initqueue&#x27;: {&#x27;description&#x27;: &#x27;dracut initqueue hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-mount&#x27;: {&#x27;description&#x27;: &#x27;dracut mount hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-pre-mount&#x27;: {&#x27;description&#x27;: &#x27;dracut pre-mount hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-pre-pivot&#x27;: {&#x27;description&#x27;: &#x27;dracut pre-pivot and cleanup hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-pre-trigger&#x27;: {&#x27;description&#x27;: &#x27;dracut pre-trigger hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-pre-udev&#x27;: {&#x27;description&#x27;: &#x27;dracut pre-udev hook&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;dracut-shutdown&#x27;: {&#x27;description&#x27;: &#x27;Restore /run/initramfs on shutdown&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;emergency&#x27;: {&#x27;description&#x27;: &#x27;Emergency Shell&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;getty@tty2&#x27;: {&#x27;description&#x27;: &#x27;DCUI&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;haveged&#x27;: {&#x27;description&#x27;: &#x27;Entropy Daemon based on the HAVEGE algorithm&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;initrd-cleanup&#x27;: {&#x27;description&#x27;: &#x27;Cleaning Up and Shutting Down Daemons&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;initrd-parse-etc&#x27;: {&#x27;description&#x27;: &#x27;Reload Configuration from the Real Root&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;initrd-switch-root&#x27;: {&#x27;description&#x27;: &#x27;Switch Root&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;initrd-udevadm-cleanup-db&#x27;: {&#x27;description&#x27;: &#x27;Cleanup udevd DB&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;irqbalance&#x27;: {&#x27;description&#x27;: &#x27;irqbalance daemon&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;kmod-static-nodes&#x27;: {&#x27;description&#x27;: &#x27;Create list of required static device nodes for the current kernel&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lsassd&#x27;: {&#x27;description&#x27;: &#x27;Likewise Security and Authentication Subsystem&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lvm2-activate&#x27;: {&#x27;description&#x27;: &#x27;LVM2 activate volume groups&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lvm2-lvmetad&#x27;: {&#x27;description&#x27;: &#x27;LVM2 metadata daemon&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lvm2-pvscan@253:2&#x27;: {&#x27;description&#x27;: &#x27;LVM2 PV scan on device 253:2&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lvm2-pvscan@253:4&#x27;: {&#x27;description&#x27;: &#x27;LVM2 PV scan on device 253:4&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;lwsmd&#x27;: {&#x27;description&#x27;: &#x27;Likewise Service Control Manager Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;ntpd&#x27;: {&#x27;description&#x27;: &#x27;Network Time Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;observability&#x27;: {&#x27;description&#x27;: &#x27;VMware Observability Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;rc-local&#x27;: {&#x27;description&#x27;: &#x27;/etc/rc.d/rc.local Compatibility&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;rescue&#x27;: {&#x27;description&#x27;: &#x27;Rescue Shell&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;rsyslog&#x27;: {&#x27;description&#x27;: &#x27;System Logging Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;sendmail&#x27;: {&#x27;description&#x27;: &#x27;Sendmail Mail Transport Agent&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;sshd&#x27;: {&#x27;description&#x27;: &#x27;OpenSSH Daemon&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;sshd-keygen&#x27;: {&#x27;description&#x27;: &#x27;Generate sshd host keys&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;syslog-ng&#x27;: {&#x27;description&#x27;: &#x27;System Logger Daemon&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;sysstat&#x27;: {&#x27;description&#x27;: &#x27;Resets System Activity Logs&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;sysstat-collect&#x27;: {&#x27;description&#x27;: &#x27;system activity accounting tool&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;sysstat-summary&#x27;: {&#x27;description&#x27;: &#x27;Generate a daily summary of process accounting&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-ask-password-console&#x27;: {&#x27;description&#x27;: &#x27;Dispatch Password Requests to Console&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-ask-password-wall&#x27;: {&#x27;description&#x27;: &#x27;Forward Password Requests to Wall&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-binfmt&#x27;: {&#x27;description&#x27;: &#x27;Set Up Additional Binary Formats&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-fsck-root&#x27;: {&#x27;description&#x27;: &#x27;File System Check on Root Device&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-hostnamed&#x27;: {&#x27;description&#x27;: &#x27;Hostname Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-hwdb-update&#x27;: {&#x27;description&#x27;: &#x27;Rebuild Hardware Database&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-initctl&#x27;: {&#x27;description&#x27;: &#x27;initctl Compatibility Daemon&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-journal-catalog-update&#x27;: {&#x27;description&#x27;: &#x27;Rebuild Journal Catalog&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-journal-flush&#x27;: {&#x27;description&#x27;: &#x27;Flush Journal to Persistent Storage&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-journald&#x27;: {&#x27;description&#x27;: &#x27;Journal Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-logind&#x27;: {&#x27;description&#x27;: &#x27;Login Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-machine-id-commit&#x27;: {&#x27;description&#x27;: &#x27;Commit a transient machine-id on disk&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-modules-load&#x27;: {&#x27;description&#x27;: &#x27;Load Kernel Modules&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-networkd&#x27;: {&#x27;description&#x27;: &#x27;Network Service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-networkd-wait-online&#x27;: {&#x27;description&#x27;: &#x27;Wait for Network to be Configured&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-quotacheck&#x27;: {&#x27;description&#x27;: &#x27;File System Quota Check&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-random-seed&#x27;: {&#x27;description&#x27;: &#x27;Load/Save Random Seed&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-remount-fs&#x27;: {&#x27;description&#x27;: &#x27;Remount Root and Kernel File Systems&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-resolved&#x27;: {&#x27;description&#x27;: &#x27;Network Name Resolution&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-sysctl&#x27;: {&#x27;description&#x27;: &#x27;Apply Kernel Variables&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-tmpfiles-clean&#x27;: {&#x27;description&#x27;: &#x27;Cleanup of Temporary Directories&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-tmpfiles-setup&#x27;: {&#x27;description&#x27;: &#x27;Create Volatile Files and Directories&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-tmpfiles-setup-dev&#x27;: {&#x27;description&#x27;: &#x27;Create Static Device Nodes in /dev&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-udev-trigger&#x27;: {&#x27;description&#x27;: &#x27;udev Coldplug all Devices&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-udevd&#x27;: {&#x27;description&#x27;: &#x27;udev Kernel Device Manager&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-update-done&#x27;: {&#x27;description&#x27;: &#x27;Update is Completed&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-update-utmp&#x27;: {&#x27;description&#x27;: &#x27;Update UTMP about System Boot/Shutdown&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-update-utmp-runlevel&#x27;: {&#x27;description&#x27;: &#x27;Update UTMP about System Runlevel Changes&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;systemd-user-sessions&#x27;: {&#x27;description&#x27;: &#x27;Permit User Sessions&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;systemd-vconsole-setup&#x27;: {&#x27;description&#x27;: &#x27;Setup Virtual Console&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;vami-lighttp&#x27;: {&#x27;description&#x27;: &#x27;vami-lighttp.service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vgauthd&#x27;: {&#x27;description&#x27;: &#x27;VGAuth Service for open-vm-tools&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;vmafdd&#x27;: {&#x27;description&#x27;: &#x27;LSB: Authentication Framework Daemon&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmcad&#x27;: {&#x27;description&#x27;: &#x27;LSB: Start and Stop vmca&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmdird&#x27;: {&#x27;description&#x27;: &#x27;LSB: Start and Stop vmdir&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmtoolsd&#x27;: {&#x27;description&#x27;: &#x27;Service for virtual machines hosted on VMware&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}, &#x27;vmware-firewall&#x27;: {&#x27;description&#x27;: &#x27;VMware Firewall service&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmware-pod&#x27;: {&#x27;description&#x27;: &#x27;VMware Pod Service.&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmware-vdtc&#x27;: {&#x27;description&#x27;: &#x27;VMware vSphere Distrubuted Tracing Collector&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}, &#x27;vmware-vmon&#x27;: {&#x27;description&#x27;: &#x27;VMware Service Lifecycle Manager&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
