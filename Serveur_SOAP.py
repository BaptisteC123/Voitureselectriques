from spyne import Application, rpc, ServiceBase,Integer, Unicode, Double, Array,ComplexModel
from spyne import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

import soap

class Calcul_Dist(ServiceBase):
    @rpc(Double,Double,Double,Double,_returns=Array(Double))
    def calcul_distance(ctx,lat1,lon1,lat2,lon2):
        result = soap.calcul_distance(lat1,lon1,lat2,lon2)
        return result

srv = Application([Calcul_Dist],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(srv)
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()

