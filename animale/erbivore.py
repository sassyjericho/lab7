# animale/erbivore.py
from base_class.base_class import BaseClass

class Vaca(BaseClass):
    def __init__(self, nume, varsta, greutate, lapte, rasa, gestanta):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("cantitate_lapte", lapte)
        self.set_parameter("rasa", rasa)
        self.set_parameter("este_gestanta", gestanta)

class Cal(BaseClass):
    def __init__(self, nume, varsta, greutate, viteza, blana, dresat):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("viteza_maxima", viteza)
        self.set_parameter("tip_blana", blana)
        self.set_parameter("dresat", dresat)

class Iepure(BaseClass):
    def __init__(self, nume, varsta, greutate, urechi, ochi, morcovi):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("lungime_urechi", urechi)
        self.set_parameter("culoare_ochi", ochi)
        self.set_parameter("prefera_morcovi", morcovi)

class Oaie(BaseClass):
    def __init__(self, nume, varsta, greutate, cantitate_lana, lana_culoare, cornuta):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("cantitate_lana", cantitate_lana)
        self.set_parameter("lana_culoare", lana_culoare)
        self.set_parameter("cornuta", cornuta)

class Capra(BaseClass):
    def __init__(self, nume, varsta, greutate, altitudine_max, barba, lapte_capra):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("altitudine_max", altitudine_max)
        self.set_parameter("barba", barba)
        self.set_parameter("lapte_capra", lapte_capra)

class Caprioara(BaseClass):
    def __init__(self, nume, varsta, greutate, lungime_coarne, viteza_salt, pete_blana):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("lungime_coarne", lungime_coarne)
        self.set_parameter("viteza_salt", viteza_salt)
        self.set_parameter("pete_blana", pete_blana)

class Elefant(BaseClass):
    def __init__(self, nume, varsta, greutate, lungime_trompa, greutate_fildes, memorie_buna):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("lungime_trompa", lungime_trompa)
        self.set_parameter("greutate_fildes", greutate_fildes)
        self.set_parameter("memorie_buna", memorie_buna)

class Girafa(BaseClass):
    def __init__(self, nume, varsta, greutate, inaltime_gat, culoare_pete, ore_somn):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("inaltime_gat", inaltime_gat)
        self.set_parameter("culoare_pete", culoare_pete)
        self.set_parameter("ore_somn", ore_somn)

class Panda(BaseClass):
    def __init__(self, nume, varsta, greutate, kg_bambus_zi, leneș, culoare_cerc_ochi):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("kg_bambus_zi", kg_bambus_zi)
        self.set_parameter("lenes", leneș)
        self.set_parameter("culoare_cerc_ochi", culoare_cerc_ochi)

class Koala(BaseClass):
    def __init__(self, nume, varsta, greutate, ore_somn_zi, tip_eucalipt, catarator):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("ore_somn_zi", ore_somn_zi)
        self.set_parameter("tip_eucalipt", tip_eucalipt)
        self.set_parameter("catarator", catarator)