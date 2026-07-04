"""Agno agent factory and run helper for the Course RAG method.

This script loads the static system prompt, binds the strict Pydantic output schema,
attaches local repository tools, and executes the RAG pipeline asynchronously.
"""

from __future__ import annotations

import asyncio
import argparse
from pathlib import Path
import yaml

# Importăm direct din biblioteca agno nativă pentru inițializarea agentului
from agno.agent import Agent
from agno.models.openai import (
    OpenAIChat,
)  # Presupunem utilizarea unui model OpenAI standard sau similar

from methods.course_rag.schema import CourseRagResponseSchema
from methods.course_rag.tools import METHOD_TOOLS

_PROMPT_PATH = Path(__file__).parent / "prompts" / "system.yaml"


def _load_system_prompt() -> str:
    """Read the static system prompt from prompts/system.yaml."""
    with _PROMPT_PATH.open("r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)
    return loaded["system"]


def get_course_rag_agent() -> Agent:
    """Build the Agno agent for the Course RAG method.

    Returns:
        An `agno.agent.Agent` configured with our strict schema and local tools.
    """
    # Folosim direct clasa nativă Agent din Agno conform regulilor stabilite de schemă
    return Agent(
        name="course_rag_expert",
        model=OpenAIChat(
            id="gpt-4o-mini"
        ),  # Model rapid și predictibil pentru producție și evals
        instructions=_load_system_prompt(),
        tools=METHOD_TOOLS,
        output_schema=CourseRagResponseSchema,
        show_tool_calls=False,
        markdown=False,
    )


async def run_method(
    query: str,
    context_session_id: str = "all",
) -> CourseRagResponseSchema:
    """Query the local course database using the Course RAG agent.

    Args:
        query: The user's technical question or search term (e.g., "What is Dropout?").
        context_session_id: A specific session ID string (42-50) to isolate, or "all".

    Returns:
        A validated `CourseRagResponseSchema` instance.
    """
    agent = get_course_rag_agent()

    # Valorile dinamice sunt interpolate în mesajul USER pentru a menține cache-ul sistemului intact
    user_prompt = (
        f"User Query: {query}\n"
        f"Context Session Isolation: {context_session_id}\n\n"
        f"Extract facts from the database and produce one CourseRagResponse matching the schema."
    )

    # Executăm apelul asincron prin motorul Agno
    response = await agent.arun(user_prompt)

    # Agno parsează automat JSON-ul nativ și returnează direct instanța validată de Pydantic
    return response.content


def _cli() -> None:  # pragma: no cover - manual smoke test
    """CLI entry point for quick manual smoke tests."""
    parser = argparse.ArgumentParser(description="Query the Course RAG system.")
    parser.add_argument(
        "--query", required=True, help="The question or concept to search for."
    )
    parser.add_argument(
        "--session",
        default="all",
        help="Target session scope (42-50 or 'all', default: all).",
    )
    args = parser.parse_args()

    result = asyncio.run(run_method(query=args.query, context_session_id=args.session))
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    _cli()
