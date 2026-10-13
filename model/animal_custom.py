from model.base_class.base_class import BaseClass


class AnimalCustom(BaseClass):
    def __init__(self, nume, varsta, greutate, categorie, detalii=None):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("categorie", categorie)

        for cheie, valoare in (detalii or {}).items():
            self.set_parameter(cheie, valoare)
