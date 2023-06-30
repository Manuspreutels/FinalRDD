# Observaciones
TP Final de Redes de Datos. Desarrollo de APIs, uso de protocolos de internet y formatos de datos.
## Requerimientos

- Python 3.11
- Antes de ejecutar, instalar los siguientes paquetes:
  - requests: `pip install requests`
  - fastapi: `pip install fastapi`
  - uvicorn: `pip install uvicorn`

## Cómo ejecutar

### Ejecución del servidor

Ejecuta el siguiente comando en una terminal: `uvicorn --host [IP] servidor:app --reload`
, donde [IP] puede ser 127.0.0.1 para que solo sea accesible de forma local (mismo dispositivo),
o 0.0.0.0 para que pueda ser visto por otros dispositivos en la red.

### Manejo del cliente

Ejecuta el siguiente comando en una terminal: `python cliente.py`.  
En el cliente se te pedirá ingresar la IP del servidor. Si se ejecutó con [IP] = 0.0.0.0,
esta será la dirección IPv4 del dispositivo host. Después de esto, el manejo del cliente es intuitivo.
