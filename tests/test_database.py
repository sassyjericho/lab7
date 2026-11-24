import tempfile
import unittest
from pathlib import Path

from model.animal_repository import AnimalRepository
from model.database import Database
from presenter.presenter import Presenter


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.database = Database(Path(self.directory.name) / "test.sqlite3")
        self.presenter = Presenter(AnimalRepository(self.database))

    def restart(self):
        return Presenter(AnimalRepository(self.database))

    def test_initializare_si_tipuri(self):
        animals = self.restart().obtine_animale()
        self.assertEqual(len(animals), 30)
        self.assertEqual(type(animals[0]).__name__, "Vaca")
        self.assertEqual(animals[0].parameters["rasa"], "Holstein")
        self.assertEqual(self.presenter.obtine_distributie_categorii(),
                         {"Erbivor": 10, "Carnivor": 10, "Omnivor": 10})

    def test_crud_persistent_si_detalii(self):
        animal = self.presenter.adauga_animal("O'Brien'); DROP TABLE animale;--", "2", "3,5", "Erbivor", {"blana": "albă", "nume": "invalid"})
        restored = self.restart().obtine_animale()[-1]
        self.assertEqual(restored.database_id, animal.database_id)
        self.assertEqual(restored.parameters["greutate"], 3.5)
        self.assertEqual(restored.parameters["nume"], animal.parameters["nume"])
        self.presenter.editeaza_animal(restored, "Nou", "10", "5", "Omnivor", {"activ": True})
        updated = self.restart().obtine_animale()[-1]
        self.assertEqual(updated.parameters["nume"], "Nou")
        self.assertTrue(updated.parameters["activ"])
        self.assertNotIn("blana", updated.parameters)
        self.presenter.sterge_animal(updated)
        self.assertEqual(len(self.restart().obtine_animale()), 30)

    def test_stergere_totala_nu_repopuleaza(self):
        self.presenter.sterge_animale(self.presenter.obtine_animale())
        self.assertEqual(self.restart().obtine_animale(), [])
        self.assertEqual(self.presenter.obtine_medie_varsta_categorii(), {})

    def test_sortare_si_agregari(self):
        self.presenter.sterge_animale(self.presenter.obtine_animale())
        self.presenter.adauga_animal("z", "10", "2", "Erbivor")
        self.presenter.adauga_animal("A", "2", "10", "Erbivor")
        self.presenter.sorteaza_dupa_varsta()
        self.assertEqual([a.parameters["varsta"] for a in self.presenter.obtine_animale()], [2, 10])
        self.presenter.sorteaza_dupa_greutate()
        self.assertEqual([a.parameters["greutate"] for a in self.presenter.obtine_animale()], [2, 10])
        self.presenter.sorteaza_dupa_nume()
        self.assertEqual([a.parameters["nume"] for a in self.presenter.obtine_animale()], ["A", "z"])
        self.assertEqual(self.presenter.obtine_medie_varsta_categorii(), {"Erbivor": 6})
        self.assertEqual(self.presenter.obtine_medie_greutate_categorii(), {"Erbivor": 6})

    def test_validare_si_rollback(self):
        for value in ("nan", "inf", "-1", "abc"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.presenter.adauga_animal("Test", value, "1", "Erbivor")
        animal = self.presenter.obtine_animale()[0]
        original = dict(animal.parameters)
        with self.assertRaises(ValueError):
            self.presenter.editeaza_animal(animal, "Modificat", "-1", "1", "Erbivor")
        self.assertEqual(animal.parameters, original)
        with self.assertRaises(RuntimeError):
            with self.database.transaction() as connection:
                connection.execute("DELETE FROM animale")
                raise RuntimeError("rollback")
        self.assertEqual(len(self.restart().obtine_animale()), 30)
        with self.assertRaises(ValueError):
            self.presenter.repository.toate("nume; DROP TABLE animale")
