import json

def json_to_m3u(json_file, m3u_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        channels = json.load(f)

    with open(m3u_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for ch in channels:
            name = ch.get("channel_name", "")
            logo = ch.get("channel_logo", "")
            group = ", ".join(ch.get("channel_genre", []))
            url = ch.get("streamData", {}).get("fairplayUrl", "")
            extinf = (
                f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
            )
            f.write(extinf)
            f.write(f'{url}\n')

if __name__ == "__main__":
    json_to_m3u('channels.json', 'playlist.m3u')