from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from views import UserService
from wsgiref.simple_server import make_server

# Application setup
application = Application(
    [UserService],
    tns='api.users',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# WSGI Application
wsgi_application = WsgiApplication(application)

# Server setup
if __name__ == '__main__':
    server = make_server('127.0.0.1', 8000, wsgi_application)
    print("SOAP server running on http://127.0.0.1:8000")
    server.serve_forever()
