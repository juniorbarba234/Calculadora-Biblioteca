from zeep import Client
from zeep.exceptions import Fault, ValidationError

cliente = Client("http://127.0.0.1:8001/?wsdl")

casos = [
    ("Pedido válido", {"cliente": "Ana", "lineas": {"LineaPedido": [
        {"producto": "P001", "cantidad": 2},
        {"producto": "P002", "cantidad": 1}
    ]}}),
    ("Stock insuficiente", {"cliente": "Ana", "lineas": {"LineaPedido": [
        {"producto": "P002", "cantidad": 99}
    ]}}),
    ("Producto inexistente", {"cliente": "Ana", "lineas": {"LineaPedido": [
        {"producto": "P999", "cantidad": 1}
    ]}}),
    ("Sin líneas", {"cliente": "Ana"}),
    ("Sin cliente", {"lineas": {"LineaPedido": [
        {"producto": "P001", "cantidad": 1}
    ]}})
]

for nombre, pedido in casos:
    print(nombre)
    try:
        resultado = cliente.service.registrar_pedido(pedido)
        print(resultado.id, resultado.cliente, resultado.total)
    except Fault as error:
        print(error.code, error.message)
    except ValidationError:
        print("ValidationError: faltan datos obligatorios.")

for id in [1, 50]:
    print("Consultar pedido", id)
    try:
        resultado = cliente.service.consultar_pedido(id)
        print(resultado.id, resultado.cliente, resultado.total)
    except Fault as error:
        print(error.code, error.message)
