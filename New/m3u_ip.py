import os
import re
import sys
import requests
from dotenv import load_dotenv

def main():
    # Verificar argumento de IP
    if len(sys.argv) != 2:
        print("Uso: python m3u_ip.py <79.144.187.114>")
        return
    ip_destino = sys.argv[1]

    # Cargar variables del archivo .env
    load_dotenv()
    m3u_url = os.environ.get('M3U_URL_SECRET')
    if not m3u_url:
        print("Error: la variable de entorno 'M3U_URL_SECRET' no está definida.")
        return

    print(f"Descargando la lista M3U desde: {m3u_url}")
    response = requests.get(m3u_url)
    if response.status_code != 200:
        print(f"Error al descargar el archivo M3U: {response.status_code}")
        return

    modified_lines = []
    for line in response.text.splitlines():
        # Modificar el grupo como antes
        if 'group-title="' in line:
            line = re.sub(r'group-title="(?!Z5 )([^"]+)"', r'group-title="Z5 \1"', line)
        # Si quieres agregar la IP como parámetro a los streams, descomenta esto:
        # if line.startswith('http'):
        #     sep = '&' if '?' in line else '?'
        #     line = f"{line}{sep}ip={ip_destino}"
        modified_lines.append(line)

    output_filename = f'all_tv_{ip_destino}.m3u'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(modified_lines))
    print(f"Archivo {output_filename} generado correctamente para la IP {ip_destino}.")

if __name__ == "__main__":
    main()
