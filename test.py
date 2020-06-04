from __future__ import print_function
import requests
from getpass import getpass
from pprint import pprint

# uri for request
uri = "https://cert-manager.com/api/report/v1/ssl-certificates"
# auth info
username = "redacted"
password = getpass()
customerUri = "redacted"

# authentication headers
headers = {"login":username,
           "password":password,
           "customerUri": customerUri}

# report specification
report_data = {"from":"2020-06-02T00:00:00.000Z",
                "to":"2020-06-09T00:00:00.000Z",
                "organizationIds":[],
                "certificateStatus":0, # any
                #"certificateRequestSource":[], # Client Admin
                "certificateDateAttribute":3 # Expiration date
                }

# get our report
r = requests.post(uri, headers=headers, json=report_data)

print(r.text)
report = r.json()['reports']
#print(r.text)

for certificate in report:
    pprint(certificate)