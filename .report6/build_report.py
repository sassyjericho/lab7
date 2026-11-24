from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from lxml import etree
from PIL import Image, ImageDraw, ImageFont


class ReportBuilder:
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    NS = {'w': W, 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
          'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

    def __init__(self):
        self.reference = Path('.report6/reference.docx')
        with ZipFile(self.reference) as source:
            self.parts = {item.filename: source.read(item.filename) for item in source.infolist()}
        self.root = etree.fromstring(self.parts['word/document.xml'])
        self.body = self.root.find('w:body', self.NS)
        self.paragraphs = self.body.findall('w:p', self.NS)
        self.section = deepcopy(self.body.find('w:sectPr', self.NS))
        self.evidence = json.loads(Path('.report6/evidence.json').read_text(encoding='utf-8'))

    def element(self, name, **attributes):
        element = etree.Element(f'{{{self.W}}}{name}')
        for key, value in attributes.items():
            element.set(f'{{{self.W}}}{key}', str(value))
        return element

    def paragraph(self, template, text, page=False, keep=False):
        source = self.paragraphs[template]
        paragraph = deepcopy(source)
        for child in list(paragraph):
            if child.tag != f'{{{self.W}}}pPr':
                paragraph.remove(child)
        properties = paragraph.find('w:pPr', self.NS)
        if properties is None:
            properties = self.element('pPr')
            paragraph.insert(0, properties)
        if page:
            properties.append(self.element('pageBreakBefore'))
        if keep:
            properties.append(self.element('keepNext'))
        run = self.element('r')
        formatting = source.find('w:r/w:rPr', self.NS)
        if formatting is not None:
            run.append(deepcopy(formatting))
        node = self.element('t')
        node.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
        node.text = text
        run.append(node)
        paragraph.append(run)
        self.body.append(paragraph)
        return paragraph

    def heading(self, text, page=False):
        return self.paragraph(58, text, page=page, keep=True)

    def prose(self, text):
        return self.paragraph(50, text)

    def evidence_image(self, key, heading):
        text = self.evidence[key]
        if key == 'schema':
            text = '\n'.join(line.strip() for line in text.splitlines())
        if key == 'tests':
            text = text.replace(' (test_database.DatabaseTests)', '')
        font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 23)
        title_font = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 26)
        lines = text.splitlines()
        width = max(1050, int(max(font.getlength(line) for line in lines)) + 64)
        image = Image.new('RGB', (width, 100 + 33 * len(lines)), '#1f1f1f')
        draw = ImageDraw.Draw(image)
        draw.text((28, 20), heading, font=title_font, fill='white')
        for index, line in enumerate(lines):
            draw.text((28, 72 + index * 33), line, font=font, fill='#cccccc')
        data = BytesIO()
        image.save(data, format='PNG')
        return data.getvalue(), image.size

    def figure(self, index, key, title, caption):
        data, size = self.evidence_image(key, title)
        self.parts[f'word/media/image{index + 1}.png'] = data
        paragraph = deepcopy(self.paragraphs[(90, 92, 93)[index]])
        width = 5900000
        height = int(width * size[1] / size[0])
        for node in paragraph.findall('.//wp:extent', self.NS) + paragraph.findall('.//a:xfrm/a:ext', self.NS):
            node.set('cx', str(width))
            node.set('cy', str(height))
        self.body.append(paragraph)
        self.prose(caption)

    def build(self):
        inventory = {name: {'size': len(data), 'sha256': sha256(data).hexdigest()} for name, data in self.parts.items()}
        Path('.report6/inventory.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
        Path('.report6/artifact.md').write_text(
            '# Contract pentru raportul 6\n'
            f'Referință: {self.reference.resolve()}\nSHA256: {sha256(self.reference.read_bytes()).hexdigest()}\n'
            'Modelul are 26 pagini conform proprietăților salvate, o secțiune A4 portret. '
            'Margini: sus/jos/dreapta 2 cm, stânga 2,5 cm. Fără tabele. '
            'Font implicit Times New Roman 12 pt. Copertă: instituții 16 pt, Raport 60 pt bold, '
            'număr laborator 14 pt, disciplină 18 pt, autor și profesor 14 pt. '
            'Titluri interioare 14 pt bold centrate, subtitluri 12 pt bold. '
            'Cod Consolas 10,5 pt, fundal 1F1F1F, spațiere minimă 14,25 pt.\n'
            'Păstrare: toate părțile ZIP în afară de document.xml și cele trei imagini cu rezultate. '
            'Coperta p0–45 se păstrează; p20 numărul 4 devine 6. '
            'p46 și p48: număr și temă. p49–56: sarcina nouă. p58 și p60: efectuare și arbore. '
            'p88–96: trei imagini cu rezultatele actuale. p97–106: concluzii. '
            'p108 și următoarele: anexa cu fișierele relevante integrării. '
            'Se clonează paragrafele originale pentru conținutul nou. '
            'Styles, numbering, relații, footer și restul părților sunt păstrate byte-for-byte.\n'
            'Randarea de referință: render_docx.py indisponibil din lipsa LibreOffice; export Word încercat. '
            'Paginarea vizuală rămâne de verificat dacă exportul Word nu se finalizează.\n', encoding='utf-8')
        for child in list(self.body):
            self.body.remove(child)
        for index in range(46):
            paragraph = deepcopy(self.paragraphs[index])
            if index == 20:
                for node in paragraph.findall('.//w:t', self.NS):
                    if node.text == '4':
                        node.text = '6'
            self.body.append(paragraph)
        self.paragraph(46, 'Lucrarea de laborator Nr. 6', page=True)
        self.paragraph(48, 'Integrarea unei baze de date în proiectul curent')
        self.heading('Mersul Lucrării:')
        self.prose('Integrarea în proiectul curent a unei baze de date, ca exemplu PostgreSQL, pentru stocarea și prelucrarea datelor. Configurarea bazei de date poate fi făcută urmând tutorialul PostgreSQL Tutorial. Pentru interacțiunea cu PostgreSQL se va utiliza librăria pentru Python psycopg. Din considerente obiective este permisă utilizarea unei alte baze de date, la alegerea studentului.')
        self.prose('Listele create în laboratorul 1 vor fi înlocuite cu baza de date. Vor fi implementate metodele necesare pentru crearea cererilor și primirea răspunsurilor de la baza de date. Ștergerea, adăugarea, sortarea și alte operațiuni cu datele se vor realiza prin intermediul bazei de date.')
        self.prose('Implementarea se va face exclusiv prin intermediul claselor, care se vor regăsi în fișiere separate conform destinației acestora. Funcționalul aflat în afara claselor nu va fi luat în considerare la atribuirea notei pentru lucrarea de laborator.')
        self.heading('Efectuarea lucrării:')
        self.prose('În aplicația de gestionare a animalelor am înlocuit lista păstrată în Presenter cu stocarea persistentă într-o bază de date SQLite. Alegerea SQLite este justificată de utilizarea locală a aplicației desktop: baza este un fișier, nu necesită administrarea unui server și poate fi accesată prin modulul sqlite3 inclus în Python. Această alegere utilizează alternativa permisă în enunț. Librăria psycopg este destinată PostgreSQL; pentru SQLite este folosit driverul sqlite3.')
        self.prose('La prima pornire se creează fișierul data/animale.sqlite3 și sunt inserate cele 30 de animale inițiale. Tabelul initializare reține versiunea populării, astfel încât ștergerea tuturor înregistrărilor nu determină recrearea lor la repornire. Generatorul existent este utilizat pentru datele inițiale și identificarea claselor, nu pentru stocarea modificărilor utilizatorului.')
        self.heading('Arborele proiectului:', page=True)
        tree = '''piig/
├── __main__.py
├── application.py
├── requirements.txt
├── README.md
├── data/
│   └── animale.sqlite3 (creat la prima pornire)
├── images/
│   └── imaginile animalelor
├── model/
│   ├── __init__.py
│   ├── database.py
│   ├── animal_repository.py
│   ├── animal_custom.py
│   ├── generator.py
│   ├── statistici_animale.py
│   ├── image_factory.py
│   ├── animale/
│   │   ├── carnivore.py
│   │   ├── erbivore.py
│   │   └── omnivore.py
│   ├── base_class/base_class.py
│   └── interface/interface.py
├── presenter/presenter.py
├── view/
│   ├── view.py
│   └── chart_frame.py
└── tests/test_database.py'''
        for line in tree.splitlines():
            self.paragraph(61, line)
        self.prose('Database gestionează conexiunile și tranzacțiile. AnimalRepository definește schema, validează datele și execută SQL. Presenter coordonează operațiile cerute de interfață. Application pornește aplicația, iar clasele din view afișează rezultatele și mesajele de eroare.')
        self.heading('Organizarea datelor și a operațiilor', page=True)
        self.prose('Tabelul animale conține câmpurile id, tip, nume, varsta, greutate, categorie și detalii. ID-ul este cheia primară generată automat. Vârsta și greutatea sunt valori numerice nenegative, categoria este limitată la Erbivor, Carnivor sau Omnivor, iar numele nu poate fi gol. Câmpul detalii păstrează în format JSON atributele specifice fiecărei specii.')
        self.prose('Metoda adauga execută INSERT și reține identificatorul generat. Metoda toate execută SELECT și reconstruiește obiectele, păstrând clasa animalului și imaginea asociată. Metoda actualizeaza execută UPDATE după ID, iar sterge folosește DELETE pentru unul sau mai multe ID-uri, în aceeași tranzacție.')
        self.prose('Sortarea se execută prin ORDER BY, după nume, vârstă sau greutate. Presenter păstrează numai criteriul selectat, iar interfața primește rezultatul unei citiri noi din baza de date. Listele returnate de SELECT sunt rezultate temporare de afișare; nu reprezintă sursa persistentă a datelor.')
        self.prose('Pentru grafice se folosesc COUNT și AVG împreună cu GROUP BY categorie. Astfel, distribuția animalelor și mediile de vârstă și greutate sunt calculate de baza de date. Metodele distributie și medie întorc rezultatele către Presenter și apoi către fereastra cu grafice.')
        self.prose('Valorile utilizatorului sunt transmise prin parametri SQL, iar criteriile de sortare și agregare sunt verificate într-un set fix. Datele numerice acceptă și virgula zecimală, dar resping valori negative, NaN sau infinit. La succes se efectuează commit, iar la excepție tranzacția este anulată prin rollback. Conexiunea este închisă în blocul finally.')
        self.prose('Aplicația se pornește prin comanda python . din directorul proiectului, după instalarea dependențelor cu python -m pip install -r requirements.txt. Punctul de intrare __main__.py apelează Application.run(); logica aplicației se află în metodele claselor.')
        self.heading('Rezultatele simulării', page=True)
        self.figure(0, 'schema', 'Schema citita din sqlite_master', 'Figura 1. Definiția tabelului animale, citită din baza de date creată de aplicație.')
        self.prose('Schema a fost extrasă printr-o interogare a sqlite_master. Constrângerile asigură identificarea unică a înregistrărilor și limitează valorile acceptate pentru câmpurile principale.')
        self.figure(1, 'crud', 'Verificarea operatiilor si a persistentei', 'Figura 2. Rezultatele executării operațiilor de adăugare, editare, ștergere și redeschidere a bazei de date.')
        self.prose('Scenariul a fost executat pe o bază temporară: numărul de animale a crescut de la 30 la 31 după adăugare și a revenit la 30 după ștergere. Animalul adăugat a fost regăsit după redeschidere. După ștergerea totală, baza a rămas goală și la reinițializarea repository-ului.')
        self.heading('Rezultatele simulării continuare', page=True)
        self.figure(2, 'tests', 'python -B -m unittest discover -s tests -v', 'Figura 3. Rezultatul rulării celor cinci teste automate de integrare.')
        self.prose('Testele verifică inițializarea unică și tipurile animalelor, persistența operațiilor CRUD și a detaliilor, ștergerea totală fără repopulare, sortarea numerică și agregările, precum și validarea datelor și rollback-ul. Toate cele cinci teste au trecut. Bazele temporare utilizate pentru verificare nu modifică datele aplicației.')
        self.heading('Concluzii:')
        for text in (
            'În cadrul lucrării de laborator nr. 6 am integrat baza de date SQLite în aplicația de gestionare a animalelor, înlocuind lista din memorie cu stocarea persistentă.',
            'Adăugarea, editarea, ștergerea individuală și multiplă sunt realizate prin interogări SQL. Sortarea și statisticile pentru grafice sunt calculate tot în baza de date.',
            'Identificatorii persistenți permit modificarea și ștergerea înregistrărilor după reîncărcare. Mecanismul de inițializare păstrează ștergerile utilizatorului la repornirea aplicației.',
            'Separarea responsabilităților în clasele Database, AnimalRepository, Presenter și Application păstrează organizarea proiectului. Interfața existentă continuă să afișeze animalele și să apeleze operațiile prin Presenter.',
            'Verificările efectuate confirmă persistența, corectitudinea operațiilor principale și anularea tranzacțiilor în caz de eroare. Alegerea SQLite permite rularea locală fără configurarea unui server separat.'
        ):
            self.prose(text)
        self.heading('Anexa', page=True)
        self.prose('Codul claselor introduse sau adaptate pentru integrarea bazei de date și al testelor de verificare este prezentat mai jos. Clasele de animale, generatorul și componentele grafice existente completează structura proiectului.')
        for file_index, filename in enumerate(('model/database.py', 'model/animal_repository.py', 'presenter/presenter.py', 'model/animal_custom.py', 'application.py', 'tests/test_database.py')):
            self.heading(filename, page=file_index > 0)
            for line in Path(filename).read_text(encoding='utf-8').splitlines():
                paragraph = self.paragraph(112, line or ' ')
                run_properties = paragraph.find('w:r/w:rPr', self.NS)
                if run_properties is not None:
                    for color in run_properties.findall('w:color', self.NS):
                        color.set(f'{{{self.W}}}val', 'CCCCCC')
        self.body.append(self.section)
        self.parts['word/document.xml'] = etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, standalone=True)
        output = Path('LAB 6 PIG.docx')
        with ZipFile(output, 'w', ZIP_DEFLATED) as destination:
            for name, data in self.parts.items():
                destination.writestr(name, data)
        with ZipFile(self.reference) as source, ZipFile(output) as final:
            changed = [name for name in source.namelist() if source.read(name) != final.read(name)]
        assert set(changed) == {'word/document.xml', 'word/media/image1.png', 'word/media/image2.png', 'word/media/image3.png'}, changed
        print('Created:', output.resolve())
        print('Changed package parts:', changed)


if __name__ == '__main__':
    ReportBuilder().build()
