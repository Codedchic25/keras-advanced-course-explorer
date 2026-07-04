"""Tools for the Course RAG agent.

We give the agent three precise local tools:

- `read_course_structure` — pulls the hierarchical sessions map (S42-S50).
- `get_session_data` — extracts glossary, code, and exercises for a specific session.
- `search_local_glossary` — scans all text for rapid keyword matching.

Fewer tools = a more predictable agent and faster runs.
"""

from __future__ import annotations
import json
import yaml
from pathlib import Path
from typing import Dict, Any

# Căi relative calculate de la fișierul curent spre folderele de date
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_PATH = BASE_DIR / "data" / "database.json"
SYSTEM_YAML_PATH = Path(__file__).resolve().parent / "prompts" / "system.yaml"


def read_course_structure() -> Dict[str, Any]:
    """Retrieve the hierarchical structure, titles, and icons of modules and sessions (S42-S50)."""
    if not SYSTEM_YAML_PATH.exists():
        return {}
    try:
        with open(SYSTEM_YAML_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}


def get_session_data(session_id: int) -> Dict[str, Any]:
    """Extract the exact glossary terms, code assets, and practical exercises for a specific session ID."""
    if not DATABASE_PATH.exists():
        return {}
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            db_data = json.load(f)
        session_str = str(session_id)
        if session_str in db_data:
            return db_data[session_str]
    except Exception:
        return {}
    return {}


def search_local_glossary(query: str) -> list[Dict[str, Any]]:
    """Scan all available session data to rapidly find terms and definitions matching the query text."""
    results = []
    if not DATABASE_PATH.exists():
        return results
    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            db_data = json.load(f)

        query_lower = query.lower()
        for session_id, content in db_data.items():
            for item in content.get("glosar", []):
                if (
                    query_lower in item.get("termen", "").lower()
                    or query_lower in item.get("definitie", "").lower()
                ):
                    results.append(
                        {
                            "session_id": int(session_id),
                            "termen": item.get("termen"),
                            "definitie": item.get("definitie"),
                        }
                    )
    except Exception:
        return results
    return results


# --- Method Tools Export --------------------------------------------------
# The agent factory will consume this list directly to bind tools to the LLM.
METHOD_TOOLS = [read_course_structure, get_session_data, search_local_glossary]
