from zeep import Client

cliente = Client("http://127.0.0.1:8000/?wsdl")

for codigo in ["LIB-001", "LIB-002", "LIB-999"]:
    titulo = cliente.service.buscar_titulo(codigo)
    cantidad = cliente.service.ejemplares_disponibles(codigo)
    disponible = cliente.service.hay_disponibilidad(codigo)

    print(codigo, titulo, cantidad, disponible, sep=" | ")

