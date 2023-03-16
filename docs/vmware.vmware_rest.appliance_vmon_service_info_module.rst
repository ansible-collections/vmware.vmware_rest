.. _vmware.vmware_rest.appliance_vmon_service_info_module:


**********************************************
vmware.vmware_rest.appliance_vmon_service_info
**********************************************

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
                        <div>identifier of the service whose state is being queried.</div>
                        <div>The parameter must be the id of a resource returned by <span class='module'>vmware.vmware_rest.appliance_vmon_service</span>. Required with <em>state=[&#x27;get&#x27;]</em></div>
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

    - name: Get information about a VMON service
      vmware.vmware_rest.appliance_vmon_service_info:
        service: vpxd
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
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>On success</td>
                <td>
                            <div>Get information about a VMON service</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;key&#x27;: &#x27;analytics&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.analytics.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.analytics.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;applmgmt&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.applmgmt.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.applmgmt.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;certificateauthority&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.certificateauthority.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;certificateathority.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.certificateauthority.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;certificatemanagement&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.certificatemanagement.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;certificatemanagement.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.certificatemanagement.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;cis-license&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.cis-license.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;The License Service is operational.&#x27;, &#x27;id&#x27;: &#x27;cis.license.health.ok&#x27;}], &#x27;name_key&#x27;: &#x27;cis.cis-license.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;content-library&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.content-library.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Database server connection is GREEN.&#x27;, &#x27;id&#x27;: &#x27;com.vmware.vdcs.vsphere-cs-lib.db_health_green&#x27;}], &#x27;name_key&#x27;: &#x27;cis.content-library.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;eam&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.eam.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;&#x27;, &#x27;id&#x27;: &#x27;cis.eam.statusOK&#x27;}], &#x27;name_key&#x27;: &#x27;cis.eam.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;envoy&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.envoy.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.envoy.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;hvc&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.hvc.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;hvc.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.hvc.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;imagebuilder&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.imagebuilder.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.imagebuilder.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;MANUAL&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;infraprofile&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.infraprofile.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;infraprofile.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.infraprofile.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;lookupsvc&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.lookupsvc.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.lookupsvc.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;netdumper&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.netdumper.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.netdumper.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;MANUAL&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;observability-vapi&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.observability-vapi.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;observability.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.observability-vapi.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;perfcharts&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.perfcharts.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY_WITH_WARNINGS&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;health.statsReoptInitalizer.illegalStateEx&#x27;, &#x27;id&#x27;: &#x27;health.statsReoptInitalizer.illegalStateEx&#x27;}], &#x27;name_key&#x27;: &#x27;cis.perfcharts.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;pschealth&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.pschealth.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.pschealth.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;rbd&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.rbd.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.rbd.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;MANUAL&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;rhttpproxy&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.rhttpproxy.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.rhttpproxy.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;sca&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.sca.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.sca.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;sps&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.sps.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.sps.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;statsmonitor&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.statsmonitor.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Appliance monitoring service is healthy.&#x27;, &#x27;id&#x27;: &#x27;com.vmware.applmgmt.mon.health.healthy&#x27;}], &#x27;name_key&#x27;: &#x27;cis.statsmonitor.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;sts&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.sts.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.sts.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;topologysvc&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.topologysvc.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;topologysvc.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.topologysvc.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;trustmanagement&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.trustmanagement.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;Health is GREEN&#x27;, &#x27;id&#x27;: &#x27;trustmanagement.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.trustmanagement.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;updatemgr&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.updatemgr.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.updatemgr.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vapi-endpoint&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vapi-endpoint.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;2022-11-23T20:10:44UTC&#x27;, &#x27;2022-11-23T20:10:46UTC&#x27;], &#x27;default_message&#x27;: &#x27;Configuration health status is created between 2022-11-23T20:10:44UTC and 2022-11-23T20:10:46UTC.&#x27;, &#x27;id&#x27;: &#x27;com.vmware.vapi.endpoint.healthStatusProducedTimes&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vapi-endpoint.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vcha&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vcha.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.vcha.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;DISABLED&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;vlcm&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vlcm.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.vlcm.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vmcam&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vmcam.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.vmcam.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;MANUAL&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;vmonapi&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vmonapi.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.vmonapi.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vmware-postgres-archiver&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vmware-postgres-archiver.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;VMware Archiver service is healthy.&#x27;, &#x27;id&#x27;: &#x27;cis.vmware-postgres-archiver.health.healthy&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vmware-postgres-archiver.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vmware-vpostgres&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vmware-vpostgres.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Service vmware-vpostgres is healthy.&#x27;, &#x27;id&#x27;: &#x27;cis.vmware-vpostgres.health.healthy&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vmware-vpostgres.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vpxd&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vpxd.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [&#x27;vCenter Server&#x27;, &#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;{0} health is {1}&#x27;, &#x27;id&#x27;: &#x27;vc.health.statuscode&#x27;}, {&#x27;args&#x27;: [&#x27;VirtualCenter Database&#x27;, &#x27;GREEN&#x27;], &#x27;default_message&#x27;: &#x27;{0} health is {1}&#x27;, &#x27;id&#x27;: &#x27;vc.health.statuscode&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vpxd.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vpxd-svcs&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vpxd-svcs.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Tagging service is in a healthy state&#x27;, &#x27;id&#x27;: &#x27;cis.tagging.health.status&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vpxd-svcs.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vsan-health&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vsan-health.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.vsan-health.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vsm&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vsm.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.vsm.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vsphere-ui&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vsphere-ui.ServiceDescription&#x27;, &#x27;name_key&#x27;: &#x27;cis.vsphere-ui.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STOPPED&#x27;}}, {&#x27;key&#x27;: &#x27;vstats&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vstats.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.vstats.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;vtsdb&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.vtsdb.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [{&#x27;args&#x27;: [], &#x27;default_message&#x27;: &#x27;Service vtsdb is healthy.&#x27;, &#x27;id&#x27;: &#x27;cis.vtsdb.health.healthy&#x27;}], &#x27;name_key&#x27;: &#x27;cis.vtsdb.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}, {&#x27;key&#x27;: &#x27;wcp&#x27;, &#x27;value&#x27;: {&#x27;description_key&#x27;: &#x27;cis.wcp.ServiceDescription&#x27;, &#x27;health&#x27;: &#x27;HEALTHY&#x27;, &#x27;health_messages&#x27;: [], &#x27;name_key&#x27;: &#x27;cis.wcp.ServiceName&#x27;, &#x27;startup_type&#x27;: &#x27;AUTOMATIC&#x27;, &#x27;state&#x27;: &#x27;STARTED&#x27;}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ansible Cloud Team (@ansible-collections)
