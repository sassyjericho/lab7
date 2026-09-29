from model.base_class.base_class import BaseClass


class Urs(BaseClass):
    def __init__(self, nume, varsta, greutate, perioada_hibernare, cantitate_miere, putere_ursoae):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("perioada_hibernare", perioada_hibernare)
        self.set_parameter("cantitate_miere", cantitate_miere)
        self.set_parameter("putere_ursoae", putere_ursoae)

class Porc(BaseClass):
    def __init__(self, nume, varsta, greutate, adancime_racire, lungime_rat, prefera_noroi):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("adancime_racire", adancime_racire)
        self.set_parameter("lungime_rat", lungime_rat)
        self.set_parameter("prefera_noroi", prefera_noroi)

class Maimuta(BaseClass):
    def __init__(self, nume, varsta, greutate, IQ, lungime_coada, tip_fruct):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("IQ", IQ)
        self.set_parameter("lungime_coada", lungime_coada)
        self.set_parameter("tip_fruct", tip_fruct)

class Arici(BaseClass):
    def __init__(self, nume, varsta, greutate, numar_ace, viteza_rostogolire, prefera_lapte):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("numar_ace", numar_ace)
        self.set_parameter("viteza_rostogolire", viteza_rostogolire)
        self.set_parameter("prefera_lapte", prefera_lapte)

class Rata(BaseClass):
    def __init__(self, nume, varsta, greutate, tip_mancare_apa, macait_decibeli, zbura_migrator):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("tip_mancare_apa", tip_mancare_apa)
        self.set_parameter("macait_decibeli", macait_decibeli)
        self.set_parameter("zbura_migrator", zbura_migrator)

class Cainele(BaseClass):
    def __init__(self, nume, varsta, greutate, rasa_caine, loialitate_grad, latrat_puternic):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("rasa_caine", rasa_caine)
        self.set_parameter("loialitate_grad", loialitate_grad)
        self.set_parameter("latrat_puternic", latrat_puternic)

class Pisica(BaseClass):
    def __init__(self, nume, varsta, greutate, numar_vieti, toarcere_hz, independenta):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("numar_vieti", numar_vieti)
        self.set_parameter("toarcere_hz", toarcere_hz)
        self.set_parameter("independenta", independenta)

class Gasca(BaseClass):
    def __init__(self, nume, varsta, greutate, agresivitate_paza, lungime_gat, ou_marime):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("agresivitate_paza", agresivitate_paza)
        self.set_parameter("lungime_gat", lungime_gat)
        self.set_parameter("ou_marime", ou_marime)

class Veverita(BaseClass):
    def __init__(self, nume, varsta, greutate, stoc_ghinde, viteza_copac, lungime_coada_stufoasa):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("stoc_ghinde", stoc_ghinde)
        self.set_parameter("viteza_copac", viteza_copac)
        self.set_parameter("lungime_coada_stufoasa", lungime_coada_stufoasa)

class Soarece(BaseClass):
    def __init__(self, nume, varsta, greutate, prefera_cascaval, viteza_fuga, auz_fin):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("prefera_cascaval", prefera_cascaval)
        self.set_parameter("viteza_fuga", viteza_fuga)
        self.set_parameter("auz_fin", auz_fin)
