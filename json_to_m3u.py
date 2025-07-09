import json

def json_to_m3u(json_file, m3u_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    channels_by_group = data.get("channels", {})

    with open(m3u_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for group, channels in channels_by_group.items():
            for ch in channels:
                name = ch.get("name", "")
                logo = ch.get("logo", "")
                group_title = ch.get("group", group)
                url = ch.get("url", "")
                extinf = (
                    f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group_title}",{name}\n'
                )
                f.write(extinf)
                f.write(f'{url}\n')

if __name__ == "__main__":
    json_to_m3u('channels.json', 'playlist.m3u')
