import requests

# URL del archivo PHP que genera el contenido M3U
url = 'https://raw.githubusercontent.com/vijay-iptv/tv/refs/heads/main/public/index.php'

try:
    # Hacer la solicitud GET a la URL
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener el contenido
        m3u_content = response.text
        
        # Guardar el contenido en un archivo
        with open('lista.m3u', 'w') as file:
            file.write(m3u_content)
        
        print("La lista M3U ha sido creada con éxito.")
    else:
        print(f"Error al hacer la solicitud: {response.status_code}")

except Exception as e:
    print(f"Ocurrió un error: {e}")