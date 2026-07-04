import os
import json
import sys
from io import StringIO
from pathlib import Path
import streamlit as st

# 1. Configurare Pagină
st.set_page_config(page_title="Multi-Lang Course Explorer", page_icon="🎓", layout="wide")

# 2. Injectare CSS pentru lățime Sidebar robustă (Previne tăierea textului)
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            min-width: 380px !important;
            max-width: 460px !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "database.json"
PROGRES_PATH = BASE_DIR / "data" / "progres.json"
LOCALES_PATH = BASE_DIR / "data" / "locales.json"

COURSES = {
    42: {"RO": "Introducere în Keras: Primii Pași", "EN": "Introduction to Keras: First Steps", "DE": "Einführung in Keras: Erste Schritte"},
    43: {"RO": "Keras Avansat: Personalizare și Reglare", "EN": "Advanced Keras: Customization & Tuning", "DE": "Fortgeschrittenes Keras: Anpassung & Tuning"},
    44: {"RO": "Clasificare de Imagini cu CNN", "EN": "Image Classification with CNNs", "DE": "Bildklassifizierung mit CNNs"},
    45: {"RO": "Transfer Learning: Modele Pre-antrenate", "EN": "Transfer Learning: Pre-trained Models", "DE": "Transfer Learning: Vorab trainierte Modelle"},
    46: {"RO": "Data Augmentation și Callbacks", "EN": "Data Augmentation & Callbacks", "DE": "Datenaugmentation & Callbacks"},
    47: {"RO": "Keras Ultra-Avansat: Fine-Tuning", "EN": "Ultra-Advanced Keras: Fine-Tuning", "DE": "Ultra-Fortgeschrittenes Keras: Fine-Tuning"},
    48: {"RO": "Servire Modele: Pregătire Producție", "EN": "Model Serving: Production Readiness", "DE": "Modellbereitstellung: Produktionsreife"},
    49: {"RO": "Deploy AI: Publicare pe Cloud", "EN": "AI Deploy: Cloud Publishing", "DE": "KI-Bereitstellung: Cloud-Veröffentlichung"},
    50: {"RO": "Scaling Deep Learning Apps", "EN": "Scaling Deep Learning Apps", "DE": "Skalierung von Deep-Learning-Apps"}
}

def load_progres():
    if PROGRES_PATH.exists():
        try:
            with open(PROGRES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception: return {}
    return {}

def save_progres(p):
    try:
        PROGRES_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRES_PATH, "w", encoding="utf-8") as f:
            json.dump(p, f, indent=2, ensure_ascii=False)
    except Exception: pass

progres = load_progres()

with st.sidebar:
    st.title("🎓 Course Explorer")
    lang = st.selectbox("🌐 Language / Limbă / Sprache:", options=["RO", "EN", "DE"], index=0)

    locales = json.load(open(LOCALES_PATH, "r", encoding="utf-8")) if LOCALES_PATH.exists() else {}
    t = locales.get(lang, locales.get("RO", {}))

    st.caption(t.get("subtitle", ""))
    st.markdown("---")

    st.markdown(f"**{t.get('select_label', 'Selectează:')}**")
    options = [f"S{sid}: {title_map[lang]} {'✅' if progres.get(str(sid)) else '⏳'}" for sid, title_map in COURSES.items()]
    selected = st.selectbox("Alege:", options=options, label_visibility="collapsed")
    
    # EXTRASE ID MINUȚIOS: Extrage curat string-ul înainte de două puncte și elimină caracterul 'S'
    part_before_colon = selected.split(":")[0]
    current_id = int(part_before_colon.replace("S", ""))
    st.markdown("---")

    st.markdown(f"**{t.get('progress_title', 'Progres')}**")
    done = sum(1 for v in progres.values() if v is True)
    chart_data = {"Stare": [t.get("finished", "Gata"), t.get("remaining", "Rămas")], "Sesiuni": [done, 9 - done]}
    st.bar_chart(data=chart_data, x="Stare", y="Sesiuni")

st.header(t.get("details_header", "Sesiunea {}").format(current_id, COURSES[current_id][lang]))

chk = st.checkbox(t.get("checkbox_label", "Completat"), value=progres.get(str(current_id), False))
if chk != progres.get(str(current_id), False):
    progres[str(current_id)] = chk
    save_progres(progres)
    st.rerun()

db = json.load(open(DATABASE_PATH, "r", encoding="utf-8")) if DATABASE_PATH.exists() else {}
content = db.get(str(current_id))

if content:
    t1, t2, t3, t4 = st.tabs([t.get("tab_glossary", "Glosar"), t.get("tab_code", "Cod"), t.get("tab_exercises", "Exerciții"), t.get("tab_sandbox", "Sandbox")])

    with t1:
        for item in content.get("glosar", []):
            termen_dict = item.get("termen", {})
            definitie_dict = item.get("definitie", {})
            
            termen_lang = termen_dict.get(lang, termen_dict.get("RO", ""))
            definitie_lang = definitie_dict.get(lang, definitie_dict.get("RO", ""))
            
            st.markdown(f"**🔹 {termen_lang}**")
            st.write(definitie_lang)
            st.write("---")
            
    with t2: st.code(content.get("assets", ""), language="python")
    
    with t3:
        exercitii_raw = content.get("exercitii", {})
        # Identificare minuțioasă a tipului de date pentru structura multilingvă din database.json
        if isinstance(exercitii_raw, dict):
            exercitii_lang = exercitii_raw.get(lang, exercitii_raw.get("RO", []))
        elif isinstance(exercitii_raw, list):
            exercitii_lang = exercitii_raw
        else:
            exercitii_lang = []
            
        for i, ex in enumerate(exercitii_lang, 1): 
            st.write(f"{i}. {ex}")
            
    with t4:
        st.markdown(t.get("sandbox_header", ""))
        code = st.text_area("Editor:", value=content.get("assets", ""), height=200, key=f"sb_{current_id}")
        if st.button(t.get("run_btn", "Execută")):
            old, red = sys.stdout, StringIO()
            sys.stdout = red
            try:
                scope = {}
                exec(code, {}, scope)
                sys.stdout = old
                st.code(red.getvalue(), language="text")
            except Exception as e:
                sys.stdout = old
                st.error(t.get("exec_err", "Eroare: {}").format(e))
else:
    st.info(t.get("missing_content", "Lipsă conținut").format(current_id))
