import json
from math import isfinite

from model.animal_custom import AnimalCustom
from model.base_class.base_class import BaseClass
from model.database import Database
from model.generator import GeneratorAnimale
from model.statistici_animale import StatisticiAnimale


class AnimalRepository:
    CATEGORII = ("Erbivor", "Carnivor", "Omnivor")
    SORTARI = {"id": "id", "nume": "LOWER(nume), id", "varsta": "varsta, id", "greutate": "greutate, id"}

    def __init__(self, database=None):
        self.database = database or Database()
        self.statistici = StatisticiAnimale()
        self.tipuri = {type(a).__name__: type(a) for a in GeneratorAnimale().genereaza_toate_animalele()}
        self.tipuri["AnimalCustom"] = AnimalCustom
        self.initialize()

    def initialize(self):
        with self.database.transaction() as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute("""CREATE TABLE IF NOT EXISTS animale (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tip TEXT NOT NULL,
                nume TEXT NOT NULL CHECK(length(trim(nume)) > 0),
                varsta REAL NOT NULL CHECK(varsta >= 0),
                greutate REAL NOT NULL CHECK(greutate >= 0),
                categorie TEXT NOT NULL CHECK(categorie IN ('Erbivor', 'Carnivor', 'Omnivor')),
                detalii TEXT NOT NULL
            )""")
            connection.execute("CREATE TABLE IF NOT EXISTS initializare (versiune INTEGER PRIMARY KEY)")
            if connection.execute("SELECT 1 FROM initializare WHERE versiune = 1").fetchone() is None:
                for animal in GeneratorAnimale().genereaza_toate_animalele():
                    self._insert(connection, animal)
                connection.execute("INSERT INTO initializare VALUES (1)")

    def _values(self, animal):
        params = animal.parameters
        nume = str(params.get("nume", "")).strip()
        categorie = self.statistici.get_categorie(animal)
        if not nume or categorie not in self.CATEGORII:
            raise ValueError("Introduceți un nume și o categorie validă.")
        numbers = []
        for key in ("varsta", "greutate"):
            try:
                value = float(str(params.get(key, "")).replace(",", "."))
            except (ValueError, TypeError):
                raise ValueError("Vârsta și greutatea trebuie să fie numere nenegative.") from None
            if not isfinite(value) or value < 0:
                raise ValueError("Vârsta și greutatea trebuie să fie numere finite, nenegative.")
            numbers.append(value)
        details = {k: v for k, v in params.items() if k not in {"nume", "varsta", "greutate", "categorie"}}
        return (type(animal).__name__, nume, *numbers, categorie, json.dumps(details, ensure_ascii=False, allow_nan=False))

    def _insert(self, connection, animal):
        cursor = connection.execute(
            "INSERT INTO animale (tip, nume, varsta, greutate, categorie, detalii) VALUES (?, ?, ?, ?, ?, ?)",
            self._values(animal),
        )
        return cursor.lastrowid

    def _animal(self, row):
        cls = self.tipuri.get(row["tip"], AnimalCustom)
        animal = cls.__new__(cls)
        BaseClass.__init__(animal)
        animal.parameters.update(json.loads(row["detalii"]))
        animal.parameters.update({key: row[key] for key in ("nume", "varsta", "greutate", "categorie")})
        animal.database_id = row["id"]
        return animal

    def toate(self, sortare="id"):
        if sortare not in self.SORTARI:
            raise ValueError("Criteriu de sortare invalid.")
        with self.database.transaction() as connection:
            rows = connection.execute("SELECT * FROM animale ORDER BY " + self.SORTARI[sortare]).fetchall()
        return [self._animal(row) for row in rows]

    def adauga(self, animal):
        with self.database.transaction() as connection:
            identifier = self._insert(connection, animal)
        animal.database_id = identifier
        return animal

    def actualizeaza(self, identifier, animal):
        with self.database.transaction() as connection:
            cursor = connection.execute(
                "UPDATE animale SET tip=?, nume=?, varsta=?, greutate=?, categorie=?, detalii=? WHERE id=?",
                (*self._values(animal), identifier),
            )
            if cursor.rowcount != 1:
                raise ValueError("Animalul nu mai există în baza de date.")
        animal.database_id = identifier
        return animal

    def sterge(self, identifiers):
        with self.database.transaction() as connection:
            connection.executemany("DELETE FROM animale WHERE id=?", ((identifier,) for identifier in identifiers))

    def distributie(self):
        with self.database.transaction() as connection:
            rows = connection.execute("SELECT categorie, COUNT(*) FROM animale GROUP BY categorie").fetchall()
        result = dict.fromkeys(self.CATEGORII, 0)
        result.update(dict(rows))
        return result

    def medie(self, parametru):
        if parametru not in {"varsta", "greutate"}:
            raise ValueError("Parametru statistic invalid.")
        with self.database.transaction() as connection:
            rows = connection.execute("SELECT categorie, AVG(" + parametru + ") FROM animale GROUP BY categorie").fetchall()
        return {row[0]: round(row[1], 2) for row in rows}
