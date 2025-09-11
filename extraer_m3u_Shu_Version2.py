import os
import requests

def descargar_m3u():
    url = os.getenv('URL_FILE_LINK')
    if not url:
        print("La variable de entorno URL_FILE_LINK no está definida.")
        exit(1)
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            m3u_content = response.text
            if "#EXTM3U" not in m3u_content:
                print("El contenido descargado no parece ser un archivo M3U válido.")
                return
            filename = 'lista_varios.m3u'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(m3u_content)
            print(f"El archivo {filename} ha sido creado con éxito.")
        else:
            print(f"Error al hacer la solicitud: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    descargar_m3u()
