from model.base_class.base_class import BaseClass


class Leu(BaseClass):
    def __init__(self, nume, varsta, greutate, putere_raget, lungime_coama, marime_hamac):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("putere_raget", putere_raget)
        self.set_parameter("lungime_coama", lungime_coama)
        self.set_parameter("marime_hamac", marime_hamac)

class Lup(BaseClass):
    def __init__(self, nume, varsta, greutate, marime_haita, rezistenta_alergare, sunet):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("marime_haita", marime_haita)
        self.set_parameter("rezistenta_alergare", rezistenta_alergare)
        self.set_parameter("sunet", sunet)

class Tigru(BaseClass):
    def __init__(self, nume, varsta, greutate, numar_dungi, inotator_bun, teritoriu):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("numar_dungi", numar_dungi)
        self.set_parameter("inotator_bun", inotator_bun)
        self.set_parameter("teritoriu", teritoriu)

class Pantera(BaseClass):
    def __init__(self, nume, varsta, greutate, agilitate, vedere_noapte, culoare):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("agilitate", agilitate)
        self.set_parameter("vedere_noapte", vedere_noapte)
        self.set_parameter("culoare", culoare)

class Gepard(BaseClass):
    def __init__(self, nume, varsta, greutate, viteza_sprint, acceleratie_sec, pete_solide):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("viteza_sprint", viteza_sprint)
        self.set_parameter("acceleratie_sec", acceleratie_sec)
        self.set_parameter("pete_solide", pete_solide)

class Hiena(BaseClass):
    def __init__(self, nume, varsta, greutate, putere_muscatura, ras_caracteristic, clan):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("putere_muscatura", putere_muscatura)
        self.set_parameter("ras_caracteristic", ras_caracteristic)
        self.set_parameter("clan", clan)

class Rechin(BaseClass):
    def __init__(self, nume, varsta, greutate, numar_dinti, simt_olfactiv, adancime_max):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("numar_dinti", numar_dinti)
        self.set_parameter("simt_olfactiv", simt_olfactiv)
        self.set_parameter("adancime_max", adancime_max)

class Crocodil(BaseClass):
    def __init__(self, nume, varsta, greutate, lungime_corp, timp_apnee, armura_solzi):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("lungime_corp", lungime_corp)
        self.set_parameter("timp_apnee", timp_apnee)
        self.set_parameter("armura_solzi", armura_solzi)

class Vultur(BaseClass):
    def __init__(self, nume, varsta, greutate, anvergura_aripi, altitudine_zbor, acuitate_vizuala):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("anvergura_aripi", anvergura_aripi)
        self.set_parameter("altitudine_zbor", altitudine_zbor)
        self.set_parameter("acuitate_vizuala", acuitate_vizuala)

class UrsPolar(BaseClass):
    def __init__(self, nume, varsta, greutate, grosime_strat_grasime, culoare_blana_reala, inotator_acvatic):
        super().__init__()
        self.set_parameter("nume", nume)
        self.set_parameter("varsta", varsta)
        self.set_parameter("greutate", greutate)
        self.set_parameter("grosime_strat_grasime", grosime_strat_grasime)
        self.set_parameter("culoare_blana_reala", culoare_blana_reala)
        self.set_parameter("inotator_acvatic", inotator_acvatic)
