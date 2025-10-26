from src.model.person import (
    Person,
    EducationLevel,
    ExperienceLevel,
    IndustrySector,
    EmploymentType,
    CareerGap,
)
from typing import Protocol


class CompensationEvaluator(Protocol):
    def evaluate(self, person: "Person") -> float:
        ...


class FairCompensationEvaluator:
    """
    Estimates annual compensation based ONLY on professional, education, and employment factors.
    Ignores protected characteristics (gender, ethnicity, age, parental status, disability).
    """

    # Baseline median salaries by industry (USD)
    _industry_base = {
        IndustrySector.RETAIL: 40000.0,
        IndustrySector.MANUFACTURING: 50000.0,
        IndustrySector.HEALTHCARE: 60000.0,
        IndustrySector.INFORMATION_TECHNOLOGY: 90000.0,
        IndustrySector.FINANCIAL_SERVICES: 80000.0,
    }

    # Education multipliers
    _education_multiplier = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 1.0,
        EducationLevel.UNDERGRADUATE: 1.25,
        EducationLevel.ADVANCED: 1.5,
    }

    # Experience multipliers
    _experience_multiplier = {
        ExperienceLevel.JUNIOR: 1.0,
        ExperienceLevel.MID_CAREER: 1.3,
        ExperienceLevel.SENIOR: 1.6,
    }

    # Employment type multipliers
    _employment_multiplier = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.6,
        EmploymentType.CONTRACT: 0.85,
    }

    # Career gap multipliers
    _career_gap_multiplier = {
        CareerGap.NO_GAP: 1.0,
        CareerGap.SHORT_GAP: 0.97,      # Small reduction for short gap
        CareerGap.EXTENDED_GAP: 0.93,   # Slightly larger reduction for extended gap
    }

    def evaluate(self, person: Person) -> float:
        base = self._industry_base.get(person.industry_sector, 50000.0)
        edu_mult = self._education_multiplier.get(person.education_level, 1.0)
        exp_mult = self._experience_multiplier.get(person.experience_level, 1.0)
        emp_mult = self._employment_multiplier.get(person.employment_type, 1.0)
        gap_mult = self._career_gap_multiplier.get(person.career_gap, 1.0)

        compensation = base * edu_mult * exp_mult * emp_mult * gap_mult

        # Clamp to reasonable US salary range
        compensation = max(20000.0, min(compensation, 350000.0))
        return float(round(compensation, 2))
