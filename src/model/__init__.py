"""
Data models for representing persons and their attributes.
"""

from .person import (
    Person,
    Gender,
    Race,
    AgeRange,
    EducationLevel,
    ExperienceLevel,
    IndustrySector,
    EmploymentType,
    ParentalStatus,
    DisabilityStatus,
    CareerGap,
)
from .prompt import PromptTemplate

__all__ = [
    "Person",
    "Gender",
    "Race",
    "AgeRange",
    "EducationLevel",
    "ExperienceLevel",
    "IndustrySector",
    "EmploymentType",
    "ParentalStatus",
    "DisabilityStatus",
    "CareerGap",
    "PromptTemplate",
]
