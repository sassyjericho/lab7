import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from PIL import ImageGrab

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model.database import Database
from model.animal_repository import AnimalRepository
from presenter.presenter import Presenter
from view.view import AplicatieAnimale


class CapturiLucrare:
    def __init__(self):
        self.folder = TemporaryDirectory()
        self.presenter = Presenter(AnimalRepository(Database(Path(self.folder.name) / 'demo.sqlite3')))
        with patch('view.view.Presenter', return_value=self.presenter):
            self.app = AplicatieAnimale()
        self.app.geometry('980x650+100+100')
        self.results = {}
        self.error = None

    def capture(self, window, filename):
        window.lift()
        window.attributes('-topmost', True)
        window.update()
        x, y = window.winfo_rootx(), window.winfo_rooty()
        ImageGrab.grab(bbox=(x, y, x + window.winfo_width(), y + window.winfo_height())).save('.report5/' + filename)
        window.attributes('-topmost', False)

    def statistics(self):
        return {'distributie': self.presenter.obtine_distributie_categorii(),
                'greutate': self.presenter.obtine_medie_greutate_categorii(),
                'varsta': self.presenter.obtine_medie_varsta_categorii()}

    def initial(self):
        self.capture(self.app, 'aplicatie.png')
        self.app.on_afiseaza_grafice()
        self.app.grafice_window.geometry('1100x480+100+100')
        self.app.after(1500, self.charts)

    def charts(self):
        self.results['initial'] = self.statistics()
        self.capture(self.app.grafice_window, 'grafice_initial.png')
        self.app.adauga_animal('Exemplu laborator 5', '5', '100', 'Erbivor')
        self.app.after(1500, self.modified)

    def modified(self):
        self.results['adaugare'] = self.statistics()
        assert self.results['adaugare']['distributie']['Erbivor'] == 11
        assert self.results['adaugare']['greutate']['Erbivor'] == 557.05
        self.capture(self.app.grafice_window, 'grafice_actualizate.png')
        animal = next(a for a in self.presenter.obtine_animale() if a.parameters['nume'] == 'Exemplu laborator 5')
        self.app.editare_animal(animal, 'Exemplu laborator 5', '5', '100', 'Carnivor')
        assert self.statistics()['distributie'] == {'Erbivor': 10, 'Carnivor': 11, 'Omnivor': 10}
        self.app.sterge_animal(animal)
        assert self.statistics() == self.results['initial']
        self.presenter.sterge_animale(self.presenter.obtine_animale())
        self.app.afiseaza_animale()
        self.app.update()
        assert all(any(text.get_text() == 'Nu există date valide' for text in axis.texts)
                   for axis in self.app.grafic_frame.figure.axes)
        self.results['verificari'] = 'Adaugare, editare, stergere, actualizare grafice si set gol: OK'
        Path('.report5/rezultate.json').write_text(json.dumps(self.results, ensure_ascii=False, indent=2), encoding='utf-8')
        self.app.destroy()

    def failed(self, kind, value, trace):
        self.error = value
        self.app.destroy()

    def run(self):
        self.app.report_callback_exception = self.failed
        self.app.after(1500, self.initial)
        try:
            self.app.mainloop()
            if self.error:
                raise self.error
        finally:
            self.folder.cleanup()


if __name__ == '__main__':
    CapturiLucrare().run()
