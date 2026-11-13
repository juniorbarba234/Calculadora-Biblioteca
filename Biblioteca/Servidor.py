from spyne import Application, ServiceBase, rpc, Unicode, Integer, Boolean
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

titulos = {
    "LIB-001": "Cien años de soledad",
    "LIB-002": "La vorágine"
}

ejemplares = {
    "LIB-001": 3,
    "LIB-002": 0
}

class Biblioteca(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def buscar_titulo(ctx, codigo):
        return titulos.get(codigo, "No encontrado")

    @rpc(Unicode, _returns=Integer)
    def ejemplares_disponibles(ctx, codigo):
        return ejemplares.get(codigo, 0)

    @rpc(Unicode, _returns=Boolean)
    def hay_disponibilidad(ctx, codigo):
        return ejemplares.get(codigo, 0) > 0

aplicacion = Application(
    [Biblioteca],
    tns="biblioteca",
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

servidor = make_server(
    "127.0.0.1",
    8000,
    WsgiApplication(aplicacion)
)

print("Servidor listo: http://127.0.0.1:8000/?wsdl")
servidor.serve_forever()
