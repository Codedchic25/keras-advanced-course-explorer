## Modul: Course RAG Expert Method

### ⚙️ Specificații Tehnice (Architecture Metadata)
- **Slug**: `course_rag`
- **Type**: `text_modular_engine`
- **Complexity**: `medium`
- **Navigation Components**: `streamlit nativ (st.selectbox / st.checkbox)`
- **Notion task**: N/A — Structură locală de producție (Enterprise Architecture Blueprint)

---

### 🌐 Internationalization & State Management Mapping
- **State Store**: `st.session_state.lang` (Implicit: `"ro"`)
- **Data Hydration Source**: `data/database.json` & `data/locales.json`
- **UI Boundary**: Extensie lățime sidebar forțată CSS (`380px` - `460px`) pentru evitarea fragmentării textului (No-Truncation Policy).
