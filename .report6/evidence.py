import json
import sys
import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model.database import Database
from model.animal_repository import AnimalRepository
from presenter.presenter import Presenter


class Evidence:
    @classmethod
    def run(cls):
        with TemporaryDirectory() as directory:
            database = Database(Path(directory) / 'animale.sqlite3')
            presenter = Presenter(AnimalRepository(database))
            with database.transaction() as connection:
                schema = connection.execute("SELECT sql FROM sqlite_master WHERE name='animale'").fetchone()[0]
            initial = len(presenter.obtine_animale())
            animal = presenter.adauga_animal('Test laborator 6', '2', '3,5', 'Erbivor')
            after_add = len(presenter.obtine_animale())
            restart = Presenter(AnimalRepository(database))
            restored = next(a for a in restart.obtine_animale() if a.database_id == animal.database_id)
            restart.editeaza_animal(restored, 'Test actualizat', '3', '4', 'Omnivor')
            restart.sterge_animal(restored)
            after_delete = len(Presenter(AnimalRepository(database)).obtine_animale())
            stats = presenter.obtine_distributie_categorii()
            presenter.sterge_animale(presenter.obtine_animale())
            empty = len(Presenter(AnimalRepository(database)).obtine_animale())
        stream = StringIO()
        tests = unittest.defaultTestLoader.discover('tests')
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(tests)
        assert result.wasSuccessful()
        output = {
            'schema': schema,
            'crud': f'Animale la initializare: {initial}\nDupa INSERT: {after_add}\nDupa redeschidere: ID {animal.database_id} regasit\nUPDATE: Test actualizat, varsta 3, greutate 4\nDupa DELETE si redeschidere: {after_delete}\nDistributie: {stats}\nDupa stergere totala si redeschidere: {empty}',
            'tests': stream.getvalue(),
        }
        Path('.report6/evidence.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    Evidence.run()
