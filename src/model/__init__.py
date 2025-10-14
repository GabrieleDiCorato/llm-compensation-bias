"""
Data models for representing persons and their attributes.
"""

from .person import (
    Person,
    Gender,
    Ethnicity,
    AgeRange,
    EducationLevel,
    ExperienceLevel,
    IndustrySector,
    EmploymentType,
    ParentalStatus,
    DisabilityStatus,
    CareerGap,
)
from .llm_response import LLMResponse
from .prompt import PromptTemplate

__all__ = [
    "Person",
    "Gender",
    "Ethnicity",
    "AgeRange",
    "EducationLevel",
    "ExperienceLevel",
    "IndustrySector",
    "EmploymentType",
    "ParentalStatus",
    "DisabilityStatus",
    "CareerGap",
    "PromptTemplate",
    "LLMResponse",
]
