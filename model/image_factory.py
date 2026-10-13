try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
except ImportError:  # pragma: no cover
    Image = None
    ImageDraw = None
    ImageFont = None
    ImageTk = None


class ImageFactory:
    def __init__(self):
        self.culori = {
            "Erbivor": "#34d399",
            "Carnivor": "#f87171",
            "Omnivor": "#60a5fa",
            "default": "#a78bfa",
        }
        self.emoji_per_tip = {
            "Vaca": "🐄", "Cal": "🐎", "Iepure": "🐇", "Oaie": "🐑", "Capra": "🐐", "Caprioara": "🦌",
            "Elefant": "🐘", "Girafa": "🦒", "Panda": "🐼", "Koala": "🐨",
            "Leu": "🦁", "Lup": "🐺", "Tigru": "🐯", "Pantera": "🐆", "Gepard": "🐆", "Hiena": "🐾",
            "Rechin": "🦈", "Crocodil": "🐊", "Vultur": "🦅", "UrsPolar": "🐻‍❄️",
            "Urs": "🐻", "Porc": "🐖", "Maimuta": "🐒", "Arici": "🦔", "Rata": "🐭", "Cainele": "🐕", "Pisica": "🐈",
            "Gasca": "🦆", "Veverita": "🐿️", "Soarece": "🐁",
            "AnimalCustom": "🦄"
        }

    def genereaza_imagine(self, nume, categorie, tip_animal=None):
        if Image is None or ImageTk is None:
            return None

        categorie = str(categorie or "default")
        background = self.culori.get(categorie, self.culori["default"])
        img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.rounded_rectangle((8, 8, 112, 112), radius=18, fill=background)
        draw.rounded_rectangle((14, 14, 106, 106), radius=15, outline=(255, 255, 255, 120), width=2)

        simbol = self.emoji_per_tip.get(str(tip_animal or ""), self.emoji_per_tip.get(str(nume), "🐾"))
        if simbol == "🐾":
            simbol = (str(nume) or "A")[0].upper()

        font = None
        for path in [
            "C:/Windows/Fonts/seguiemj.ttf",
            "C:/Windows/Fonts/Segoe UI Emoji.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "arial.ttf"
        ]:
            try:
                font = ImageFont.truetype(path, 52)
                break
            except Exception:
                continue
        if font is None:
            try:
                font = ImageFont.load_default()
            except Exception:
                font = None

        if font is not None:
            try:
                bbox = draw.textbbox((0, 0), simbol, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (img.width - text_width) / 2
                y = (img.height - text_height) / 2 - 8
                draw.text((x, y), simbol, font=font, fill="white")
                return ImageTk.PhotoImage(img)
            except Exception:
                pass

        initiala = (str(nume) or "A")[0].upper()
        fallback_font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), initiala, font=fallback_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2 - 6
        draw.text((x, y), initiala, fill="white", font=fallback_font)
        return ImageTk.PhotoImage(img)
