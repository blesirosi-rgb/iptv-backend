def parse_m3u(content: str):
    channels = []
    lines = content.splitlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith("#EXTINF:"):
            name = line.split(",", 1)[1].strip()
            url = lines[i+1].strip() if i+1 < len(lines) else ""
            channels.append({"name": name, "url": url})
    return channels
