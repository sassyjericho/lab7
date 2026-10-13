from model.generator import GeneratorAnimale
from model.animal_custom import AnimalCustom


class Presenter:
    def __init__(self):
        self.generator = GeneratorAnimale()
        self.animale = self.generator.genereaza_toate_animalele()

    def get_categorie(self, animal):
        if type(animal).__name__ == "AnimalCustom":
            return str(animal.get_parameter("categorie"))
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

    def formateaza_lista_animale(self):
        antet = f"{'Rasa':<10} {'Nume':<14} {'Varsta':<8} {'Greutate':<10} Detalii\n"
        separator = "-" * 78 + "\n"
        textbox_content = antet + separator

        for animal in self.animale:
            categorie = self.get_categorie(animal)
            nume = animal.get_parameter("nume")
            varsta = animal.get_parameter("varsta")
            greutate = animal.get_parameter("greutate")
            detalii = ", ".join(
                f"{cheie}={valoare}"
                for cheie, valoare in animal.parameters.items()
                if cheie not in {"nume", "varsta", "greutate", "categorie"}
            )
            textbox_content += f"{categorie:<10} {str(nume):<14} {str(varsta):<8} {str(greutate):<10} {detalii}\n"

        return textbox_content

    def sorteaza_dupa_nume(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "nume"))
        return self.formateaza_lista_animale()

    def sorteaza_dupa_varsta(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "varsta"))
        return self.formateaza_lista_animale()

    def sorteaza_dupa_greutate(self):
        self.animale.sort(key=lambda animal: self.extrage_valoare_sortare(animal, "greutate"))
        return self.formateaza_lista_animale()

    def obtine_lista_initiala(self):
        return self.formateaza_lista_animale()

    def obtine_animale(self):
        return self.animale

    def adauga_animal(self, nume, varsta, greutate, categorie, detalii=None):
        animal = AnimalCustom(
            nume=str(nume),
            varsta=str(varsta),
            greutate=str(greutate),
            categorie=str(categorie),
            detalii=detalii or {}
        )
        self.animale.append(animal)
        return animal

    def editeaza_animal(self, animal, nume, varsta, greutate, categorie, detalii=None):
        animal.set_parameter("nume", str(nume))
        animal.set_parameter("varsta", str(varsta))
        animal.set_parameter("greutate", str(greutate))
        animal.set_parameter("categorie", str(categorie))

        for cheie in list(animal.parameters.keys()):
            if cheie not in {"nume", "varsta", "greutate", "categorie"}:
                del animal.parameters[cheie]

        for cheie, valoare in (detalii or {}).items():
            animal.set_parameter(str(cheie), valoare)

        return animal

    def sterge_animal(self, animal):
        self.animale = [element for element in self.animale if element is not animal]

    def sterge_animale(self, animale):
        selected = set(id(element) for element in animale)
        self.animale = [element for element in self.animale if id(element) not in selected]
