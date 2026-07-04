"""Promptfoo Python provider for the Course RAG method.

Routes each evaluation fixture row directly through our asynchronous run_method.
This ensures promptfoo evaluates the actual agent, including its attached local
tools, static configuration prompts, and strict Pydantic enforcement.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

# Importăm run_method specific din modulul nostru course_rag
from methods.course_rag.agent import run_method


def call_api(
    prompt: str, options: dict[str, Any], context: dict[str, Any]
) -> dict[str, Any]:
    """Promptfoo Python provider entry point.

    Args:
        prompt: One JSON-encoded fixture line from evals/fixtures/inputs.json.
        options: Promptfoo's provider options block (unused).
        context: Promptfoo's per-test context (unused).

    Returns:
        Dict with `output` (a JSON string of the validated schema instance),
        or `error` if the agent run or validation failed.
    """
    _ = options, context

    try:
        payload = json.loads(prompt)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON fixture line: {e}"}

    try:
        # Executăm asincron metoda cu parametrii despachetați din inputs.json (query, session)
        result = asyncio.run(run_method(**payload))
    except Exception as e:
        return {"error": f"Agent run failed: {e!r}"}

    # result este o instanță de CourseRagResponseSchema - o serializăm curat în JSON string
    return {"output": result.model_dump_json()}
