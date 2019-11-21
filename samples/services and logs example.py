# -------------------------------------------------------------------------
# Copyright (c) PTC Inc. All rights reserved.
# See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

# IoT Gateway Example - Simple example on how to manage a connection and 
# exectute various calls for the IoT Gateway components of the Kepware
# configuration API

from kepconfig import connection
from kepconfig.connectivity import channel, device
import kepconfig.iot_gateway as IoT
from kepconfig.iot_gateway import agent, iot_items
import json
import datetime

# Channel and Device name to be used
ch_name = 'ControlLogix_Channel'
dev_name = 'Device1'
device_IP = '192.168.1.100'


# This creates a server reference that is used to target all modifications of 
# the Kepware configuration
server = connection.server(host = '127.0.0.1', port = 57412, user = 'Administrator', pw = '')

# This Reinitializes Kepware's Server Runtime process, similar to manually reinitializing
# using the Configuration UI or the Administrator tool.

print('{} - {}'.format("Execute Reinitialize Service", server.reinitialize()))

# Add a Channel using the "ControlLogix Driver" with a ControlLogix 5500 family device. 
# This will be used to demonstrate the "Auto Tag Generation" service available.
channel_data = {
    "common.ALLTYPES_NAME": ch_name,
    "common.ALLTYPES_DESCRIPTION": "This is the test channel created",
    "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
    "devices": [
        {
            "common.ALLTYPES_NAME": dev_name,
            "common.ALLTYPES_DESCRIPTION": "Hello, new description",
            "servermain.MULTIPLE_TYPES_DEVICE_DRIVER": "Allen-Bradley Controllogix Ethernet",
            "servermain.DEVICE_MODEL": 0,
            "servermain.DEVICE_ID_STRING": "<{}>,1,0".format(device_IP)
        }
    ]
}
print("{} - {}".format("Adding Controllogix Channel and Device", channel.add_channel(server,channel_data)))

# Execute the "TagGeneration" service available in the Kepware Configuration API
print("{} - {}".format("Executing ATG for Controllogix Device", device.auto_tag_gen(server, '{}.{}'.format(ch_name, dev_name))))

# Get Event Log from Kepware instance.
print("{} - {}".format("Here is the last Event Log Entry", json.dumps(server.get_event_log(1, None, None), indent=4)))
print("{} - {}".format("Here are the last 25 entries of the Event Log", json.dumps(server.get_event_log(25, datetime.datetime.fromisoformat('2019-11-03T23:35:23.000'), datetime.datetime.now()), indent=4)))

#Get Configuration API Transaction Log
print("{} - {}".format("Here is the last API Transaction Log Entry", json.dumps(server.get_trans_log(1, None, None), indent=4)))
