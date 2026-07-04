"""Shared fixtures for Course RAG Expert tests.

Provides stable, mockable data streams and schema validation targets for
both functional unit verification and end-to-end integration tests.
"""

from __future__ import annotations
import pytest

from methods.course_rag.schema import CourseRagResponseSchema, GlossaryTermSchema


@pytest.fixture
def sample_query() -> str:
    """Returns a canonical technical question for unit testing."""
    return "What is an Optimizer in Keras?"


@pytest.fixture
def sample_session_id() -> str:
    """Returns a valid course session isolation scope."""
    return "42"


@pytest.fixture
def valid_rag_response() -> CourseRagResponseSchema:
    """A fully-valid sample RAG schema instance used for integration assertions."""
    return CourseRagResponseSchema(
        answer=(
            "An optimizer is a mathematical algorithm responsible for adjusting "
            "the weights of a neural network based on the gradients of the loss "
            "function to minimize total error during training."
        ),
        matched_session_id=42,
        related_glossary_terms=[
            GlossaryTermSchema(
                term="Optimizer",
                definition="Algoritm care ajusteaza greutatile retelei neuronale pentru a minimiza eroarea (ex: Adam, SGD).",
            )
        ],
        quick_check_question="How does an Adam optimizer dynamically adapt learning rates compared to standard SGD?",
    )
