import customtkinter as ctk
from presenter.presenter import Presenter


class AplicatieAnimale(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lista animale")
        self.geometry("980x650")
        self.minsize(900, 600)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.presenter = Presenter()

        self.titlu = ctk.CTkLabel(self, text="Lista de animale", font=ctk.CTkFont(size=24, weight="bold"))
        self.titlu.pack(pady=(20, 10))

        self.textbox = ctk.CTkTextbox(self, width=900, height=440, corner_radius=12, font=("Consolas", 13))
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)

        self.controale = ctk.CTkFrame(self)
        self.controale.pack(padx=20, pady=(0, 20), fill="x")

        self.btn_nume = ctk.CTkButton(self.controale, text="Sortează după nume", command=self.on_sort_by_name)
        self.btn_varsta = ctk.CTkButton(self.controale, text="Sortează după vârstă", command=self.on_sort_by_age)
        self.btn_greutate = ctk.CTkButton(self.controale, text="Sortează după greutate", command=self.on_sort_by_weight)

        self.btn_nume.pack(side="left", padx=10, pady=12, expand=True, fill="x")
        self.btn_varsta.pack(side="left", padx=10, pady=12, expand=True, fill="x")
        self.btn_greutate.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        self.afiseaza_lista_initiala()

    def afiseaza_textbox(self, content):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", content)
        self.textbox.configure(state="disabled")

    def afiseaza_lista_initiala(self):
        content = self.presenter.obtine_lista_initiala()
        self.afiseaza_textbox(content)

    def on_sort_by_name(self):
        content = self.presenter.sorteaza_dupa_nume()
        self.afiseaza_textbox(content)

    def on_sort_by_age(self):
        content = self.presenter.sorteaza_dupa_varsta()
        self.afiseaza_textbox(content)

    def on_sort_by_weight(self):
        content = self.presenter.sorteaza_dupa_greutate()
        self.afiseaza_textbox(content)
