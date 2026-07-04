import os

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import json
import sys
from io import StringIO
from pathlib import Path

import streamlit as st

# 1. Configurare Pagină
st.set_page_config(
    page_title="Multi-Lang Course Explorer", page_icon="🎓", layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "database.json"
PROGRES_PATH = BASE_DIR / "data" / "progres.json"
LOCALES_PATH = BASE_DIR / "data" / "locales.json"

# Numele sesiunilor traduse automat la runtime prin ID-uri stabile
COURSES = {
    42: {
        "RO": "Introducere în Keras: Primii Pași",
        "EN": "Introduction to Keras: First Steps",
        "DE": "Einführung in Keras: Erste Schritte",
    },
    43: {
        "RO": "Keras Avansat: Personalizare și Reglare",
        "EN": "Advanced Keras: Customization & Tuning",
        "DE": "Fortgeschrittenes Keras: Anpassung & Tuning",
    },
    44: {
        "RO": "Clasificare de Imagini cu CNN",
        "EN": "Image Classification with CNNs",
        "DE": "Bildklassifizierung mit CNNs",
    },
    45: {
        "RO": "Transfer Learning: Modele Pre-antrenate",
        "EN": "Transfer Learning: Pre-trained Models",
        "DE": "Transfer Learning: Vorab trainierte Modelle",
    },
    46: {
        "RO": "Data Augmentation și Callbacks",
        "EN": "Data Augmentation & Callbacks",
        "DE": "Datenaugmentation & Callbacks",
    },
    47: {
        "RO": "Keras Ultra-Avansat: Fine-Tuning",
        "EN": "Ultra-Advanced Keras: Fine-Tuning",
        "DE": "Ultra-Fortgeschrittenes Keras: Fine-Tuning",
    },
    48: {
        "RO": "Servire Modele: Pregătire Producție",
        "EN": "Model Serving: Production Readiness",
        "DE": "Modellbereitstellung: Produktionsreife",
    },
    49: {
        "RO": "Deploy AI: Publicare pe Cloud",
        "EN": "AI Deploy: Cloud Publishing",
        "DE": "KI-Bereitstellung: Cloud-Veröffentlichung",
    },
    50: {
        "RO": "Scaling Deep Learning Apps",
        "EN": "Scaling Deep Learning Apps",
        "DE": "Skalierung von Deep-Learning-Apps",
    },
}


def load_progres():
    if PROGRES_PATH.exists():
        try:
            with open(PROGRES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_progres(p):
    with open(PROGRES_PATH, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2, ensure_ascii=False)


progres = load_progres()

# --- SIDEBAR GLOBALIZAT (Meniu superior) ------------------------------------
with st.sidebar:
    st.title("🎓 Course Explorer")

    # 🪄 Selectorul "Magic" de Limbă pentru Recruiteri
    lang = st.selectbox(
        "🌐 Language / Limbă / Sprache:", options=["RO", "EN", "DE"], index=0
    )

    # Încărcăm dicționarul curent din locales.json
    locales = (
        json.load(open(LOCALES_PATH, "r", encoding="utf-8"))
        if LOCALES_PATH.exists()
        else {}
    )
    t = locales.get(lang, locales.get("RO"))  # Fallback sigur pe Română

    st.caption(t["subtitle"])
    st.markdown("---")

    # 1. Meniul de selecție dropdown sincronizat cu limba aleasă
    st.markdown(f"**{t['select_label']}**")
    options = [
        f"S{sid}: {title_map[lang]} {'✅' if progres.get(str(sid)) else '⏳'}"
        for sid, title_map in COURSES.items()
    ]
    selected = st.selectbox("Alege:", options=options, label_visibility="collapsed")
    current_id = int(selected.split(":")[0].replace("S", ""))
    st.markdown("---")

    # 2. Graficul de progres cu etichete dinamice traduse live
    st.markdown(f"**{t['progress_title']}**")
    done = sum(1 for v in progres.values() if v is True)
    chart_data = {"Stare": [t["finished"], t["remaining"]], "Sesiuni": [done, 9 - done]}
    st.bar_chart(data=chart_data, x="Stare", y="Sesiuni")
    st.caption(t["status"].format(done, int((done / 9) * 100)))

# --- ZONA PRINCIPALĂ INTERNAȚIONALIZATĂ -------------------------------------
st.header(t["details_header"].format(current_id, COURSES[current_id][lang]))

chk = st.checkbox(t["checkbox_label"], value=progres.get(str(current_id), False))
if chk != progres.get(str(current_id), False):
    progres[str(current_id)] = chk
    save_progres(progres)
    st.rerun()

db = {}
if DATABASE_PATH.exists():
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
    except Exception:
        db = {}

content = db.get(str(current_id))

if content:
    t1, t2, t3, t4 = st.tabs(
        [t["tab_glossary"], t["tab_code"], t["tab_exercises"], t["tab_sandbox"]]
    )

    with t1:
        for item in content.get("glosar", []):
            st.markdown(f"**🔹 {item['termen']}**")
            st.write(item["definitie"])
            st.write("---")

    with t2:
        st.code(content.get("assets", ""), language="python")

    with t3:
        for i, ex in enumerate(content.get("exercitii", []), 1):
            st.write(f"{i}. {ex}")

    with t4:
        st.markdown(t["sandbox_header"])
        st.caption(t["sandbox_caption"])
        code = st.text_area(
            "Editor:",
            value=content.get("assets", ""),
            height=200,
            key=f"sb_{current_id}",
        )

        if st.button(t["run_btn"]):
            old, red = sys.stdout, StringIO()
            sys.stdout = red
            try:
                scope = {}
                exec(code, {}, scope)
                sys.stdout = old
                out = red.getvalue()
                st.success(t["success_msg"])
                if out:
                    st.code(out, language="text")
                if "history" in scope and isinstance(scope["history"], dict):
                    st.markdown("#### 📈 Grafic")
                    st.line_chart(scope["history"])
            except Exception as e:
                sys.stdout = old
                st.error(t["exec_err"].format(e))
else:
    st.info(t["missing_content"].format(current_id))

# --- SIMULATOR RAG CU COMTUARE DE LIMBĂ -------------------------------------
st.markdown("---")
st.subheader(t["rag_header"])
st.caption(t["rag_caption"])
q = st.text_input(t["rag_input"])

if q and db:
    found = next(
        (
            item
            for s in db.values()
            for item in s.get("glosar", [])
            if q.lower() in item["termen"].lower()
        ),
        None,
    )
    if found:
        st.success(t["rag_success"])
        st.json(
            {
                "answer": f"[{lang} Translated Context]: {found['definitie']}",
                "related_glossary_terms": [
                    {"term": found["termen"], "definition": found["definitie"]}
                ],
                "quick_check_question": f"How do you plan to leverage {found['termen']} in your scalable pipeline?",
            }
        )
    else:
        st.warning(t["rag_missing"])
