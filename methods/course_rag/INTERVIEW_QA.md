# 🎓 Technical Interview Q&A — Project Architecture

Acest ghid cuprinde întrebările critice de arhitectură software pe care un Senior Developer sau Technical Lead le poate adresa pe marginea acestui codebase în timpul unui interviu tehnic.

---

### Q1: De ce ai ales un design pattern bazat pe Metode (Method-Driven Agent Design) în loc să scrii o aplicație Streamlit monolithic clasică?
**Răspuns:**
Într-o aplicație monolitică, logica agenților AI, prompturile de sistem și uneltele sunt amestecate direct în fișierele de interfață, făcând aplicația imposibil de testat automat sau de scalat în producție. Prin izolarea motorului RAG în subfolderul dedicat `methods/course_rag/`, am obținut un sistem atomic:
1. **Separarea Responsabilităților (SoC):** Interfața (`app.py`) nu știe cum funcționează AI-ul, ea doar consumă funcția expusă `run_method`.
2. **Testabilitate 100% Offline:** Putem rula aserțiuni și simulări riguroase direct pe fabrică și pe schemă fără să încărcăm interfața grafică.

---

### Q2: Ce este un „Contract Rigid de Date” și cum protejează aplicația împotriva halucinațiilor specifice LLM-urilor?
**Răspuns:**
În `schema.py`, am configurat modelul Pydantic folosind `ConfigDict(extra="forbid", strict=True)`. Acest lucru înseamnă că:
* `extra="forbid"`: LLM-ul este penalizat instantaneu dacă încearcă să adauge câmpuri parazite sau nesolicitate în obiectul returnat.
* `strict=True`: Se dezactivează conversia automată a tipurilor de date, blocând orice inconsecvență.
* Validatoarele customizate (`@field_validator`) impun constrângeri cantitative dure (lungimi minime, terminarea obligatorie a întrebărilor cu `?`), interceptând orice răspuns parțial sau incorect direct la nivel de backend.

---

### Q3: Cum ai rezolvat problema costurilor și a predictibilității în timpul rulării suitei de teste unitare?
**Răspuns:**
Toate testele din folderul `tests/` folosesc obiecte simulate de tip `AsyncMock` și `SimpleNamespace` din biblioteca nativă `unittest.mock`. În loc să apelăm API-ul OpenAI real (ceea ce ar fi costisitor și dependent de conexiunea la internet), noi simulăm exclusiv comportamentul motorului de execuție asincron `.arun()`. Testele se execută local în câteva milisecunde, sunt complet deterministe și nu consumă credit din API quota.

---

### Q4: Cum funcționează protecția împotriva atacurilor de tip Prompt Injection în acest proiect?
**Răspuns:**
Sistemul folosește o barieră dublă de securitate:
1. **Izolarea Promptului de Sistem**: Promptul din `prompts/system.yaml` este complet static. Schimbările și intrările dinamice ale utilizatorului sunt injectate exclusiv în mesajul utilizatorului (`user_prompt`), împiedicând rescrierea instrucțiunilor de bază.
2. **Blocul de Securitate Brut (Security Guardrail)**: Poziționat strategic la finalul promptului de sistem, acesta instruiește în mod explicit modelul să trateze toate datele extrase din unelte ca date nesigure (`untrusted DATA`), anulând orice instrucțiune malițioasă ascunsă în fișierele de curs.

---

### Q5: În arhitectura finală UI, de ce ai preferat componentele native Streamlit în locul unei biblioteci externe complexe (precum streamlit-antd-components)?
**Răspuns:**
Componentele externe care aduc dependențe secundare grele (precum `fastapi` sau servere `uvicorn` asunse în fundal) pot deturna sau bloca verificările de tip „heartbeat” ale platformelor cloud precum Hugging Face Spaces pe portul `7860`. De asemenea, randările JavaScript customizate pot suferi de probleme de contrast sau de fragmentare a textului. Prin alegerea componentelor native (`st.selectbox`, `st.checkbox`) susținute de un control CSS fin injectat manual:
1. **Predictibilitate la Runtime:** Execuția este curată, nativă și elimină conflictele de porturi din containerul Docker.
2. **No-Truncation Policy:** Lățimea barei laterale a fost extinsă programatic la `380px-460px`, garantând că titlurile lungi enterprise nu sunt tăiate cu puncte-puncte, indiferent de rezoluție.

---

### Q6: Cum ai implementat sistemul de internaționalizare (i18n) și de ce este important acest detaliu arhitectural într-o aplicație de producție?
**Răspuns:**
Pentru a asigura suportul pentru limbi multiple (RO/EN/DE), am decuplat complet etichetele de text și instrucțiunile statice din codul sursă, externalizându-le într-un fișier centralizat numit `data/locales.json`.
1. **Arhitectură Curată (i18n Best Practices)**: `app.py` nu mai conține string-uri hardcodate; el doar injectează dinamic un dicționar de traduceri (`t`) bazat pe starea selectorului web la runtime.
2. **Mentenabilitate și Scalabilitate**: Adăugarea unei limbi noi (ex: Franceză) nu necesită modificarea niciunei linii de cod în orchestratorul Streamlit; se adaugă doar un nou nod de traduceri în fișierul JSON, reducând riscul apariției erorilor de sintaxă în producție.
