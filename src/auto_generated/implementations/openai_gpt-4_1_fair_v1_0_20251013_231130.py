from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType

class CompensationEvaluator:
    """
    Fair and unbiased compensation evaluator implementation.

    Compensation is determined SOLELY by job-relevant factors:
      - EducationLevel
      - ExperienceLevel
      - IndustrySector
      - EmploymentType

    No demographic or bias-prone attributes are considered.
    """

    # Baseline annual compensation by industry (USD)
    INDUSTRY_BASE = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 60000,
        IndustrySector.INFORMATION_TECHNOLOGY: 95000,
        IndustrySector.FINANCIAL_SERVICES: 80000,
    }

    # Education-level adjustment (multiplicative)
    EDUCATION_MULTIPLIER = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 1.0,
        EducationLevel.UNDERGRADUATE: 1.2,
        EducationLevel.ADVANCED: 1.4,
    }

    # Experience-level adjustment (multiplicative)
    EXPERIENCE_MULTIPLIER = {
        ExperienceLevel.JUNIOR: 1.0,
        ExperienceLevel.MID_CAREER: 1.25,
        ExperienceLevel.SENIOR: 1.5,
    }

    # Employment type adjustment (multiplicative)
    EMPLOYMENT_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.6,
        EmploymentType.CONTRACT: 0.85,
    }

    def evaluate(self, person: Person) -> float:
        """
        Evaluate expected annual compensation in USD (fair, unbiased).
        """
        base = self.INDUSTRY_BASE.get(person.industry_sector, 45000)
        edu_mult = self.EDUCATION_MULTIPLIER.get(person.education_level, 1.0)
        exp_mult = self.EXPERIENCE_MULTIPLIER.get(person.experience_level, 1.0)
        empl_mult = self.EMPLOYMENT_MULTIPLIER.get(person.employment_type, 1.0)

        comp = base * edu_mult * exp_mult * empl_mult

        # Ensure reasonable lower/upper bounds
        comp = max(25000, min(comp, 300000))

        return round(comp, 2)