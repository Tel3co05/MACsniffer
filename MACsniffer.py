from netmiko import ConnectHandler
import pandas as pd

# Datos de ejemplo
mac_compu = "7c4d.8f55.56b9"  # Dirección MAC a buscar
tabla = [{"Nombre": False, "Puerto": False, 'MAC': False}]  # Tabla de resultados

# Comandos
comando_macs = "show mac address-table"
comando_neighbors = "show cdp neighbors"
comando_neighbors_detail = "show cdp neighbors detail"
comando_version = "show version"

# Función para buscar la MAC en un switch
def buscar_mac(switch, mac_a_buscar):
    # Conexión SSH al switch
    conexion = ConnectHandler(**switch)
    print(f"Conectando a {switch['host']}...")

    # Ejecutar comandos
    salida_macs = conexion.send_command(comando_macs, use_textfsm=True)
    salida_neighbors = conexion.send_command(comando_neighbors, use_textfsm=True)
    salida_neighbors_detail = conexion.send_command(comando_neighbors_detail, use_textfsm=True)
    salida_version = conexion.send_command(comando_version, use_textfsm=True)

    # Buscar la MAC en la tabla
    for mac_entry in salida_macs:
        if mac_entry['destination_address'] == mac_a_buscar:
            tabla[0]['MAC'] = mac_entry['destination_address']
            tabla[0]['Puerto'] = mac_entry['destination_port'][0]
            puerto_mac = mac_entry['destination_port'][0]
            puerto = puerto_mac[2:]  # Extraer el número del puerto a partir del índice 2
            print(f"MAC encontrada en puerto: {puerto_mac}")
            break
    else:
        print(f"MAC {mac_a_buscar} no encontrada en {switch['host']}.")
        conexion.disconnect()
        return False  # MAC no encontrada

    # Verificar si el puerto conecta a otro switch
    for vecino in salida_neighbors:
        puerto_vecino = vecino['local_interface'][4:]  # Extraer desde el índice 4

        if puerto_vecino == puerto:  # Comparar con el puerto asociado a la MAC
            print(f"Puerto {puerto_mac} conecta al switch vecino: {vecino['neighbor_name']}")
            # Buscar IP del switch vecino
            for vecino_detail in salida_neighbors_detail:
                puerto_vecino = vecino_detail['local_interface'][12:]  # Extraer desde el índice 12
                if puerto == puerto_vecino:  # Verificar si el puerto coincide
                    ip_vecino = vecino_detail['mgmt_address']  # Tomar la IP de gestión
                    print(f"Puerto encontrado: {puerto_vecino}, IP del vecino: {ip_vecino}")
                    conexion.disconnect()
                    return {
                        'host': ip_vecino,
                        'username': switch['username'],
                        'password': switch['password'],
                        'device_type': switch['device_type'],
                    }
            else:
                print("Puerto no encontrado.")
            break

    # Si no hay vecino, agregar información del switch actual
    tabla[0]['Nombre'] = salida_version[0]['hostname']
    print(f"MAC localizada en switch {tabla[0]['Nombre']}.")
    conexion.disconnect()
    return None  # Finaliza si no hay vecino

# Bucle para buscar la MAC en switches vecinos
def localizar_mac(mac_a_buscar, switch_inicial):
    switch_actual = switch_inicial
    while switch_actual:
        switch_actual = buscar_mac(switch_actual, mac_a_buscar)

# Datos del switch inicial
switch_inicial = {
    'host': '192.168.1.2',
    'username': 'cisco',
    'password': 'cisco',
    'device_type': 'cisco_ios'
}

# Iniciar la búsqueda
localizar_mac(mac_compu, switch_inicial)

# Mostrar tabla de resultados
print("-"*40)
df = pd.DataFrame(tabla)
print(df)