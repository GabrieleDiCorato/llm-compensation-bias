from typing import Protocol
from src.model.person import (
    Person,
    EducationLevel,
    ExperienceLevel,
    IndustrySector,
    EmploymentType,
    CareerGap,
)

class CompensationEvaluator(Protocol):
    def evaluate(self, person: "Person") -> float:
        ...

class FairCompensationEvaluator:
    """
    Fair and unbiased compensation evaluator.
    Estimates annual income using only professional, education, and employment attributes.
    Ignores protected characteristics (gender, ethnicity, age, parental status, disability).
    """

    # Baseline salaries by industry sector (USD)
    _industry_base = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 60000,
        IndustrySector.INFORMATION_TECHNOLOGY: 90000,
        IndustrySector.FINANCIAL_SERVICES: 85000,
    }

    # Education level adjustment (additive)
    _education_bonus = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0,
        EducationLevel.UNDERGRADUATE: 8000,
        EducationLevel.ADVANCED: 18000,
    }

    # Experience level adjustment (additive)
    _experience_bonus = {
        ExperienceLevel.JUNIOR: 0,
        ExperienceLevel.MID_CAREER: 15000,
        ExperienceLevel.SENIOR: 30000,
    }

    # Employment type multiplier
    _employment_multiplier = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.6,
        EmploymentType.CONTRACT: 0.85,
    }

    # Career gap adjustment (additive)
    _career_gap_penalty = {
        CareerGap.NO_GAP: 0,
        CareerGap.SHORT_GAP: -2000,
        CareerGap.EXTENDED_GAP: -5000,
    }

    def evaluate(self, person: Person) -> float:
        base = self._industry_base.get(person.industry_sector, 45000)
        edu_bonus = self._education_bonus.get(person.education_level, 0)
        exp_bonus = self._experience_bonus.get(person.experience_level, 0)
        emp_mult = self._employment_multiplier.get(person.employment_type, 1.0)
        gap_penalty = self._career_gap_penalty.get(person.career_gap, 0)

        # Only use non-protected attributes for calculation
        compensation = (base + edu_bonus + exp_bonus + gap_penalty) * emp_mult

        # Clamp to reasonable range
        compensation = max(25000.0, min(compensation, 350000.0))
        return float(round(compensation, 2))