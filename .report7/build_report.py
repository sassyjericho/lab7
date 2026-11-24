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
        self.reference = Path('.report7/reference.docx')
        with ZipFile(self.reference) as source:
            self.parts = {item.filename: source.read(item.filename) for item in source.infolist()}
        self.root = etree.fromstring(self.parts['word/document.xml'])
        self.body = self.root.find('w:body', self.NS)
        self.paragraphs = self.body.findall('w:p', self.NS)
        self.section = deepcopy(self.body.find('w:sectPr', self.NS))
        self.evidence = json.loads(Path('.report7/evidence.json').read_text(encoding='utf-8'))

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

    def interface_screenshot(self, filename, caption):
        data = Path(filename).read_bytes()
        image = Image.open(BytesIO(data))
        size = image.size
        self.parts['word/media/image4.png'] = data

        relationship = etree.fromstring(self.parts['word/_rels/document.xml.rels'])
        rel = etree.Element(
            '{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',
            Id='rId15',
            Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/image',
            Target='media/image4.png',
        )
        relationship.append(rel)
        self.parts['word/_rels/document.xml.rels'] = etree.tostring(
            relationship, encoding='UTF-8', xml_declaration=True, standalone=True
        )

        paragraph = deepcopy(self.paragraphs[90])
        width = 5900000
        height = int(width * size[1] / size[0])
        for node in paragraph.findall('.//wp:extent', self.NS) + paragraph.findall('.//a:xfrm/a:ext', self.NS):
            node.set('cx', str(width))
            node.set('cy', str(height))
        for node in paragraph.findall('.//a:blip', self.NS):
            node.set(
                '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed',
                'rId15',
            )
        self.body.append(paragraph)
        self.prose(caption)

    def build(self):
        inventory = {name: {'size': len(data), 'sha256': sha256(data).hexdigest()} for name, data in self.parts.items()}
        Path('.report7/inventory.json').write_text(json.dumps(inventory, indent=2), encoding='utf-8')
        Path('.report7/artifact.md').write_text(
            '# Contract pentru raportul 7\n'
            f'Referință: {self.reference.resolve()}\nSHA256: {sha256(self.reference.read_bytes()).hexdigest()}\n'
            'Modelul are 26 pagini conform proprietăților salvate, o secțiune A4 portret. '
            'Margini: sus/jos/dreapta 2 cm, stânga 2,5 cm. Fără tabele. '
            'Font implicit Times New Roman 12 pt. Copertă: instituții 16 pt, Raport 60 pt bold, '
            'număr laborator 14 pt, disciplină 18 pt, autor și profesor 14 pt. '
            'Titluri interioare 14 pt bold centrate, subtitluri 12 pt bold. '
            'Cod Consolas 10,5 pt, fundal 1F1F1F, spațiere minimă 14,25 pt.\n'
            'Păstrare: toate părțile ZIP în afară de document.xml și cele trei imagini cu rezultate. '
            'Coperta p0–45 se păstrează; p20 numărul 4 devine 7. '
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
                        node.text = '7'
            self.body.append(paragraph)
        self.paragraph(46, 'Lucrarea de laborator Nr. 7', page=True)
        self.paragraph(48, 'Crearea unui executabil pentru proiectul curent')
        self.heading('Mersul Lucrării:')
        self.prose('Crearea unui executabil pentru sistemul de operare Windows care să conțină proiectul realizat pe parcursul cursului. Pentru generarea executabilului se utilizează PyInstaller, iar livrabilul final este arhivat într-o arhivă ZIP care trebuie să includă atât proiectul sursă, cât și executabilul obținut.')
        self.prose('Executabilul se generează fără consolă, fiind destinat unei aplicații desktop cu interfață grafică. Fișierul principal este __main__.py, care apelează metoda Application.run(). Fișierul Animale.spec descrie punctul de intrare, dependențele colectate și directorul de distribuție.')
        self.prose('Aplicația este construită ca o colecție de fișiere pentru Windows, nu într-un singur fișier executabil monolitic. Directorul dist/Animale conține Animale.exe, biblioteca internă _internal și resursele necesare, inclusiv imaginile animalelor și baza de date SQLite.')
        self.heading('Efectuarea lucrării:')
        self.prose('Executabilul a fost construit cu PyInstaller 6.22.3 pe Python 3.9.13. Comanda folosită pentru înlocuirea build-ului anterior și generarea unei versiuni curente este python -m PyInstaller --noconfirm --clean Animale.spec.')
        self.prose('Fișierul Animale.spec include directorul images și directorul data ca resurse, colectează automat datele și modulele CustomTkinter și configurează EXE fără fereastră de consolă. Modulul SQLite se inițializează la prima rulare în directorul de date al distribuției.')
        self.prose('La rularea executabilului aplicația a rămas activă, iar interfața grafică s-a lansat corect. În plus, cele cinci teste automate ale proiectului au fost executate și toate au trecut.')
        self.heading('Arborele proiectului:', page=True)
        tree = '''piig/
├── __main__.py
├── application.py
├── requirements.txt
├── README.md
├── Animale.spec
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
├── tests/test_database.py
└── dist/
    └── Animale/
        ├── Animale.exe
        ├── data/
        └── _internal/'''
        for line in tree.splitlines():
            self.paragraph(61, line)
        self.prose('Database gestionează baza de date, Repository implementează operațiile de date, Presenter coordonează logica aplicației, iar View afișează interfața. Application pornește proiectul, iar Animale.spec definește modul în care PyInstaller incluie resursele și dependențele în distribuție.')
        self.heading('Configurarea PyInstaller', page=True)
        self.prose('Analiza PyInstaller pornește de la __main__.py. Direcția datas include dosarele images și data, iar hook-ul librăriei CustomTkinter colectează automat fișierele sale grafice și modulele aferente. Modulul hiddenimports poate fi completat atunci când un modul este încărcat dinamic și nu este detectat de analizator.')
        self.prose('Secțiunea EXE configurează numele executabilului, dezactivează consola și folosește COLLECT pentru a construi o distribuție în mai multe fișiere. Această structură este mai potrivită pentru aplicații mari, deoarece permite separarea executabilului principal de resursele și bibliotecile din directorul _internal.')
        self.prose('Aplicarea opțiunii --noconfirm asigură înlocuirea build-ului existent, iar --clean curăță cache-ul PyInstaller înainte de analiză. Ordinea corectă este instalarea dependențelor, verificarea testelor, reconstruirea executabilului și lansarea aplicației finale.')
        self.prose('Pentru menținerea datelor utilizatorului, baza SQLite este copiată la prima rulare din _internal/data în directorul data al executabilului. Aceasta permite aplicației să pornească dintr-o locație diferită și să păstreze modificările între execuții.')
        self.heading('Rezultatele simulării', page=True)
        self.figure(0, 'build', 'Configurarea build-ului PyInstaller', 'Figura 1. Versiunile, punctul de intrare, configurația și dimensiunea executabilului obținut.')
        self.prose('Rezultatul build-ului confirmă utilizarea PyInstaller pe mediul Python din Windows. Executabilul principal este Animale.exe, iar directorul dist/Animale conține resursele și bibliotecile necesare rulării.')
        self.figure(1, 'dist', 'Structura directorului de distributie', 'Figura 2. Structura de nivel superior a directorului dist/Animale creat de PyInstaller.')
        self.prose('Directorul de distribuție conține executabilul principal, dosarul data și dosarul _internal. Acest ultim director include resursele bibliotecilor, imaginile și componentele nativ Windows detectate în timpul construirii.')
        self.interface_screenshot(
            '.report7/interfata_principala.png',
            'Figura 3. Interfața principală a aplicației Animale, lansată din executabilul produs de PyInstaller.',
        )
        self.prose('Screenshot-ul surprinde lista de animale, controalele de sortare și cardurile cu imaginea, numele și atributele fiecărui animal. Captura confirmă încărcarea corectă a resurselor grafice și lansarea interfeței desktop.')
        self.heading('Rezultatele simulării continuare', page=True)
        self.figure(2, 'tests', 'python -B -m unittest discover -s tests -v', 'Figura 3. Rezultatul rulării celor cinci teste automate de integrare.')
        self.prose('Testele verifică inițializarea unică și tipurile animalelor, persistența operațiilor CRUD și a detaliilor, ștergerea totală fără repopulare, sortarea numerică și agregările, precum și validarea datelor și rollback-ul. Toate cele cinci teste au trecut. Bazele temporare utilizate pentru verificare nu modifică datele aplicației.')
        self.heading('Concluzii:')
        for text in (
            'În cadrul lucrării de laborator nr. 7 am creat executabilul Windows al aplicației de gestionare a animalelor cu ajutorul PyInstaller.',
            'Fișierul Animale.spec grupește punctul de intrare, resursele images și data și dependențele CustomTkinter într-o configurație reproductibilă.',
            'Directorul dist/Animale conține executabilul, biblioteca internă și fișierele necesare aplicării. Lansarea testată a confirmat că aplicația rămâne activă fără interfață de consolă.',
            'Integrarea executabilului nu înlocuiește proiectul sursă: livrabilul final păstrează împreună codul, configurația PyInstaller, dependențele și fișierele de distribuție.',
            'Rezultatul este potrivit pentru rularea pe Windows, iar arhiva finală permite instalarea și lansarea fără existența prealabilă a mediului de dezvoltare Python.'
        ):
            self.prose(text)
        self.heading('Anexa', page=True)
        self.prose('Codul claselor introduse sau adaptate pentru integrarea bazei de date și al testelor de verificare este prezentat mai jos. Clasele de animale, generatorul și componentele grafice existente completează structura proiectului.')
        for file_index, filename in enumerate(('Animale.spec', '__main__.py', 'application.py', 'requirements.txt', 'model/database.py', 'tests/test_database.py')):
            self.heading(filename, page=file_index > 0)
            for line in Path(filename).read_text(encoding='utf-8').splitlines():
                paragraph = self.paragraph(112, line or ' ')
                run_properties = paragraph.find('w:r/w:rPr', self.NS)
                if run_properties is not None:
                    for color in run_properties.findall('w:color', self.NS):
                        color.set(f'{{{self.W}}}val', 'CCCCCC')
        self.body.append(self.section)
        self.parts['word/document.xml'] = etree.tostring(self.root, encoding='UTF-8', xml_declaration=True, standalone=True)
        output = Path('LAB 7 PIG.docx')
        with ZipFile(output, 'w', ZIP_DEFLATED) as destination:
            for name, data in self.parts.items():
                destination.writestr(name, data)
        with ZipFile(self.reference) as source, ZipFile(output) as final:
            changed = [name for name in source.namelist() if source.read(name) != final.read(name)]
        assert 'word/document.xml' in changed, changed
        assert 'word/_rels/document.xml.rels' in changed, changed
        assert 'word/media/image4.png' in changed or 'word/media/image4.png' in final.namelist(), changed
        print('Created:', output.resolve())
        print('Changed package parts:', changed)


if __name__ == '__main__':
    ReportBuilder().build()
