import os
import sqlite3
import sys
from tkinter import messagebox

from PIL import Image as PILImage, ImageOps
import customtkinter as ctk

from model.image_factory import ImageFactory
from presenter.presenter import Presenter
from view.chart_frame import GraficAnimaleFrame


class AppHeader(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=12, fg_color="#27243a", height=62)
        self.grid_columnconfigure(0, weight=1)

        self.icon = ctk.CTkLabel(self, text="C", width=28, height=28, corner_radius=8,
                                font=ctk.CTkFont(size=22, weight="bold"),
                                fg_color="#7c3aed", text_color="white")
        self.icon.grid(row=0, column=0, sticky="w", padx=(16, 0), pady=14)


class CardAnimal(ctk.CTkFrame):
    def __init__(self, master, animal, callback_stergere, callback_selectie, callback_editare):
        super().__init__(master, corner_radius=14, fg_color="#2d2f3a", border_width=1, border_color="#3b3d4d")
        self.animal = animal
        self.callback_stergere = callback_stergere
        self.callback_selectie = callback_selectie
        self.callback_editare = callback_editare

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)

        self.select_var = ctk.BooleanVar(value=False)
        self.check_select = ctk.CTkCheckBox(self, text="", variable=self.select_var, command=self.on_selectie,
                                            fg_color="#8b5cf6", checkbox_height=18, checkbox_width=18)
        self.check_select.grid(row=0, column=0, padx=(16, 8), pady=(18, 6), sticky="w")

        self.imagine = self.load_image_for_animal(animal)
        self.image_box = ctk.CTkFrame(self, width=200, height=200, corner_radius=18, fg_color="#1f2333")
        self.image_box.grid(row=0, column=1, padx=(8, 18), pady=(8, 8), sticky="w")
        self.image_box.grid_propagate(False)

        self.image_label = ctk.CTkLabel(self.image_box, text="") if self.imagine is None else ctk.CTkLabel(self.image_box, image=self.imagine, text="")
        if self.imagine is not None:
            self.image_label.image = self.imagine
        self.image_label.place(relx=0.5, rely=0.5, anchor="center")

        info_container = ctk.CTkFrame(self, fg_color="transparent")
        info_container.grid(row=0, column=2, padx=(0, 12), pady=12, sticky="w")
        info_container.grid_columnconfigure(0, weight=1)

        nume = str(animal.get_parameter("nume"))
        self.nume_label = ctk.CTkLabel(info_container, text=nume, font=ctk.CTkFont(size=26, weight="bold"), text_color="#f8fafc")
        self.nume_label.grid(row=0, column=0, sticky="w")

        self.descriere_label = ctk.CTkLabel(info_container, text=self.get_descriere(animal), anchor="w", text_color="#cbd5e1")
        self.descriere_label.grid(row=1, column=0, pady=(10, 4), sticky="w")

        varsta = str(animal.get_parameter("varsta"))
        greutate = str(animal.get_parameter("greutate"))
        self.date_principale_label = ctk.CTkLabel(
            info_container,
            text=f"Vârstă: {varsta} | Greutate: {greutate}",
            anchor="w",
            text_color="#e2e8f0"
        )
        self.date_principale_label.grid(row=2, column=0, pady=(2, 4), sticky="w")

        self.more_label = ctk.CTkLabel(info_container, text=self.get_more_info(animal), anchor="w", text_color="#a5b4fc")
        self.more_label.grid(row=3, column=0, sticky="w")

        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=0, column=3, padx=(4, 18), pady=(10, 8), sticky="e")

        self.buton_edit = ctk.CTkButton(actions, text="✎", width=42, height=42, fg_color="#4a5fd1", hover_color="#5b6fe7",
                                        command=lambda: self.callback_editare(self.animal), corner_radius=10)
        self.buton_edit.grid(row=0, column=0, pady=(0, 8), sticky="ew")

        self.buton_stergere = ctk.CTkButton(actions, text="✕", width=42, height=42, fg_color="#7a1d2d", hover_color="#9c2a3b",
                                            command=lambda: self.callback_stergere(self.animal), corner_radius=10)
        self.buton_stergere.grid(row=1, column=0, sticky="ew")

    def load_image_for_animal(self, animal):
        tip = type(animal).__name__
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
        if getattr(sys, "frozen", False):
            candidates = [
                os.path.join(getattr(sys, "_MEIPASS", ""), "images"),
                os.path.join(os.path.dirname(sys.executable), "images"),
                os.path.join(os.path.dirname(sys.executable), "_internal", "images"),
                base_dir,
            ]
            for candidate in candidates:
                if candidate and os.path.isdir(candidate):
                    base_dir = candidate
                    break
        image_path = os.path.join(base_dir, f"{tip}.png")
        if os.path.exists(image_path):
            try:
                pil_image = PILImage.open(image_path).convert("RGBA")
                square = self.zoom_crop_to_square(pil_image, 0.72, 360)
                return ctk.CTkImage(light_image=square, dark_image=square, size=(200, 200))
            except Exception:
                pass

        fallback = PILImage.new("RGBA", (360, 360), (90, 110, 180, 255))
        return ctk.CTkImage(light_image=fallback, dark_image=fallback, size=(200, 200))

    @staticmethod
    def zoom_crop_to_square(pil_image, zoom_factor=0.72, output_size=360):
        width, height = pil_image.size
        zoom_factor = max(0.35, min(zoom_factor, 1.0))

        crop_w = max(1, int(width * zoom_factor))
        crop_h = max(1, int(height * zoom_factor))
        left = max(0, (width - crop_w) // 2)
        top = max(0, (height - crop_h) // 2)
        right = min(width, left + crop_w)
        bottom = min(height, top + crop_h)

        cropped = pil_image.crop((left, top, right, bottom))
        return ImageOps.fit(
            cropped,
            (output_size, output_size),
            method=PILImage.Resampling.LANCZOS,
            centering=(0.5, 0.5),
        )

    @staticmethod
    def get_descriere(animal):
        categorie = animal.parameters.get("categorie") or type(animal).__name__
        if "AnimalCustom" in str(type(animal).__name__):
            return "Some description"
        return f"Categorie: {categorie}"

    @staticmethod
    def get_more_info(animal):
        params = []
        for cheie, valoare in animal.parameters.items():
            if cheie not in {"nume", "categorie", "varsta", "greutate"}:
                params.append(f"{cheie}={valoare}")
        if not params:
            return "More info"
        return ", ".join(params[:2])

    @staticmethod
    def get_categorie_for_display(animal):
        if animal.parameters.get("categorie"):
            return str(animal.parameters.get("categorie"))
        if type(animal).__name__ in {
            "Vaca", "Cal", "Iepure", "Oaie", "Capra", "Caprioara", "Elefant", "Girafa", "Panda", "Koala"
        }:
            return "Erbivor"
        if type(animal).__name__ in {
            "Leu", "Lup", "Tigru", "Pantera", "Gepard", "Hiena", "Rechin", "Crocodil", "Vultur", "UrsPolar"
        }:
            return "Carnivor"
        return "Omnivor"

    def on_selectie(self):
        self.callback_selectie(self.animal, self.select_var.get())


class DialogAdaugareAnimal(ctk.CTkToplevel):
    def __init__(self, master, callback_adaugare):
        super().__init__(master)
        self.title("Adaugă animal")
        self.geometry("420x360")
        self.minsize(350, 280)
        self.callback_adaugare = callback_adaugare
        self.grab_set()

        self.columnconfigure(0, weight=1)

        self.nume_var = ctk.StringVar(value="")
        self.varsta_var = ctk.StringVar(value="")
        self.greutate_var = ctk.StringVar(value="")
        self.categorie_var = ctk.StringVar(value="Erbivor")
        self.detalii_var = ctk.StringVar(value="")

        ctk.CTkLabel(self, text="Nume:").grid(row=0, column=0, padx=18, pady=(18, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.nume_var).grid(row=1, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Vârstă:").grid(row=2, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.varsta_var).grid(row=3, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Greutate:").grid(row=4, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.greutate_var).grid(row=5, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Categorie:").grid(row=6, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkOptionMenu(self, values=["Erbivor", "Carnivor", "Omnivor"], variable=self.categorie_var).grid(row=7, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Detalii (opțional, cheie=valoare):").grid(row=8, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.detalii_var).grid(row=9, column=0, padx=18, sticky="ew")

        butoane = ctk.CTkFrame(self, fg_color="transparent")
        butoane.grid(row=10, column=0, pady=(18, 18), padx=18, sticky="ew")
        butoane.columnconfigure(0, weight=1)
        butoane.columnconfigure(1, weight=1)

        ctk.CTkButton(butoane, text="Adaugă", command=self.adauga).grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkButton(butoane, text="Anulează", command=self.destroy).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def adauga(self):
        nume = self.nume_var.get().strip()
        varsta = self.varsta_var.get().strip()
        greutate = self.greutate_var.get().strip()
        categorie = self.categorie_var.get()
        detalii_text = self.detalii_var.get().strip()

        if not nume or not varsta or not greutate:
            return

        detalii = {}
        if detalii_text:
            for item in detalii_text.split(","):
                if "=" in item:
                    key, value = item.split("=", 1)
                    detalii[key.strip()] = value.strip()

        self.callback_adaugare(nume, varsta, greutate, categorie, detalii)
        self.destroy()


class DialogEditareAnimal(ctk.CTkToplevel):
    def __init__(self, master, animal, callback_editare):
        super().__init__(master)
        self.title("Editează animal")
        self.geometry("420x360")
        self.minsize(350, 280)
        self.callback_editare = callback_editare
        self.animal = animal
        self.grab_set()

        self.columnconfigure(0, weight=1)

        self.nume_var = ctk.StringVar(value=str(animal.get_parameter("nume")))
        self.varsta_var = ctk.StringVar(value=str(animal.get_parameter("varsta")))
        self.greutate_var = ctk.StringVar(value=str(animal.get_parameter("greutate")))
        self.categorie_var = ctk.StringVar(value=str(animal.parameters.get("categorie") or self.get_categorie_for_display(animal)))
        self.detalii_var = ctk.StringVar(value=", ".join(f"{k}={v}" for k, v in animal.parameters.items() if k not in {"nume", "varsta", "greutate", "categorie"}))

        ctk.CTkLabel(self, text="Nume:").grid(row=0, column=0, padx=18, pady=(18, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.nume_var).grid(row=1, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Vârstă:").grid(row=2, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.varsta_var).grid(row=3, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Greutate:").grid(row=4, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.greutate_var).grid(row=5, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Categorie:").grid(row=6, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkOptionMenu(self, values=["Erbivor", "Carnivor", "Omnivor"], variable=self.categorie_var).grid(row=7, column=0, padx=18, sticky="ew")

        ctk.CTkLabel(self, text="Detalii (cheie=valoare):").grid(row=8, column=0, padx=18, pady=(12, 4), sticky="w")
        ctk.CTkEntry(self, textvariable=self.detalii_var).grid(row=9, column=0, padx=18, sticky="ew")

        butoane = ctk.CTkFrame(self, fg_color="transparent")
        butoane.grid(row=10, column=0, pady=(18, 18), padx=18, sticky="ew")
        butoane.columnconfigure(0, weight=1)
        butoane.columnconfigure(1, weight=1)

        ctk.CTkButton(butoane, text="Salvează", command=self.salveaza).grid(row=0, column=0, padx=(0, 8), sticky="ew")
        ctk.CTkButton(butoane, text="Anulează", command=self.destroy).grid(row=0, column=1, padx=(8, 0), sticky="ew")

    @staticmethod
    def get_categorie_for_display(animal):
        if animal.parameters.get("categorie"):
            return str(animal.parameters.get("categorie"))
        if type(animal).__name__ in {
            "Vaca", "Cal", "Iepure", "Oaie", "Capra", "Caprioara", "Elefant", "Girafa", "Panda", "Koala"
        }:
            return "Erbivor"
        if type(animal).__name__ in {
            "Leu", "Lup", "Tigru", "Pantera", "Gepard", "Hiena", "Rechin", "Crocodil", "Vultur", "UrsPolar"
        }:
            return "Carnivor"
        return "Omnivor"

    def salveaza(self):
        detalii = {}
        text = self.detalii_var.get().strip()
        if text:
            for item in text.split(","):
                item = item.strip()
                if item and "=" in item:
                    key, value = item.split("=", 1)
                    detalii[key.strip()] = value.strip()

        self.callback_editare(
            self.animal,
            self.nume_var.get().strip(),
            self.varsta_var.get().strip(),
            self.greutate_var.get().strip(),
            self.categorie_var.get(),
            detalii
        )
        self.destroy()


class AplicatieAnimale(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lista animale")
        self.geometry("980x650")
        self.minsize(900, 600)
        self.configure(fg_color="#171923")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.presenter = Presenter()
        self.animale_selectate = set()
        self.grafice_window = None
        self.grafic_frame = None

        self.header = AppHeader(self)
        self.header.pack(padx=20, pady=(18, 12), fill="x")

        self.sort_controls = ctk.CTkFrame(self, corner_radius=12, fg_color="#27243a")
        self.sort_controls.pack(padx=20, pady=(0, 10), fill="x")

        self.btn_nume = ctk.CTkButton(self.sort_controls, text="Sort by name", command=self.on_sort_by_name, fg_color="#3a5aa8", hover_color="#4d6ec4")
        self.btn_varsta = ctk.CTkButton(self.sort_controls, text="Sort by age", command=self.on_sort_by_age, fg_color="#3a5aa8", hover_color="#4d6ec4")
        self.btn_greutate = ctk.CTkButton(self.sort_controls, text="Sort by weight", command=self.on_sort_by_weight, fg_color="#3a5aa8", hover_color="#4d6ec4")
        self.btn_grafice = ctk.CTkButton(
            self.sort_controls,
            text="Afișează grafice",
            command=self.on_afiseaza_grafice,
            fg_color="#0f766e",
            hover_color="#0d9488"
        )

        self.btn_nume.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        self.btn_varsta.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        self.btn_greutate.pack(side="left", padx=10, pady=8, expand=True, fill="x")
        self.btn_grafice.pack(side="left", padx=10, pady=8, expand=True, fill="x")

        self.container = ctk.CTkScrollableFrame(self, width=900, height=440, corner_radius=14, fg_color="#1f2333")
        self.container.pack(padx=20, pady=10, fill="both", expand=True)

        self.controale = ctk.CTkFrame(self, corner_radius=12, fg_color="#27243a")
        self.controale.pack(padx=20, pady=(0, 20), fill="x")

        self.btn_adauga = ctk.CTkButton(self.controale, text="Add item", command=self.on_adauga_element, fg_color="#7c3aed", hover_color="#8b5cf6")
        self.btn_adauga.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        self.btn_sterge_selectate = ctk.CTkButton(self.controale, text="Delete selected", command=self.sterge_selectate, fg_color="#c2410c", hover_color="#e76f51")
        self.btn_sterge_selectate.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        self.afiseaza_animale()

    def report_callback_exception(self, exception, value, traceback):
        if isinstance(value, (ValueError, sqlite3.Error)):
            messagebox.showerror("Eroare", str(value), parent=self)
        else:
            super().report_callback_exception(exception, value, traceback)

    def afiseaza_animale(self):
        self.animale_selectate.clear()
        for widget in self.container.winfo_children():
            widget.destroy()

        for animal in self.presenter.obtine_animale():
            card = CardAnimal(self.container, animal, self.sterge_animal, self.on_selectie_animal, self.on_editare_animal)
            card.pack(fill="x", padx=18, pady=10)

        self.actualizeaza_grafice()

    def actualizeaza_grafice(self):
        if self.grafic_frame is None:
            return

        distributie = self.presenter.obtine_distributie_categorii()
        medii_greutate = self.presenter.obtine_medie_greutate_categorii()
        medii_varsta = self.presenter.obtine_medie_varsta_categorii()
        self.grafic_frame.actualizeaza_grafice(distributie, medii_greutate, medii_varsta)

    def on_afiseaza_grafice(self):
        if self.grafice_window is not None and self.grafice_window.winfo_exists():
            self.grafice_window.focus()
            self.actualizeaza_grafice()
            return

        self.grafice_window = ctk.CTkToplevel(self)
        self.grafice_window.title("Grafice animale")
        self.grafice_window.geometry("1100x480")
        self.grafice_window.minsize(1000, 440)

        self.grafic_frame = GraficAnimaleFrame(self.grafice_window)
        self.grafic_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.actualizeaza_grafice()

        self.grafice_window.protocol("WM_DELETE_WINDOW", self.on_inchide_fereastra_grafice)

    def on_inchide_fereastra_grafice(self):
        if self.grafice_window is not None and self.grafice_window.winfo_exists():
            self.grafice_window.destroy()
        self.grafice_window = None
        self.grafic_frame = None

    def on_adauga_element(self):
        DialogAdaugareAnimal(self, self.adauga_animal)

    def adauga_animal(self, nume, varsta, greutate, categorie, detalii=None):
        self.presenter.adauga_animal(nume, varsta, greutate, categorie, detalii)
        self.afiseaza_animale()

    def sterge_animal(self, animal):
        self.presenter.sterge_animal(animal)
        self.animale_selectate.discard(animal)
        self.afiseaza_animale()

    def on_selectie_animal(self, animal, este_selectat):
        if este_selectat:
            self.animale_selectate.add(animal)
        else:
            self.animale_selectate.discard(animal)

    def sterge_selectate(self):
        if self.animale_selectate:
            self.presenter.sterge_animale(list(self.animale_selectate))
            self.animale_selectate.clear()
            self.afiseaza_animale()

    def on_editare_animal(self, animal):
        DialogEditareAnimal(self, animal, self.editare_animal)

    def editare_animal(self, animal, nume, varsta, greutate, categorie, detalii=None):
        self.presenter.editeaza_animal(animal, nume, varsta, greutate, categorie, detalii)
        self.afiseaza_animale()

    def on_sort_by_name(self):
        self.presenter.sorteaza_dupa_nume()
        self.afiseaza_animale()

    def on_sort_by_age(self):
        self.presenter.sorteaza_dupa_varsta()
        self.afiseaza_animale()

    def on_sort_by_weight(self):
        self.presenter.sorteaza_dupa_greutate()
        self.afiseaza_animale()
