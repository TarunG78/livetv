import os
import requests

# Leer la URL del enlace M3U desde la variable de entorno
url = os.getenv('URL_FILE_LINK')

if not url:
    print("La variable de entorno URL_FILE_LINK no está definida.")
    exit(1)

try:
    response = requests.get(url)
    if response.status_code == 200:
        m3u_content = response.text
        with open('lista_varios.m3u', 'w') as file:
            file.write(m3u_content)
        print("La lista_varios.m3u ha sido creada con éxito.")
    else:
        print(f"Error al hacer la solicitud: {response.status_code}")
except Exception as e:
    print(f"Ocurrió un error: {e}")