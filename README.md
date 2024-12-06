# MACsniffer
Script en Python para localizar una dirección MAC en una red de switches Cisco, utilizando SSH y Netmiko para identificar el switch y puerto donde está conectada.

# Datos
Muñoz Ramirez Angel

Conmutacion y Enrutamiento de Redes

M.C Eliud Bueno Moreno

Universidad Politécnica de Durango

# Requisitos 
Antes de poder ejectutar nuestro codigo de Pyhton necestiamos cumplir algunos requisitos minimos, lo primero y principal seria tener instalada la libreria de Netmiko.
Aparte de estos se nececita:
- Tener interconexión entre cada equipo de red
- Tener conexión por SSH en cada equipo de red
- Debe de estar acitvado el comando CDP RUN
- El equipo desde donde se ejecutará el codigo debe de tener conexión en la red y poder conectarse por SSH

# Búsqueda de una Dirección MAC en una Red de Switches Cisco
Este script permite localizar una dirección MAC específica en una red de switches Cisco utilizando conexiones SSH. La búsqueda comienza en un switch inicial y, si la dirección MAC está en un puerto conectado a otro switch, el programa sigue al switch vecino hasta encontrar la dirección.

## Requisitos
- Bibliotecas necesarias: Netmiko (para SSH), Pandas (para tablas).
- Configuración previa: Los switches deben permitir SSH y los comandos show mac address-table, show cdp neighbors, y show cdp neighbors detail deben estar habilitados.

## Funciones
### buscar_mac(switch, mac_a_buscar)

Busca la dirección MAC en un switch y, si es necesario, retorna datos del switch vecino.

- Conexión: Establece conexión SSH con el switch usando Netmiko.
- Comandos ejecutados:
  - show mac address-table: Busca la dirección MAC.
  - show cdp neighbors y show cdp neighbors detail: Obtiene detalles del switch vecino.
  - show version: Extrae información del switch actual.
- Resultados:
  - Si encuentra la MAC, verifica si el puerto está conectado a otro switch.
  - Si hay un vecino, retorna sus datos para continuar la búsqueda.
  - Si no hay vecino, registra el switch donde está la MAC.

### localizar_mac(mac_a_buscar, switch_inicial)
Inicia la búsqueda en el switch inicial y sigue explorando vecinos hasta localizar la dirección MAC o agotar las conexiones.

## Tabla de Resultados
Los resultados se almacenan en una lista (tabla) y se presentan con Pandas en formato de tabla.
