from __future__ import annotations

import io
import json
from time import sleep
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen, Request

from PIL import Image, ImageOps


ANIMALS = {
    "Vaca": "cow",
    "Cal": "horse",
    "Iepure": "rabbit",
    "Oaie": "sheep",
    "Capra": "goat",
    "Caprioara": "roe deer",
    "Elefant": "elephant",
    "Girafa": "giraffe",
    "Panda": "giant panda",
    "Koala": "koala",
    "Leu": "lion",
    "Lup": "wolf",
    "Tigru": "tiger",
    "Pantera": "panther",
    "Gepard": "cheetah",
    "Hiena": "hyena",
    "Rechin": "shark",
    "Crocodil": "crocodile",
    "Vultur": "vulture",
    "UrsPolar": "polar bear",
    "Urs": "bear",
    "Porc": "pig",
    "Maimuta": "monkey",
    "Arici": "hedgehog",
    "Rata": "duck",
    "Cainele": "dog",
    "Pisica": "cat",
    "Gasca": "goose",
    "Veverita": "squirrel",
    "Soarece": "mouse",
}


BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
IMAGES_DIR = BASE_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)


def get_thumbnail_url(title: str) -> str | None:
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(title)}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urlopen(req, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    thumb = data.get("thumbnail") or {}
    return thumb.get("source")


def download_image(url: str) -> Image.Image:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=60) as response:
        raw = response.read()
    return Image.open(io.BytesIO(raw)).convert("RGB")


def prepare_image(img: Image.Image) -> Image.Image:
    img = ImageOps.exif_transpose(img)
    img.thumbnail((900, 900), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (900, 900), "#1f2333")
    x = (canvas.width - img.width) // 2
    y = (canvas.height - img.height) // 2
    canvas.paste(img, (x, y))
    return canvas


def main() -> None:
    successes = 0
    failures = []

    for class_name, tag in ANIMALS.items():
        try:
            sleep(2.5)
            url = get_thumbnail_url(tag)
            if not url:
                raise RuntimeError(f"No thumbnail for {tag}")
            img = download_image(url)
            img = prepare_image(img)
            output_path = IMAGES_DIR / f"{class_name}.png"
            img.save(output_path, format="PNG", optimize=True)
            successes += 1
            print(f"Saved {output_path.name}")
        except Exception as exc:
            failures.append(class_name)
            print(f"Failed {class_name}: {exc}")

    print()
    print(f"Done. Saved {successes} images.")
    if failures:
        print("Missing or failed:", ", ".join(failures))


if __name__ == "__main__":
    main()
