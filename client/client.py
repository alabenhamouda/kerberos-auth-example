#!/usr/bin/python3
from KerberosClient import KerberosClient

krb = KerberosClient("host@kdc.insat.tn")

response = krb.kerberos_handshake("http://kdc.insat.tn:5000/")

if response is not None:
    print("status code: " + str(response.status_code))
    print("response:")
    print(response.content.decode("utf-8"))
