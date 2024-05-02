import mysql.connector
import paramiko
import time
import re

# Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="iotw4m.duckdns.org",
    user="root",
    password="radius",
    database="w4m"
)

cursor = conexion.cursor()

# Ingresar el dato a buscar
n = input('Numero de Habitacion: ')

# Consulta SQL con parámetros
consulta = "SELECT ONU_SN FROM ONT_S WHERE DEVICE_DESC = %s"
cursor.execute(consulta, (n,))

# Obtener los resultados
resultados = cursor.fetchone()

# Mostrar los resultados
if resultados:
    for resultado in resultados:
        print(resultado)
        sn = resultado
else:
    print("No se encontraron resultados para el dato ingresado.")

# Cerrar la conexión
conexion.close()

# Datos de conexión OLT ----- Hotel Paraiso
hostname = '194.79.91.17'
port = 8060
username = 'root'
password = 'W1f14m3d1a'

try:
    # Establecer la conexión SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port, username, password)

    # Abrir un canal SSH
    chan = ssh.invoke_shell()

    # Enviar comandos y recibir respuestas ('ont restore-factory 2 10')
    commands = ['enable', 'config', 'interface gpon 0/0', f'show ont info by-sn {sn}']
    for cmd in commands:
        chan.send(cmd + '\n')
        time.sleep(1)
        response = chan.recv(1024).decode()
        print(response)

finally:

    # Utilizar expresiones regulares para encontrar la frase "not online"
    match = re.search(r'\bnot online\b', response)

# Cerrar la conexión SSH
    chan.close()
    ssh.close()

