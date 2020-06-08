from __future__ import print_function
import requests
from getpass import getpass
from pprint import pprint
import os
import sys
import ConfigParser
from datetime import datetime, timedelta
import json

# get application path
APP_LOCATION = os.path.dirname(os.path.dirname(sys.argv[0]))
config_default = APP_LOCATION + "/default/cert-manager.conf"
config_local = APP_LOCATION + "/local/cert-manager.conf"

# read values in from config file
config = ConfigParser.ConfigParser()
config.read([config_default, config_local])
try:
    customerUri = config.get("cert-manager", "customerUri")
    login = config.get("cert-manager", "login")
    password = config.get("cert-manager", "password")
    time_range = int(config.get("cert-manager", "time_range"))
except:
    sys.exit("values missing from cert-manager.conf")  

# uri for request
uri = "https://cert-manager.com/api/report/v1/ssl-certificates"
# # auth info
# username = "redacted"
# password = getpass()
# customerUri = "redacted"

# calculate start and end times for certificate retrieval
time_format = "%Y-%m-%dT%H:%M:%S.000Z"
now = datetime.utcnow()
start_time = now.strftime(time_format)
end_datetime = now + timedelta(days=time_range)
end_time = end_datetime.strftime(time_format)


# authentication headers
headers = {"login":login,
           "password":password,
           "customerUri": customerUri}

# report specification
report_data = {"from":start_time,
                "to":end_time,
                "organizationIds":[],
                "certificateStatus":0, # any
                #"certificateRequestSource":[], # Client Admin
                "certificateDateAttribute":3 # Expiration date
                }

# get our report
r = requests.post(uri, headers=headers, json=report_data)

#print(r.text)
report = r.json()['reports']

for certificate in report:
    print(json.dumps(certificate))