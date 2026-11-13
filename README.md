# Calculadora-Biblioteca

Actividad 4.1 de Arquitectura Orientada a Servicios.

## Biblioteca

Servicio SOAP con un catálogo en memoria y un cliente Zeep. Ofrece tres operaciones:

| Operación | Recibe | Devuelve |
|---|---|---|
| buscar_titulo | Código del libro | Título o "No encontrado" (string) |
| ejemplares_disponibles | Código del libro | Cantidad de ejemplares (integer) |
| hay_disponibilidad | Código del libro | True o False (boolean) |

El servidor está en `Biblioteca/Servidor.py` y el cliente en `Biblioteca/Cliente.py`.

Usar Python 3.10. En CMD, desde la carpeta del repositorio:

```cmd
py -3.10 -m pip install -r requirements.txt
py -3.10 Biblioteca\Servidor.py
```

Dejar el servidor abierto. En otra ventana de CMD, desde la misma carpeta:

```cmd
py -3.10 Biblioteca\Cliente.py
```

Contrato WSDL: http://127.0.0.1:8000/?wsdl

Resultado esperado:

```text
LIB-001 | Cien años de soledad | 3 | True
LIB-002 | La vorágine | 0 | False
LIB-999 | No encontrado | 0 | False
```

La calculadora se añadirá después.
