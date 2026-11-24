# Gestionarea animalelor — bază de date

## Pornire (PowerShell)

```powershell
python -m pip install -r requirements.txt
python .
```

Proiectul folosește **SQLite**, alternativa permisă în enunț. Motivul alegerii:
aplicația este desktop, locală, iar SQLite este inclus în Python și nu necesită
instalarea/configurarea unui server PostgreSQL. Driverul utilizat este `sqlite3`;
`psycopg` este destinat PostgreSQL și nu se folosește pentru SQLite.

La prima pornire se creează `data/animale.sqlite3` și se inserează cele 30 de animale
din laboratorul anterior. Inițializarea este tranzacțională și se marchează separat,
astfel încât animalele șterse (inclusiv toate) nu reapar la repornire.
Datele se păstrează între rulări. Calea bazei este relativă la proiect, nu la
directorul din care se lansează aplicația. Fișierul nu se include în Git.

## Clase și responsabilități

- `model/database.py` — `Database`: conexiuni, tranzacții, commit/rollback și închidere.
- `model/animal_repository.py` — `AnimalRepository`: schemă, inițializare, INSERT,
  SELECT, UPDATE, DELETE, ORDER BY, COUNT/AVG cu GROUP BY și validare.
- `presenter/presenter.py` — `Presenter`: coordonează interfața și repository-ul.
- `application.py` — `Application`: pornirea aplicației și raportarea erorilor de inițializare.

Tabelul `animale` stochează ID-ul persistent, tipul clasei, numele, vârsta,
greutatea, categoria și detaliile specifice în JSON. Tipul clasei este reconstituit
la citire pentru a păstra imaginile și comportamentul animalelor existente.
Valorile sunt transmise ca parametri SQL; coloanele de sortare și agregare sunt
selectate din liste fixe. Vârsta și greutatea trebuie să fie finite și nenegative;
este acceptată și virgula zecimală.

Lista din presenter nu mai este sursa datelor. Colecțiile returnate de SELECT sunt
rezultate temporare pentru afișare. Adăugarea, editarea, ștergerea individuală sau
multiplă, sortarea și statisticile graficelor se execută în baza de date.
Generatorul existent servește doar la popularea inițială și identificarea claselor.
Logica nouă este exclusiv în clase; `__main__.py` doar apelează metoda de pornire.

## Verificare

```powershell
python -B -m unittest discover -s tests -v
```

Testele folosesc baze temporare și nu modifică datele aplicației.
