.. _vmware.vmware_rest.appliance_infraprofile_configs_module:


*************************************************
vmware.vmware_rest.appliance_infraprofile_configs
*************************************************

**Exports the desired profile specification.**


Version added: 2.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Exports the desired profile specification.



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
                    <b>description</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Custom description provided by the user.</div>
                        <div>If unset description will be empty.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>encryption_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Encryption Key to encrypt/decrypt profiles.</div>
                        <div>If unset encryption will not be used for the profile.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profiles</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Profiles to be exported/imported.</div>
                        <div>If unset or empty, all profiles will be returned.</div>
                        <div>When clients pass a value of this structure as a parameter, the field must contain the id of resources returned by <span class='module'>vmware.vmware_rest.appliance_infraprofile_configs</span>.</div>
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
                    <b>state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>export</li>
                        </ul>
                </td>
                <td>
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
    </table>
    <br/>


Notes
-----

.. note::
   - Tested on vSphere 7.0.2



Examples
--------

.. code-block:: yaml

    - name: Export the ApplianceManagement profile
      vmware.vmware_rest.appliance_infraprofile_configs:
        state: export
        profiles:
        - ApplianceManagement
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
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Export the ApplianceManagement profile</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&quot;action&quot;:&quot;RESTART_SERVICE&quot;,&quot;productName&quot;:&quot;VMware vCenter Server&quot;,&quot;creationTime&quot;:&quot;2022-11-23T20:11:00+0000&quot;,&quot;version&quot;:&quot;7.0.3.00800&quot;,&quot;profiles&quot;:{&quot;ApplianceManagement&quot;:{&quot;action&quot;:&quot;RESTART_SERVICE&quot;,&quot;actionOn&quot;:{&quot;VC_SERVICES&quot;:[&quot;applmgmt&quot;],&quot;SYSTEMD&quot;:[&quot;sendmail&quot;,&quot;rsyslog&quot;]},&quot;description&quot;:&quot;Appliance Mangment Service&quot;,&quot;version&quot;:&quot;7.0&quot;,&quot;config&quot;:{&quot;/etc/applmgmt/appliance/appliance.conf&quot;:{&quot;Is shell Enabled&quot;:true,&quot;Shell Expiration Time&quot;:9,&quot;TimeSync Mode (Host/NTP)&quot;:&quot;NTP&quot;},&quot;/etc/ntp.conf&quot;:{&quot;Time servers&quot;:&quot;time.nist.gov&quot;},&quot;/etc/shadow&quot;:{&quot;root&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;bin&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;daemon&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;messagebus&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-bus-proxy&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-journal-gateway&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-journal-remote&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-journal-upload&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-network&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-resolve&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;systemd-timesync&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;nobody&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;rpc&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;sshd&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;ntp&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;smmsp&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;apache&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;tftp&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;named&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vmdird&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;sso-user&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;dnsmasq&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;observability&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vdtc&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vmafdd-user&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vmcad-user&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;pod&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vmonapi&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;envoy&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vpostgres&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;lookupsvc&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;cis-license&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;pschealth&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;netdumper&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vapiEndpoint&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vpxd-svcs&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;certauth&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;certmgr&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;infraprofile&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;topologysvc&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;trustmanagement&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vpxd&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;analytics&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;eam&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;sps&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;deploy&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;updatemgr&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vlcm&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vmcam&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vsan-health&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vsm&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vsphere-ui&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vtsdbuser&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;vstatsuser&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;&quot;},&quot;wcp&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;content-library&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;imagebuilder&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;perfcharts&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vpgmonusr&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;vtsdbmonusr&quot;:{&quot;maximumDays&quot;:&quot;&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;zuul&quot;:{&quot;maximumDays&quot;:&quot;90&quot;,&quot;warningDays&quot;:&quot;7&quot;},&quot;Send Waring before this No of Days.&quot;:null,&quot;Password validity (days)&quot;:null},&quot;/etc/sysconfig/clock&quot;:{&quot;Time zone&quot;:&quot;\&quot;Etc/UTC\&quot;&quot;,&quot;UTC&quot;:&quot;1&quot;},&quot;/usr/bin/systemctl/sshd.service&quot;:{&quot;Enable SSH&quot;:&quot;true&quot;},&quot;/etc/mail/sendmail.cf&quot;:{&quot;SMTP Port&quot;:null,&quot;Mail server&quot;:null},&quot;/etc/vmware-syslog/syslog.conf&quot;:{&quot;Port [2]&quot;:null,&quot;Port [1]&quot;:null,&quot;Port [0]&quot;:null,&quot;Protocol [2]&quot;:null,&quot;Remote Syslog Host [1]&quot;:null,&quot;Protocol [1]&quot;:null,&quot;Remote Syslog Host [0]&quot;:null,&quot;Protocol [0]&quot;:null,&quot;Remote Syslog Host [2]&quot;:null},&quot;/etc/pam.d/system-auth&quot;:{&quot;Deny Login after these many Unsuccessful Attempts.&quot;:null,&quot;Unlock root after (seconds)&quot;:null,&quot;On Error Login will be.&quot;:null,&quot;Include Root user for SSH lockout.&quot;:null,&quot;Unlock user after (seconds)&quot;:null}},&quot;name&quot;:&quot;ApplianceManagement&quot;}}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
