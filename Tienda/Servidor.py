from decimal import Decimal as Dinero
from spyne import Application, ServiceBase, rpc, Unicode, Integer, Decimal, ComplexModel, Array, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class LineaPedido(ComplexModel):
    producto = Unicode(min_occurs=1, nillable=False, min_len=1)
    cantidad = Integer(min_occurs=1, nillable=False, ge=1)

class Pedido(ComplexModel):
    cliente = Unicode(min_occurs=1, nillable=False, min_len=1)
    lineas = Array(LineaPedido.customize(min_occurs=1, nillable=False), min_occurs=1, nillable=False)

class Confirmacion(ComplexModel):
    id = Integer
    cliente = Unicode
    total = Decimal

precios = {"P001": Dinero("25.00"), "P002": Dinero("15.00")}
stock = {"P001": 10, "P002": 5}
pedidos = {}

class Tienda(ServiceBase):
    @rpc(Pedido.customize(min_occurs=1, nillable=False), _returns=Confirmacion)
    def registrar_pedido(ctx, pedido):
        if not pedido.cliente.strip():
            raise Fault("Client.DatosIncompletos", "El cliente no puede estar vacío.")

        cantidades = {}
        for linea in pedido.lineas:
            if linea.producto not in stock:
                raise Fault("Client.ProductoInexistente", "No existe el producto " + linea.producto)
            cantidades[linea.producto] = cantidades.get(linea.producto, 0) + linea.cantidad

        total = Dinero("0.00")
        for producto, cantidad in cantidades.items():
            if cantidad > stock[producto]:
                raise Fault("Client.StockInsuficiente", "No hay suficiente stock de " + producto)
            total += precios[producto] * cantidad

        for producto, cantidad in cantidades.items():
            stock[producto] -= cantidad

        id = len(pedidos) + 1
        confirmacion = Confirmacion(id=id, cliente=pedido.cliente, total=total)
        pedidos[id] = confirmacion
        print("Stock:", stock)
        return confirmacion

    @rpc(Integer(min_occurs=1, nillable=False), _returns=Confirmacion)
    def consultar_pedido(ctx, id):
        if id not in pedidos:
            raise Fault("Client.PedidoInexistente", "No existe el pedido solicitado.")
        return pedidos[id]

aplicacion = Application(
    [Tienda],
    tns="tienda",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11()
)

servidor = make_server("127.0.0.1", 8001, WsgiApplication(aplicacion))
print("Servidor listo: http://127.0.0.1:8001/?wsdl")
servidor.serve_forever()
