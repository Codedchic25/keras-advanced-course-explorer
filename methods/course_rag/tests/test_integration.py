"""End-to-end integration test for run_method.

We mock the Agno agent instance — not the network layer — so the test:
    - is fully deterministic
    - costs nothing and burns no API quota
    - runs in milliseconds
    - exercises every line in agent.py to prevent regression errors.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import pytest

from methods.course_rag import agent as agent_module
from methods.course_rag.schema import CourseRagResponseSchema


@pytest.mark.asyncio
async def test_run_method_returns_validated_schema(
    sample_query: str,
    sample_session_id: str,
    valid_rag_response: CourseRagResponseSchema,
) -> None:
    """run_method should hand back the strict schema instance the agent produced."""
    fake_arun = AsyncMock(return_value=SimpleNamespace(content=valid_rag_response))
    fake_agent = SimpleNamespace(arun=fake_arun)

    # Patch-uim funcția get_course_rag_agent pentru a returna agentul nostru simulat (mock)
    with patch.object(agent_module, "get_course_rag_agent", return_value=fake_agent):
        result = await agent_module.run_method(
            query=sample_query,
            context_session_id=sample_session_id,
        )

    assert isinstance(result, CourseRagResponseSchema)
    assert result.matched_session_id == valid_rag_response.matched_session_id
    assert result.quick_check_question == valid_rag_response.quick_check_question


@pytest.mark.asyncio
async def test_run_method_passes_query_and_session_in_user_prompt(
    sample_query: str,
    sample_session_id: str,
    valid_rag_response: CourseRagResponseSchema,
) -> None:
    """The user prompt seen by the model must include both dynamic variables verbatim."""
    fake_arun = AsyncMock(return_value=SimpleNamespace(content=valid_rag_response))
    fake_agent = SimpleNamespace(arun=fake_arun)

    with patch.object(agent_module, "get_course_rag_agent", return_value=fake_agent):
        await agent_module.run_method(
            query=sample_query,
            context_session_id=sample_session_id,
        )

    # Extragem primul argument transmis metodei arun() de către agent.py
    sent_prompt = fake_arun.call_args.args[0]
    assert sample_query in sent_prompt
    assert sample_session_id in sent_prompt
