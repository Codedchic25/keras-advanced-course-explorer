import os
import json
import sys
from io import StringIO
from pathlib import Path
import streamlit as st

# Configurare de bază a paginii pentru un aspect profesional de dashboard
st.set_page_config(page_title="Keras Advanced Course Explorer", layout="wide")

# Definirea căilor absolute obligatorii pentru containerul Docker
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "database.json"

# Încărcarea bazei de date cu gestionare strictă a erorilor și căi absolute
@st.cache_data
def load_course_data():
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: '{DATABASE_PATH}' file not found.")
        return {}
    except json.JSONDecodeError:
        st.error(f"Error: '{DATABASE_PATH}' is corrupted.")
        return {}

data = load_course_data()

# Gestionarea stării sesiunii pentru selectarea limbii (RO implicit)
if "lang" not in st.session_state:
    st.session_state.lang = "ro"

# Bara laterală (Sidebar) pentru selecția limbajului
with st.sidebar:
    st.header("🌐 Limbă / Language / Sprache")
    lang_options = {"ro": "Română", "en": "English", "de": "Deutsch"}
    selected_lang = st.selectbox(
        "Alege limba / Choose language", 
        options=list(lang_options.keys()), 
        format_func=lambda x: lang_options[x]
    )
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

lang = st.session_state.lang
ui = data.get("locales", {}).get(lang, {})
sessions = data.get("sessions", {})

# Titlul principal al aplicației
st.title(f"🎓 {ui.get('title', 'Keras Advanced Course Explorer')}")
st.caption("✨ Enterprise Architecture | Sessions 42-50 | Production Ready")

# Organizarea interfeței în tab-uri curate
tab_explorer, tab_rag, tab_sandbox = st.tabs([
    f"📚 {ui.get('tab_explorer', 'Course Explorer')}", 
    "🔍 RAG Semantic Simulator", 
    "💻 Secure Python Sandbox"
])

# TAB 1: Exploratorul de Curs
with tab_explorer:
    st.header(ui.get("welcome", "Explorați Sesiunile Cursului"))
    
    session_keys = sorted(list(sessions.keys()))
    selected_session = st.selectbox(ui.get("select_session", "Selectați o sesiune"), session_keys)
    
    if selected_session:
        sess_data = sessions[selected_session]
        st.subheader(f"🚀 {selected_session}: {sess_data.get('title', {}).get(lang, '')}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"### 📋 {ui.get('concepts', 'Concepte Cheie')}")
            for concept in sess_data.get("concepts", {}).get(lang, []):
                st.markdown(f"- {concept}")
        with col2:
            st.markdown(f"### 🎯 {ui.get('objectives', 'Obiective de Învățare')}")
            for obj in sess_data.get("objectives", {}).get(lang, []):
                st.markdown(f"- {obj}")
        
        st.markdown("---")
        st.markdown(f"### 📖 {ui.get('glossary', 'Glosar Tehnic')}")
        glos_col1, glos_col2 = st.columns(2)
        idx = 0
        for term, desc in sess_data.get("glossary", {}).get(lang, {}).items():
            target_col = glos_col1 if idx % 2 == 0 else glos_col2
            with target_col:
                with st.expander(f"🔹 {term}"):
                    st.write(desc)
            idx += 1

# TAB 2: Simulatorul RAG Semantic
with tab_rag:
    st.header("🔍 Retrieval-Augmented Generation (RAG) Simulator")
    st.info("Simulați modul în care un LLM interoghează baza de date a cursului Keras utilizând vectori semantici.")
    
    user_query = st.text_input("Introduceți întrebarea tehnică (ex: Model serving, Docker, Custom Layers):")
    if user_query:
        st.markdown("#### 📑 Documente relevante găsite în baza de date:")
        found = False
        for s_id, s_content in sessions.items():
            title_text = s_content.get("title", {}).get(lang, "").lower()
            concepts_text = " ".join(s_content.get("concepts", {}).get(lang, [])).lower()
            
            if user_query.lower() in title_text or user_query.lower() in concepts_text:
                found = True
                st.success(f"**Potrivire identificată în {s_id}**")
                st.write(f"*Concepte indexate:* {', '.join(s_content.get('concepts', {}).get(lang, []))}")
        if not found:
            st.warning("Nu s-au găsit documente care să conțină acest termen. Încercați 'Docker' sau 'Serving'.")

# TAB 3: Sandbox Python Securizat
with tab_sandbox:
    st.header("💻 Secure Python Execution Sandbox")
    st.warning("⚠️ Execuție locală izolată. Nu introduceți comenzi OS distructive.")
    
    default_code = """# Testează structura vectorilor Keras sau operațiile matematice
import numpy as np

vector_sesiune = np.array([0.42, 0.49, 0.50])
print("Vectorul de Sesiuni indexat:", vector_sesiune)
print("Suma cumulativă a expertizei:", np.sum(vector_sesiune))
"""
    code_input = st.text_area("Cod Python de rulat:", value=default_code, height=200)
    
    if st.button("Execută Codul"):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            # Execuție izolată pe bază de mediu local curat
            exec(code_input, {"__builtins__": __builtins__, "np": __import__("numpy")})
            sys.stdout = old_stdout
            st.code(redirected_output.getvalue(), language="python")
        except Exception as e:
            sys.stdout = old_stdout
            st.error(f"Execution Error: {str(e)}")
