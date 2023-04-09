import kerberos
import requests


class KerberosClient:
    def __init__(self, service):
        self.service = service

    def get_service_authenticator_from_response(r: requests.Response):
        auth_header = r.headers["WWW-Authenticate"]
        # auth_header is under the form negotiate {service_authenticator}
        return auth_header.split(" ")[1]

    def kerberos_handshake(self, url):
        try:
            _, krb_context = kerberos.authGSSClientInit(self.service)
            kerberos.authGSSClientStep(krb_context, "")
            # grab the service ticket
            negotiate_details = kerberos.authGSSClientResponse(krb_context)
            # setup the auth header to use the kerberos ticket
            headers = {"Authorization": "Negotiate " + negotiate_details}

            # make the request
            response = requests.get(url, headers=headers)

            # authenticate the service
            service_auth = KerberosClient.get_service_authenticator_from_response(
                response)
            kerberos.authGSSClientStep(krb_context, service_auth)
            kerberos.authGSSClientClean(krb_context)

            return response
        except Exception as err:
            print("Something is wrong with the ticket: " + err)
            return None
