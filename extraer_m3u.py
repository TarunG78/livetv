import requests
import re

# Define las fuentes y sus tipos de procesado
sources = [
    {
        'url': 'https://raw.githubusercontent.com/iptv-org/iptv/refs/heads/master/streams/in.m3u',
        'mode': 'override',  # Sobrescribe el nombre del grupo (ALL INDIA FREE)
    },
    {
        'url': 'https://raw.githubusercontent.com/Raulpa78/m3u/refs/heads/main/z5.m3u',
        'mode': 'prepend',   # Mantiene pero antepone (Z5 TARUN)
    },
    {
        'url': 'https://raw.githubusercontent.com/Raulpa78/tkg/refs/heads/main/I_L_BK.m3u',
        'mode': 'none',  # No modificar ni nombres de grupos ni contenido
    },
    # Puedes añadir más fuentes con sus "mode" correspondiente
]

def process_line(line, mode):
    # Si el modo es "none", respeta el contenido como está
    if mode == 'none':
        return line
    # Solo procesar líneas EXTINF para otros modos
    if line.startswith("#EXTINF"):
        if mode == 'override':
            # Sobrescribe cualquier group-title
            if 'group-title="' in line:
                line = re.sub(r'group-title=".*?"', 'group-title="ALL INDIA FREE"', line)
            else:
                idx = line.find(',')
                if idx != -1:
                    line = line[:idx] + ' group-title="ALL INDIA FREE"' + line[idx:]
        elif mode == 'prepend':
            # Si existe group-title, anteponer Z5 TARUN
            if 'group-title="' in line:
                # Cambia group-title="X" por group-title="Z5 TARUN X"
                line = re.sub(
                    r'group-title="(.*?)"',
                    lambda m: f'group-title="Z5 TARUN {m.group(1)}"',
                    line
                )
            else:
                # Si no existe, simplemente añade el group-title nuevo
                idx = line.find(',')
                if idx != -1:
                    line = line[:idx] + ' group-title="Z5 TARUN"' + line[idx:]
    return line

new_lines = []
for source in sources:
    try:
        response = requests.get(source['url'])
        if response.status_code == 200:
            m3u_content = response.text
            for line in m3u_content.splitlines():
                new_lines.append(process_line(line, source['mode']))
        else:
            print(f"Error al obtener {source['url']}: {response.status_code}")
    except Exception as e:
        print(f"Ocurrió un error con la fuente {source['url']}: {e}")

# Reconstruir el archivo M3U combinado
new_content = "\n".join(new_lines)

try:
    with open('lista_varios.m3u', 'w', encoding='utf-8') as file:
        file.write(new_content)
    print("La lista_varios.m3u ha sido creada con éxito.")
except Exception as e:
    print(f"Ocurrió un error al guardar el archivo final: {e}")
