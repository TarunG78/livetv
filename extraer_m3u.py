import requests
import re
import os
import json

# Intenta cargar los sources desde el secret M3U_SOURCES
sources_json = os.environ.get("M3U_SOURCES")
if not sources_json:
    print("ERROR: No se encontró el secret M3U_SOURCES como variable de entorno.")
    exit(1)

try:
    sources = json.loads(sources_json)
except Exception as e:
    print(f"ERROR al decodificar el JSON de sources: {e}")
    exit(1)

def process_line(line, mode):
    if mode == 'none':
        return line
    if line.startswith("#EXTINF"):
        if mode == 'override':
            if 'group-title="' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="ALL INDIA FREE"', line)
            else:
                idx = line.find(',')
                if idx != -1:
                    line = line[:idx] + ' group-title="ALL INDIA FREE"' + line[idx:]
        elif mode == 'prepend':
            if 'group-title="' in line:
                line = re.sub(
                    r'group-title="(.*?)"',
                    lambda m: f'group-title="Z5 TARUN {m.group(1)}"',
                    line
                )
            else:
                idx = line.find(',')
                if idx != -1:
                    line = line[:idx] + ' group-title="Z5 TARUN"' + line[idx:]
    return line

new_lines = []
for source in sources:
    url = source.get('url')
    mode = source.get('mode')
    if not url or not mode:
        print(f"Fuente mal formada: {source}")
        continue
    try:
        response = requests.get(url)
        if response.status_code == 200:
            m3u_content = response.text
            for line in m3u_content.splitlines():
                new_lines.append(process_line(line, mode))
        else:
            print(f"Error al obtener {url}: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error con la fuente {url}: {e}")

new_content = "\n".join(new_lines)

try:
    with open('lista_varios.m3u', 'w', encoding='utf-8') as file:
        file.write(new_content)
    print("La lista_varios.m3u ha sido creada con éxito.")
except Exception as e:
    print(f"Ocurrió un error al guardar el archivo final: {e}")



