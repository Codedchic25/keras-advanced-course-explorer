"""Factory tests — verify how get_course_rag_agent instantiates the Agno Agent.

We do not construct a real live network agent here. We patch the Agno Agent class
and inspect the kwargs it received. That keeps these tests offline and dependency-free.
"""

from __future__ import annotations

from unittest.mock import patch
from methods.course_rag import agent as agent_module
from methods.course_rag.schema import CourseRagResponseSchema


def test_factory_passes_correct_output_schema() -> None:
    """The factory must wire CourseRagResponseSchema into output_schema."""
    with patch("methods.course_rag.agent.Agent") as mock_agent_cls:
        agent_module.get_course_rag_agent()
        kwargs = mock_agent_cls.call_args.kwargs
        assert kwargs["output_schema"] is CourseRagResponseSchema


def test_factory_uses_stable_name() -> None:
    """The agent name is what observability and logs key on — must be stable."""
    with patch("methods.course_rag.agent.Agent") as mock_agent_cls:
        agent_module.get_course_rag_agent()
        kwargs = mock_agent_cls.call_args.kwargs
        assert kwargs["name"] == "course_rag_expert"


def test_factory_attaches_all_local_tools() -> None:
    """Course RAG expert must attach all three custom repository tools."""
    with patch("methods.course_rag.agent.Agent") as mock_agent_cls:
        agent_module.get_course_rag_agent()
        kwargs = mock_agent_cls.call_args.kwargs
        tool_names = {getattr(t, "__name__", repr(t)) for t in kwargs["tools"]}
        assert "read_course_structure" in tool_names
        assert "get_session_data" in tool_names
        assert "search_local_glossary" in tool_names


def test_system_prompt_is_loaded_and_nonempty() -> None:
    """The system prompt must load from prompts/system.yaml and be substantial."""
    prompt = agent_module._load_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 200, "System prompt seems suspiciously short"
    # Sanity check: prompt must explicitly invoke the injection security block.
    assert "untrusted" in prompt.lower()
