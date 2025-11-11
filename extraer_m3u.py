import requests

# URL del archivo M3U fuente
url = 'https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/in.m3u' 

try:
    # Hacer la solicitud GET a la URL
    response = requests.get(url)
    
    if response.status_code == 200:
        m3u_content = response.text

        # Procesar líneas para añadir group-title="ALL INDIA FREE" a cada canal
        new_lines = []
        for line in m3u_content.splitlines():
            if line.startswith("#EXTINF"):
                # Verifica si ya tiene group-title
                if 'group-title="' in line:
                    # Reemplaza el valor de group-title por "ALL INDIA FREE"
                    import re
                    line = re.sub(r'group-title=".*?"', 'group-title="ALL INDIA FREE"', line)
                else:
                    # Añade group-title="ALL INDIA FREE" antes de la coma
                    idx = line.find(',')
                    if idx != -1:
                        line = line[:idx] + ' group-title="ALL INDIA FREE"' + line[idx:]
            new_lines.append(line)

        # Reconstruir el archivo M3U
        new_content = "\n".join(new_lines)

        # Guardar el resultado
        with open('lista_varios.m3u', 'w', encoding='utf-8') as file:
            file.write(new_content)
            
        print("La lista_varios.m3u ha sido creada con éxito con el grupo 'ALL INDIA FREE'.")

    else:
        print(f"Error al hacer la solicitud: {response.status_code}")

except Exception as e:
    print(f"Ocurrió un error: {e}")
