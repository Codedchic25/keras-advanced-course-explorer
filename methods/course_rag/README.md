---
title: Keras Advanced Course Explorer
emoji: 🎓
colorFrom: red
colorTo: red
sdk: docker
app_port: 7860
tags:
  - streamlit
pinned: false
short_description: Multi-language Keras Explorer
license: mit
---

# 🎓 Keras Advanced Course Explorer

Enterprise Architecture | Sessions 42-50 | Production Ready

Aplicație web interactivă dezvoltată în Streamlit și izolată industrial în container Docker, concepută pentru explorarea multilingvă (RO/EN/DE) a conceptelor avansate de Keras, model serving și scalare cloud.

---

# 🔍 Course RAG Expert Method

Aceastămetodă implementează un sistem de interogare semantică (RAG) ghidat de un Agent AI pentru parcurgerea și verificarea cunoștințelor din cursul avansat de Python, Keras și Cloud Deployment (Sesiunile 42-50).

## 📋 Ce generează metoda
Un răspuns structurat și validat riguros, extras direct din contextul local al cursului:

```json
{
  "answer": "O explicație tehnică detaliată...",
  "matched_session_id": 44,
  "related_glossary_terms": [
    {
      "term": "Conv2D",
      "definition": "Strat convolutional..."
    }
  ],
  "quick_check_question": "Întrebare deschisă pentru student?"
}
```

## 💻 Rularea Interfeței Grafice (UI Dashboard Local)
Pentru a parcurge sesiunile interactiv, a gestiona progresul persistent și a rula cod live în Sandbox-ul integrat, executați local:
```bash
uv run streamlit run app.py
```

## ⚡ Rularea manuală prin CLI (Smoke Test Backend)
Asigură-te că cheia `OPENAI_API_KEY` este configurată în mediul tău virtual, apoi rulează din rădăcina proiectului:
```bash
uv run python -m methods.course_rag.agent --query "What is Dropout?" --session 43
```

## 🎯 Rularea testelor unitare (Offline)
Pentru a executa suita completă de 12 teste unitare asincrone fără apeluri către API-ul extern:
```bash
uv run pytest -v
```

## 📈 Rularea evaluărilor de prompturi (Evals)
Pentru rularea testelor de consistență a prompturilor utilizând Promptfoo:
```bash
cd methods/course_rag
npx promptfoo@latest eval
```
