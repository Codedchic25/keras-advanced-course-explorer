"""Schema-level tests for CourseRagResponseSchema.

These tests run with no LLM, no network, no Agno — they exercise only the
Pydantic model. That keeps them fast and deterministic.
"""

from __future__ import annotations
import pytest
from pydantic import ValidationError

from methods.course_rag.schema import CourseRagResponseSchema


def test_happy_path_validates(valid_rag_response: CourseRagResponseSchema) -> None:
    """A fully-valid RAG response instance constructs without error."""
    assert "optimizer" in valid_rag_response.answer.lower()
    assert valid_rag_response.matched_session_id == 42
    assert valid_rag_response.quick_check_question.endswith("?")


def test_extra_fields_are_forbidden() -> None:
    """extra='forbid' on model_config must reject unknown fields from the LLM."""
    with pytest.raises(ValidationError) as excinfo:
        CourseRagResponseSchema.model_validate(
            {
                "answer": "A clean response that easily satisfies the minimum character limit constraint.",
                "matched_session_id": 44,
                "related_glossary_terms": [],
                "quick_check_question": "Does this question validate correctly?",
                "hacker_injected_field": "should be blocked",
            }
        )
    assert "hacker_injected_field" in str(excinfo.value)


def test_question_must_end_with_question_mark(
    valid_rag_response: CourseRagResponseSchema,
) -> None:
    """The quick_check_question validator must reject missing punctuation."""
    bad = valid_rag_response.model_dump()
    bad["quick_check_question"] = "This is a statement without a question mark"
    with pytest.raises(ValidationError) as excinfo:
        CourseRagResponseSchema.model_validate(bad)
    assert "must end with '?'" in str(excinfo.value)


def test_whitespace_only_strings_rejected() -> None:
    """A string containing only empty spaces should be explicitly rejected."""
    with pytest.raises(ValidationError):
        CourseRagResponseSchema.model_validate(
            {
                "answer": "   ",  # whitespace-only
                "matched_session_id": 42,
                "related_glossary_terms": [],
                "quick_check_question": "Is this still valid?",
            }
        )


def test_session_id_range_boundaries() -> None:
    """The session ID must reside strictly within the course bounds (42-50)."""
    with pytest.raises(ValidationError) as excinfo:
        CourseRagResponseSchema.model_validate(
            {
                "answer": "A clean response that easily satisfies the minimum character limit constraint.",
                "matched_session_id": 10,  # Invalid session out of course scope
                "related_glossary_terms": [],
                "quick_check_question": "Does this session work?",
            }
        )
    assert "matched_session_id must be an integer between 42 and 50" in str(
        excinfo.value
    )


def test_minimum_lengths_enforced() -> None:
    """An answer shorter than 30 characters must fail validation."""
    with pytest.raises(ValidationError):
        CourseRagResponseSchema.model_validate(
            {
                "answer": "short",  # Fails min_length=30
                "matched_session_id": 45,
                "related_glossary_terms": [],
                "quick_check_question": "Is this short answer valid?",
            }
        )
