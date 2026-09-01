# interface/__main__.py
import random
from animale.erbivore import Vaca, Cal, Iepure, Oaie, Capra, Caprioara, Elefant, Girafa, Panda, Koala
from animale.carnivore import Leu, Lup, Tigru, Pantera, Gepard, Hiena, Rechin, Crocodil, Vultur, UrsPolar
from animale.omnivore import Urs, Porc, Maimuta, Arici, Rata, Cainele, Pisica, Gasca, Veverita, Soarece

def genereaza_animal_random():
    clase_disponibile = [
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
        lambda: Soarece("Jerry", 1, 0.05, True, "15km/h", True)
    ]
    
    constructor_aleator = random.choice(clase_disponibile)
    return constructor_aleator()

if __name__ == "__main__":
    numar_animale_generate = 10
    animale = [genereaza_animal_random() for _ in range(numar_animale_generate)]

    print(f"--- GENERARE ALEATORIE A {numar_animale_generate} ANIMALE ---\n")
    for animal in animale:
        print(f"--- Obiect: {type(animal).__name__} ---")
        for cheie in animal.parameters.keys():
            print(f"  {cheie}: {animal.get_parameter(cheie)}")
        print()