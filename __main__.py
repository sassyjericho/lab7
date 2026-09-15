import random
import customtkinter as ctk

from animale.erbivore import Vaca, Cal, Iepure, Oaie, Capra, Caprioara, Elefant, Girafa, Panda, Koala
from animale.carnivore import Leu, Lup, Tigru, Pantera, Gepard, Hiena, Rechin, Crocodil, Vultur, UrsPolar
from animale.omnivore import Urs, Porc, Maimuta, Arici, Rata, Cainele, Pisica, Gasca, Veverita, Soarece


class GeneratorAnimale:
    def __init__(self):
        self.clase_disponibile = [
            # 10 Erbivore
            lambda: Vaca("Bălțata", 5, 450, "25l/zi", "Holstein", True),
            lambda: Cal("Tornado", 7, 520, "65km/h", "Murg", True),
            lambda: Iepure("Urechiat", 2, 3.5, "12cm", "Roșii", True),
            lambda: Oaie("Bârsana", 3, 60, "4kg", "Albă", True),
            lambda: Capra("Râioasa", 4, 45, "2500m", True, "2l/zi"),
            lambda: Caprioara("Bambi", 2, 40, "20cm", "50km/h", True),
            lambda: Elefant("Dumbo", 12, 4000, "2m", "50kg", True),
            lambda: Girafa("Melman", 6, 800, "3m", "Maro", 4),
            lambda: Panda("Po", 5, 100, 15, True, "Negru"),
            lambda: Koala("Leneșu", 3, 9, 20, "Eucalipt", True),

            # 10 Carnivore
            lambda: Leu("Simba", 4, 190, "114 dB", "40cm", "Mare"),
            lambda: Lup("Alpha", 3, 50, 8, "Ridicată", "Urlet"),
            lambda: Tigru("Sherkhan", 6, 220, 100, True, "Jungle"),
            lambda: Pantera("Bagheera", 4, 70, "Foarte mare", True, "Negru"),
            lambda: Gepard("Flash", 5, 55, "120km/h", 3.0, True),
            lambda: Hiena("Shenzi", 3, 60, "Ridicată", True, "Clan 1"),
            lambda: Rechin("Jaws", 8, 1100, 300, True, "1000m"),
            lambda: Crocodil("Nile", 15, 500, "4m", 60, True),
            lambda: Vultur("Sky", 4, 6, "2m", "3000m", True),
            lambda: UrsPolar("Nanook", 9, 450, "10cm", "Alb", True),

            # 10 Omnivore
            lambda: Urs("Martin", 8, 350, "5 luni", "10kg", "Puternic"),
            lambda: Porc("Ghiță", 1, 120, "15cm", "10cm", True),
            lambda: Maimuta("Cici", 4, 12, 85, "50cm", "Banană"),
            lambda: Arici("Sonic", 2, 1, 5000, "20km/h", False),
            lambda: Rata("Donak", 2, 2, "Semințe", 70, True),
            lambda: Cainele("Rex", 4, 30, "Ciobanesc", 10, True),
            lambda: Pisica("Tom", 3, 4, 9, 25, True),
            lambda: Gasca("Honk", 2, 5, "Ridicată", "30cm", "Mare"),
            lambda: Veverita("Rontzi", 1, 0.5, 150, "30km/h", "20cm"),
            lambda: Soarece("Jerry", 1, 0.05, True, "15km/h", True),
        ]

    def genereaza_animal_random(self):
        constructor_aleator = random.choice(self.clase_disponibile)
        return constructor_aleator()

    def genereaza_toate_animalele(self):
        return [constructor() for constructor in self.clase_disponibile]


class AplicatieAnimale(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lista animale")
        self.geometry("980x650")
        self.minsize(900, 600)

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.generator = GeneratorAnimale()
        self.animale = self.generator.genereaza_toate_animalele()

        self.titlu = ctk.CTkLabel(self, text="Lista de animale", font=ctk.CTkFont(size=24, weight="bold"))
        self.titlu.pack(pady=(20, 10))

        self.textbox = ctk.CTkTextbox(self, width=900, height=440, corner_radius=12, font=("Consolas", 13))
        self.textbox.pack(padx=20, pady=10, fill="both", expand=True)

        self.controale = ctk.CTkFrame(self)
        self.controale.pack(padx=20, pady=(0, 20), fill="x")

        self.btn_nume = ctk.CTkButton(self.controale, text="Sortează după nume", command=self.sorteaza_dupa_nume)
        self.btn_varsta = ctk.CTkButton(self.controale, text="Sortează după vârstă", command=self.sorteaza_dupa_varsta)
        self.btn_greutate = ctk.CTkButton(self.controale, text="Sortează după greutate", command=self.sorteaza_dupa_greutate)

        self.btn_nume.pack(side="left", padx=10, pady=12, expand=True, fill="x")
        self.btn_varsta.pack(side="left", padx=10, pady=12, expand=True, fill="x")
        self.btn_greutate.pack(side="left", padx=10, pady=12, expand=True, fill="x")

        self.afiseaza_animale()

    def get_categorie(self, animal):
        if type(animal).__name__ in {
            "Vaca", "Cal", "Iepure", "Oaie", "Capra", "Caprioara", "Elefant", "Girafa", "Panda", "Koala"
        }:
            return "Erbivor"
        if type(animal).__name__ in {
            "Leu", "Lup", "Tigru", "Pantera", "Gepard", "Hiena", "Rechin", "Crocodil", "Vultur", "UrsPolar"
        }:
            return "Carnivor"
        return "Omnivor"

    def extrage_valoare_sortare(self, animal, cheie):
        valoare = animal.get_parameter(cheie)
        if cheie == "nume":
            return str(valoare).lower()
        try:
            return float(valoare)
        except (TypeError, ValueError):
            return str(valoare).lower()

    def afiseaza_animale(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        antet = f"{'Rasa':<10} {'Nume':<14} {'Varsta':<8} {'Greutate':<10} Detalii\n"
        separator = "-" * 78 + "\n"
        self.textbox.insert("end", antet)
        self.textbox.insert("end", separator)

        for index, animal in enumerate(self.animale, start=1):
            categorie = self.get_categorie(animal)
            nume = animal.get_parameter("nume")
            varsta = animal.get_parameter("varsta")
            greutate = animal.get_parameter("greutate")
            detalii = ", ".join(f"{cheie}={valoare}" for cheie, valoare in animal.parameters.items() if cheie not in {"nume", "varsta", "greutate"})
            self.textbox.insert(
                "end",
                f"{categorie:<10} {str(nume):<14} {str(varsta):<8} {str(greutate):<10} {detalii}\n"
            )

        self.textbox.configure(state="disabled")

    def sorteaza_dupa_nume(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "nume"))
        self.afiseaza_animale()

    def sorteaza_dupa_varsta(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "varsta"))
        self.afiseaza_animale()

    def sorteaza_dupa_greutate(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "greutate"))
        self.afiseaza_animale()


if __name__ == "__main__":
    aplicatie = AplicatieAnimale()
    aplicatie.mainloop()