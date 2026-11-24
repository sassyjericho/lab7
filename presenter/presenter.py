from model.animal_repository import AnimalRepository
from model.animal_custom import AnimalCustom
from model.statistici_animale import StatisticiAnimale


class Presenter:
    def __init__(self, repository=None):
        self.repository = repository or AnimalRepository()
        self.statistici = StatisticiAnimale()
        self.sortare = "id"

    def get_categorie(self, animal):
        return self.statistici.get_categorie(animal)

    def formateaza_lista_animale(self):
        antet = f"{'Rasa':<10} {'Nume':<14} {'Varsta':<8} {'Greutate':<10} Detalii\n"
        separator = "-" * 78 + "\n"
        textbox_content = antet + separator

        for animal in self.obtine_animale():
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
        self.sortare = "nume"
        return self.formateaza_lista_animale()

    def sorteaza_dupa_varsta(self):
        self.sortare = "varsta"
        return self.formateaza_lista_animale()

    def sorteaza_dupa_greutate(self):
        self.sortare = "greutate"
        return self.formateaza_lista_animale()

    def obtine_lista_initiala(self):
        return self.formateaza_lista_animale()

    def obtine_animale(self):
        return self.repository.toate(self.sortare)

    def adauga_animal(self, nume, varsta, greutate, categorie, detalii=None):
        animal = AnimalCustom(
            nume=str(nume),
            varsta=str(varsta),
            greutate=str(greutate),
            categorie=str(categorie),
            detalii=detalii or {}
        )
        return self.repository.adauga(animal)

    def editeaza_animal(self, animal, nume, varsta, greutate, categorie, detalii=None):
        actualizat = type(animal).__new__(type(animal))
        actualizat.parameters = dict(detalii or {})
        actualizat.parameters.update(nume=str(nume), varsta=str(varsta),
                                     greutate=str(greutate), categorie=str(categorie))
        self.repository.actualizeaza(animal.database_id, actualizat)
        animal.parameters = actualizat.parameters
        return animal

    def sterge_animal(self, animal):
        self.repository.sterge([animal.database_id])

    def sterge_animale(self, animale):
        self.repository.sterge(animal.database_id for animal in animale)

    def obtine_distributie_categorii(self):
        return self.repository.distributie()

    def obtine_medie_greutate_categorii(self):
        return self.repository.medie("greutate")

    def obtine_medie_varsta_categorii(self):
        return self.repository.medie("varsta")
