from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory

from model.database import Database
from model.animal_repository import AnimalRepository
from presenter.presenter import Presenter


class DatabaseCuUrmarire(Database):
    """Afișează comenzile executate efectiv de SQLite în demonstrație."""

    def __init__(self, path):
        super().__init__(path)
        self.afiseaza = False
        self.comenzi = []

    def inregistreaza(self, sql):
        self.comenzi.append(sql)
        if self.afiseaza:
            print("SQL>", sql)

    @contextmanager
    def transaction(self):
        with super().transaction() as connection:
            connection.set_trace_callback(self.inregistreaza)
            yield connection


class DemonstratieSQL:
    @classmethod
    def ruleaza(cls):
        print("VERIFICARE SQL - baza temporara, fara modificarea datelor aplicatiei")
        with TemporaryDirectory() as folder:
            database = DatabaseCuUrmarire(Path(folder) / "demonstratie.sqlite3")
            presenter = Presenter(AnimalRepository(database))
            assert len(presenter.obtine_animale()) == 30
            database.comenzi.clear()
            database.afiseaza = True

            print("\n1. ADAUGARE prin aceeasi metoda folosita de interfata")
            animal = presenter.adauga_animal("Demonstratie SQL", "2", "3,5", "Erbivor")
            assert len(presenter.obtine_animale()) == 31
            print("REZULTAT: 30 -> 31 animale")

            print("\n2. REDESCHIDERE: un Presenter si conexiuni noi")
            database.afiseaza = False
            presenter = Presenter(AnimalRepository(database))
            database.afiseaza = True
            animal = next(a for a in presenter.obtine_animale() if a.database_id == animal.database_id)
            assert animal.parameters["nume"] == "Demonstratie SQL"
            print("REZULTAT: animalul a ramas salvat, ID =", animal.database_id)

            print("\n3. EDITARE")
            presenter.editeaza_animal(animal, "Animal editat", "5", "8", "Omnivor")
            with database.transaction() as connection:
                row = connection.execute("SELECT nume, varsta, greutate FROM animale WHERE id=?", (animal.database_id,)).fetchone()
            assert tuple(row) == ("Animal editat", 5, 8)
            print("REZULTAT:", tuple(row))

            print("\n4. SORTARE in SQL")
            for key, method in (("nume", presenter.sorteaza_dupa_nume),
                                ("varsta", presenter.sorteaza_dupa_varsta),
                                ("greutate", presenter.sorteaza_dupa_greutate)):
                method()
                values = [a.parameters[key] for a in presenter.obtine_animale()]
                expected = sorted(values, key=str.lower) if key == "nume" else sorted(values)
                assert values == expected
                print("REZULTAT:", key, "- primele 5 valori:", values[:5])

            print("\n5. STATISTICI calculate in SQL")
            distribution = presenter.obtine_distributie_categorii()
            assert distribution == {"Erbivor": 10, "Carnivor": 10, "Omnivor": 11}
            print("REZULTAT distributie:", distribution)
            print("REZULTAT medii greutate:", presenter.obtine_medie_greutate_categorii())
            print("REZULTAT medii varsta:", presenter.obtine_medie_varsta_categorii())

            print("\n6. STERGERE si verificare dupa redeschidere")
            presenter.sterge_animal(animal)
            database.afiseaza = False
            presenter = Presenter(AnimalRepository(database))
            database.afiseaza = True
            remaining = presenter.obtine_animale()
            assert len(remaining) == 30
            assert all(a.database_id != animal.database_id for a in remaining)
            print("REZULTAT: 31 -> 30 animale; animalul sters nu reapare")

            for fragment in ("INSERT INTO animale", "UPDATE animale", "DELETE FROM animale",
                             "ORDER BY LOWER(nume)", "ORDER BY varsta", "ORDER BY greutate",
                             "COUNT(*)", "AVG(greutate)", "AVG(varsta)"):
                assert any(fragment in sql for sql in database.comenzi), fragment
            print("\nVERDICT: toate operatiile au executat SQL real. Toate verificarile au trecut.")


if __name__ == "__main__":
    DemonstratieSQL.ruleaza()
