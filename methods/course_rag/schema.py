"""Pydantic output schema for the Course RAG Agent method.

The schema is the contract between the LLM and everything else in this folder.
Ensures strict validation, explicit constraints, and fields forbidden to shift.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class GlossaryTermSchema(BaseModel):
    """Strict structure for an individual glossary term returned by the LLM."""

    model_config = ConfigDict(extra="forbid", strict=True, str_strip_whitespace=True)

    term: str = Field(
        ...,
        min_length=2,
        max_length=80,
        description="The exact technical name of the concept found in the database.",
    )
    definition: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="The exact plain-language definition extracted from local database context.",
    )


class CourseRagResponseSchema(BaseModel):
    """Structured output for the Course RAG presentation and verification method."""

    # Configurăm comportamentul echivalent cu StrictBaseModel din șablonul tău
    model_config = ConfigDict(
        extra="forbid",  # Interzice câmpurile extra strecurate de LLM
        strict=True,  # Dezactivează coerciția automată a tipurilor (ex: fără "5" -> 5)
        str_strip_whitespace=True,  # Curăță automat spațiile goale de la început/sfârșit
    )

    answer: str = Field(
        ...,
        min_length=30,
        max_length=1000,
        description=(
            "The direct, highly accurate response to the user query. "
            "Must be grounded ONLY in the provided course context or local database."
        ),
    )

    matched_session_id: Optional[int] = Field(
        None,
        description="The precise course session ID (42-50) where the core answer resides.",
    )

    related_glossary_terms: List[GlossaryTermSchema] = Field(
        default_factory=list,
        description="List of verified terms from the local database that back up this specific answer.",
    )

    quick_check_question: str = Field(
        ...,
        min_length=15,
        max_length=300,
        description=(
            "An open-ended evaluation question generated dynamically to test the user's "
            "understanding of this response. Must end with '?'."
        ),
    )

    # --- Validators ----------------------------------------------------------

    @field_validator("answer", "quick_check_question")
    @classmethod
    def _reject_whitespace_only(cls, value: str) -> str:
        """Guards explicitly against strings containing nothing but spaces."""
        if not value.strip():
            raise ValueError("must contain non-whitespace characters")
        return value

    @field_validator("quick_check_question")
    @classmethod
    def _must_end_with_question_mark(cls, value: str) -> str:
        """A verification retrieval question must dynamically end with a proper symbol."""
        if not value.rstrip().endswith("?"):
            raise ValueError("must end with '?'")
        return value

    @field_validator("matched_session_id")
    @classmethod
    def _validate_session_range(cls, value: Optional[int]) -> Optional[int]:
        """Ensures that the matched session falls strictly within the scope of our course."""
        if value is not None and not (42 <= value <= 50):
            raise ValueError("matched_session_id must be an integer between 42 and 50")
        return value
