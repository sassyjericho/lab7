from pathlib import Path
import io
import json
from urllib.request import Request, urlopen
from PIL import Image

base = Path(r"c:\Users\Asus\Downloads\piig\images")

def save(title, filename):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '%20')}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    data = json.loads(urlopen(req, timeout=30).read().decode("utf-8"))
    src = data.get("thumbnail", {}).get("source")
    if not src:
        raise RuntimeError(f"No thumbnail for {title}")
    raw = urlopen(Request(src, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read()
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    img.thumbnail((900, 900))
    canvas = Image.new("RGB", (900, 900), "#1f2333")
    canvas.paste(img, ((900 - img.width) // 2, (900 - img.height) // 2))
    canvas.save(base / filename)
    print(f"saved {filename}")

save("Goat", "Capra.png")
save("Leopard", "Pantera.png")
