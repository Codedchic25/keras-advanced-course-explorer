# Application Architecture & Data Flow Diagram

Acest document descrie modul în care datele circulă prin ecosistemul modular al aplicației, evidențiind interacțiunea dintre interfața grafică, modulele de testare și contractul rigid de date.

## 📊 1. Fluxul Căutării Semantice (Simulator RAG)

1. **Input**: Utilizatorul introduce o întrebare tehnică sau un concept în bara de căutare din interfață (`app.py`).
2. **Interogare**: Cererea apelează funcția de scanare locală aflată în modulul izolat `methods/course_rag/tools.py`.
3. **Extragere**: Instrumentul citește direct din baza de date centrală locală `data/database.json`.
4. **Validare Contractuală**: Datele brute extrase sunt mapate și verificate prin schema rigidă Pydantic din `methods/course_rag/schema.py`.
5. **Afișare**: Răspunsul validat este trimis înapoi în `app.py` și randat securizat sub formă de structură JSON nativă pe ecran.

## 💻 2. Fluxul de Execuție în Sandbox (⚡ Python Sandbox)

1. **Preluare Cod**: Utilizatorul introduce sau editează un fragment de cod Keras în caseta dedicată din Tab-ul 4.
2. **Izolare Context**: La apăsarea butonului, codul este transmis funcției native `exec()` rulată pe un scope local izolat (`local_scope = {}`).
3. **Interceptare I/O**: `sys.stdout` este redirecționat temporar către un obiect `StringIO()` pentru a captura toate mesajele `print()` și erorile de execuție, injectându-le estetic înapoi în browser.
4. **Detecție Grafice**: După execuție, un analizor structural scanează variabilele din `local_scope`. Dacă identifică un obiect numit `history` (dicționar sau clasă Keras History), extrage automat metricile de performanță (`loss`, `accuracy`) și randează un grafic linie (`st.line_chart`) în timp real.

## 💾 3. Managementul Persistenței Progresului

* **Input**: User-ul bifează starea unei sesiuni în zona centrală a ecranului.
* **I/O**: Starea este mapată ca o valoare booleană (`True/False`) legată de ID-ul unic al sesiunii și salvată asincron pe disc în format JSON în `data/progres.json`.
* **State Hydration**: La repornirea aplicației, graficul de bare și indicatorii de stare text (`✅` sau `⏳`) din interiorul meniului dropdown sunt reconstruite direct prin citirea stării stocate în `data/progres.json`, garantând vizibilitate maximă și zero pierderi de date.
## 💾 4. Managementul Internaționalizării (i18n System)
* **Input**: Utilizatorul modifică selectorul de limbă (`RO`, `EN`, `DE`) din Sidebar.
* **I/O**: Aplicația încarcă dicționarul de mapare corespunzător din fișierul static securizat `data/locales.json`.
* **State Hydration**: La fiecare refresh (`st.rerun()`), toate tab-urile, titlurile, butoanele, mesajele de succes și indicatorii grafici sunt traduse instantaneu în memorie înainte de randarea pe ecran, garantând performanță maximă (zero latență).
