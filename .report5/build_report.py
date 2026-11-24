from copy import deepcopy
from hashlib import sha256
import ast
import json
from pathlib import Path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree
from PIL import Image

sys.path.insert(0, str(Path('.report6').resolve()))
from build_report import ReportBuilder


class ReportGrafice(ReportBuilder):
    def picture(self, index, name, caption):
        path = Path('.report5') / name
        self.parts[f'word/media/image{index + 1}.png'] = path.read_bytes()
        with Image.open(path) as image:
            width, height = image.size
        paragraph = deepcopy(self.paragraphs[(90, 92, 93)[index]])
        for node in paragraph.findall('.//wp:extent', self.NS) + paragraph.findall('.//a:xfrm/a:ext', self.NS):
            node.set('cx', '5900000')
            node.set('cy', str(int(5900000 * height / width)))
        self.body.append(paragraph)
        self.prose(caption)

    def code(self, text):
        for line in text.splitlines():
            paragraph = self.paragraph(112, line or ' ')
            properties = paragraph.find('w:r/w:rPr', self.NS)
            if properties is not None:
                for color in properties.findall('w:color', self.NS):
                    color.set(f'{{{self.W}}}val', 'CCCCCC')

    def excerpt(self, filename, class_name, methods):
        source = Path(filename).read_text(encoding='utf-8')
        lines = source.splitlines()
        tree = ast.parse(source)
        node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name)
        output = [lines[node.lineno - 1]]
        for method in node.body:
            if isinstance(method, ast.FunctionDef) and method.name in methods:
                output.extend([''] + lines[method.lineno - 1:method.end_lineno])
        return '\n'.join(output)

    def build(self):
        results = json.loads(Path('.report5/rezultate.json').read_text(encoding='utf-8'))
        assert results['initial']['distributie'] == {'Erbivor': 10, 'Carnivor': 10, 'Omnivor': 10}
        for child in list(self.body):
            self.body.remove(child)
        for index in range(41):
            paragraph = deepcopy(self.paragraphs[index])
            if index == 20:
                for text in paragraph.findall('.//w:t', self.NS):
                    if text.text == '4':
                        text.text = '5'
            self.body.append(paragraph)
        self.paragraph(46, 'Lucrarea de laborator Nr. 5', page=True)
        self.paragraph(48, 'Afișarea informației prin intermediul graficelor')
        self.heading('Mersul lucrării:')
        self.prose('Integrarea în proiectul curent a unei biblioteci care va permite construirea graficelor în baza datelor caracteristice proiectului. Este recomandată biblioteca Matplotlib, care este o bibliotecă cuprinzătoare pentru crearea de vizualizări statice, animate și interactive în Python.')
        self.prose('Integrarea graficelor se va face prin intermediul unui cadru distinct, care va fi implementat într-o clasă aparte. Funcționalitățile vor fi implementate în Presenter, care la rândul său va chema metodele necesare din Model.')
        self.prose('Implementarea se va face exclusiv prin intermediul claselor, care se vor regăsi în fișiere separate conform destinației acestora. Funcționalul aflat în afara claselor nu va fi luat în considerare la atribuirea notei pentru lucrarea de laborator.')
        self.heading('Efectuarea lucrării:')
        self.prose('În aplicația de gestionare a animalelor am integrat biblioteca Matplotlib pentru a reprezenta datele prin trei diagrame cu bare: numărul animalelor din fiecare categorie, greutatea medie și vârsta medie. Graficele sintetizează informațiile existente în proiect și permit compararea categoriilor Erbivor, Carnivor și Omnivor.')
        self.prose('Cadrul GraficAnimaleFrame este definit în fișierul view/chart_frame.py și moștenește CTkFrame. El este afișat într-o fereastră separată, deschisă prin butonul „Afișează grafice”. Clasa primește rezultatele statistice de la interfață, configurează diagramele și actualizează desenul.')
        self.prose('Presenter pune la dispoziție metodele obtine_distributie_categorii(), obtine_medie_greutate_categorii() și obtine_medie_varsta_categorii(). Acestea solicită rezultatele din Model. În versiunea curentă a proiectului, extinsă ulterior cu baza de date, metodele apelează AnimalRepository; calculele sunt realizate în Model prin COUNT, AVG și GROUP BY. Clasa StatisticiAnimale conține și metodele de calcul pe colecții dezvoltate pentru grafice.')
        self.heading('Arborele proiectului:', page=True)
        tree = '''piig/
├── __main__.py
├── application.py
├── requirements.txt
├── images/
├── model/
│   ├── statistici_animale.py
│   ├── generator.py
│   ├── animal_custom.py
│   ├── animal_repository.py
│   ├── database.py
│   ├── animale/
│   │   ├── erbivore.py
│   │   ├── carnivore.py
│   │   └── omnivore.py
│   ├── base_class/base_class.py
│   └── interface/interface.py
├── presenter/
│   └── presenter.py
└── view/
    ├── view.py
    └── chart_frame.py'''
        for line in tree.splitlines():
            self.paragraph(61, line)
        self.prose('Fluxul datelor este: AplicatieAnimale → Presenter → Model → Presenter → AplicatieAnimale → GraficAnimaleFrame. Interfața solicită statisticile, Presenter apelează Model, iar cadrul grafic primește dicționarele cu valori. Metodele de desenare nu citesc direct baza de date și nu calculează mediile.')
        self.heading('Construirea și actualizarea graficelor', page=True)
        self.prose('Metoda _setup_chart() creează un obiect Figure și trei obiecte Axes prin subplots(1, 3). Figure reprezintă figura completă, iar fiecare Axes conține o diagramă. FigureCanvasTkAgg integrează figura Matplotlib în cadrul CustomTkinter. Implementarea utilizează obiectele Figure și Axes, potrivit interfeței orientate pe obiecte descrise în documentația Matplotlib.')
        self.prose('Metoda _deseneaza_bare() curăță axa, setează titlul, unitatea de măsură, culorile categoriilor și etichetele numerice. Pentru numărul de animale este utilizat MaxNLocator(integer=True), astfel încât axa verticală să aibă gradații întregi. Limita superioară a axei lasă spațiu pentru etichetele afișate deasupra barelor.')
        self.prose('Distribuția reprezintă numărul animalelor din fiecare categorie. Greutatea medie este raportul dintre suma greutăților și numărul animalelor categoriei, iar vârsta medie se calculează analog. Mediile sunt rotunjite la două zecimale. În Model, clasa StatisticiAnimale acceptă valori numerice finite și nenegative, inclusiv șiruri cu virgulă zecimală. În versiunea cu SQLite, datele sunt validate înainte de salvare și apoi agregate în repository.')
        self.prose('Butonul „Afișează grafice” apelează on_afiseaza_grafice(), care creează fereastra CTkToplevel și cadrul GraficAnimaleFrame. Dacă fereastra este deja deschisă, aplicația o focalizează și îi actualizează datele. La închidere, referințele către fereastră și cadru sunt eliberate.')
        self.prose('După adăugare, editare sau ștergere, metoda afiseaza_animale() apelează actualizeaza_grafice(). Aceasta obține cele trei seturi de date prin Presenter și le transmite metodei actualizeaza_grafice() a cadrului. Apelul canvas.draw_idle() programează redesenarea. Sortarea schimbă ordinea afișării animalelor, dar nu valorile statistice.')
        self.prose('Dacă nu există animale sau valori pentru o diagramă, cadrul afișează mesajul „Nu există date valide”. Această situație este tratată în metoda _deseneaza_bare(), fără a produce medii artificiale pentru categorii fără date.')
        self.prose('Pornirea proiectului: python -m pip install -r requirements.txt, apoi python . din directorul proiectului. Biblioteca Matplotlib este declarată în requirements.txt împreună cu CustomTkinter și Pillow.')
        self.heading('Rezultatele simulării', page=True)
        self.picture(0, 'aplicatie.png', 'Figura 1. Captură reală a ferestrei aplicației și a butonului „Afișează grafice”.')
        self.prose('Pentru verificare a fost folosit setul inițial de 30 de animale într-o bază temporară, fără modificarea datelor utilizatorului. Aplicația a fost pornită, iar fereastra cu grafice a fost deschisă prin metoda asociată butonului.')
        self.heading('Rezultatele simulării continuare', page=True)
        self.picture(1, 'grafice_initial.png', 'Figura 2. Captură reală a cadrului GraficAnimaleFrame pentru cele 30 de animale inițiale.')
        initial = results['initial']
        for category in ('Erbivor', 'Carnivor', 'Omnivor'):
            weight = str(initial['greutate'][category]).replace('.', ',')
            age = str(initial['varsta'][category]).replace('.', ',')
            self.prose(f"{category}: {initial['distributie'][category]} animale, greutatea medie {weight} kg și vârsta medie {age} ani.")
        self.picture(2, 'grafice_actualizate.png', 'Figura 3. Captură reală după adăugarea unui erbivor cu vârsta de 5 ani și greutatea de 100 kg.')
        self.prose('După adăugare, totalul devine 31 de animale, iar numărul erbivorelor crește la 11. Greutatea medie a erbivorelor devine 557,05 kg, iar vârsta medie 4,91 ani. Modificarea este vizibilă în cadrul deja deschis, fără redeschiderea ferestrei.')
        self.heading('Concluzii:', page=True)
        self.prose('În cadrul lucrării de laborator nr. 5 am integrat biblioteca Matplotlib în aplicația de gestionare a animalelor. Datele proiectului sunt reprezentate prin trei diagrame cu bare, afișate în cadrul distinct GraficAnimaleFrame.')
        self.prose('Separarea responsabilităților respectă arhitectura MVP: Model furnizează datele statistice, Presenter expune metodele necesare, iar View afișează rezultatele prin cadrul grafic. Logica de calcul și logica de desenare sunt organizate în clase și fișiere separate.')
        self.prose('Verificarea în aplicație a confirmat actualizarea graficelor după adăugare, editare și ștergere. Mutarea animalului demonstrativ la categoria Carnivor a modificat distribuția la 10 erbivore, 11 carnivore și 10 omnivore, iar ștergerea lui a restabilit statisticile inițiale. Pentru setul gol, toate cele trei diagrame au afișat mesajul „Nu există date valide”.')
        self.prose('Graficele permit compararea rapidă a categoriilor și a valorilor medii. Capturile incluse reprezintă ferestre reale ale aplicației în timpul verificării, iar valorile afișate au fost comparate cu rezultatele metodelor din Presenter.')
        self.prose('Documentație consultată: Matplotlib, Quick start guide — https://matplotlib.org/stable/users/explain/quick_start.html. Structura și fragmentele de cod prezentate corespund fișierelor proiectului curent.')
        self.heading('Anexa', page=True)
        self.prose('Codul relevant pentru construirea graficelor și legătura dintre Model, Presenter și View. Fragmentele marcate ca extrase păstrează metodele din proiectul curent; fișierele complete conțin și celelalte funcționalități ale aplicației.')
        self.heading('model/statistici_animale.py')
        self.code(Path('model/statistici_animale.py').read_text(encoding='utf-8'))
        self.heading('view/chart_frame.py', page=True)
        self.code(Path('view/chart_frame.py').read_text(encoding='utf-8'))
        self.heading('presenter/presenter.py — extras', page=True)
        self.code(self.excerpt('presenter/presenter.py', 'Presenter', {'obtine_distributie_categorii', 'obtine_medie_greutate_categorii', 'obtine_medie_varsta_categorii'}))
        self.heading('model/animal_repository.py — extras')
        self.code(self.excerpt('model/animal_repository.py', 'AnimalRepository', {'distributie', 'medie'}))
        self.heading('view/view.py — extras', page=True)
        self.code(self.excerpt('view/view.py', 'AplicatieAnimale', {'afiseaza_animale', 'actualizeaza_grafice', 'on_afiseaza_grafice', 'on_inchide_fereastra_grafice'}))
        self.body.append(self.section)
        self.parts['word/document.xml'] = etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, standalone=True)
        output = Path('LAB 5 PIG - raport final.docx')
        with ZipFile(output, 'w', ZIP_DEFLATED) as final:
            for name, data in self.parts.items():
                final.writestr(name, data)
        with ZipFile(self.reference) as reference, ZipFile(output) as final:
            changed = [name for name in reference.namelist() if reference.read(name) != final.read(name)]
        assert set(changed) == {'word/document.xml', 'word/media/image1.png', 'word/media/image2.png', 'word/media/image3.png'}
        contract = Path('.report6/artifact.md').read_text(encoding='utf-8')
        Path('.report5/artifact.md').write_text(contract + '\nAdaptare LL5: copertă și titlu 5; tema Matplotlib; aceleași roluri tipografice; trei capturi reale ale aplicației; cod relevant graficelor. Fișierul LL5 existent este păstrat.\n', encoding='utf-8')
        print(output.resolve())


if __name__ == '__main__':
    ReportGrafice().build()
