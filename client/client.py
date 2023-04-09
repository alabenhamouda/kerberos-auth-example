#!/usr/bin/python3
from KerberosClient import KerberosClient

krb = KerberosClient("host@kdc.insat.tn")

data = {"path": "dest/txt/test.txt"}
response = krb.post(
    "http://kdc.insat.tn:5000/directory", data)

if response is not None:
    print("status code: " + str(response.status_code))
    print("response:")
    print(response.content.decode("utf-8"))
