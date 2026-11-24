from math import isfinite


class StatisticiAnimale:
    def __init__(self):
        self.erbivore = {
            "Vaca", "Cal", "Iepure", "Oaie", "Capra", "Caprioara", "Elefant", "Girafa", "Panda", "Koala"
        }
        self.carnivore = {
            "Leu", "Lup", "Tigru", "Pantera", "Gepard", "Hiena", "Rechin", "Crocodil", "Vultur", "UrsPolar"
        }

    def get_categorie(self, animal):
        categorie_custom = animal.parameters.get("categorie")
        if categorie_custom:
            return str(categorie_custom)

        tip = type(animal).__name__
        if tip in self.erbivore:
            return "Erbivor"
        if tip in self.carnivore:
            return "Carnivor"
        return "Omnivor"

    @staticmethod
    def _to_number(value):
        try:
            number = float(str(value).strip().replace(",", "."))
            return number if isfinite(number) and number >= 0 else None
        except (TypeError, ValueError):
            return None

    def distributie_categorii(self, animale):
        rezultat = {"Erbivor": 0, "Carnivor": 0, "Omnivor": 0}
        for animal in animale:
            categorie = self.get_categorie(animal)
            rezultat[categorie] = rezultat.get(categorie, 0) + 1
        return rezultat

    def medie_pe_categorie(self, animale, parametru):
        valori = {}
        for animal in animale:
            categorie = self.get_categorie(animal)
            numar = self._to_number(animal.parameters.get(parametru))
            if numar is not None:
                valori.setdefault(categorie, []).append(numar)
        return {
            categorie: round(sum(numere) / len(numere), 2)
            for categorie, numere in valori.items()
        }

    def medie_greutate_pe_categorie(self, animale):
        return self.medie_pe_categorie(animale, "greutate")

    def medie_varsta_pe_categorie(self, animale):
        return self.medie_pe_categorie(animale, "varsta")
