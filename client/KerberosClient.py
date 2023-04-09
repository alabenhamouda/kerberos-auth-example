import kerberos
import requests


class KerberosClient:
    class ClientHandler:
        def __init__(self) -> None:
            self.headers = {}

        def set_auth_header(self, negotiate_details):
            self.headers["Authorization"] = "Negotiate " + negotiate_details

        def call(self) -> requests.Response:
            pass

    class GetClientHandler(ClientHandler):
        def __init__(self, url):
            super().__init__()
            self.url = url

        def call(self) -> requests.Response:
            return requests.get(self.url, headers=self.headers)

    def __init__(self, service):
        self.service = service

    def get_service_authenticator_from_response(r: requests.Response):
        auth_header = r.headers["WWW-Authenticate"]
        # auth_header is under the form negotiate {service_authenticator}
        return auth_header.split(" ")[1]

    def kerberos_handshake(self, handler: ClientHandler):
        try:
            _, krb_context = kerberos.authGSSClientInit(self.service)
            kerberos.authGSSClientStep(krb_context, "")
            # grab the service ticket
            negotiate_details = kerberos.authGSSClientResponse(krb_context)
            # setup the auth header to use the kerberos ticket
            handler.set_auth_header(negotiate_details=negotiate_details)

            # make the request
            response = handler.call()

            # authenticate the service
            service_auth = KerberosClient.get_service_authenticator_from_response(
                response)
            kerberos.authGSSClientStep(krb_context, service_auth)
            kerberos.authGSSClientClean(krb_context)

            return response
        except Exception as err:
            print("Something is wrong with the ticket: " + err)
            return None

    def get(self, url):
        handler = KerberosClient.GetClientHandler(url)
        return self.kerberos_handshake(handler)
