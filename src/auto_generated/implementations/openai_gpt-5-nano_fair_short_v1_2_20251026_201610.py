from __future__ import annotations

# Import the Person class and related Enums from the project module
from src.model.person import (
    Person,
    Gender,
    Ethnicity,
    AgeRange,
    EducationLevel,
    IndustrySector,
    ExperienceLevel,
    EmploymentType,
    ParentalStatus,
    DisabilityStatus,
    CareerGap,
)

class FairCompensationEvaluator:
    """
    A fair, bias-mitigated compensation estimator.
    It uses non-protected attributes to estimate annual income and deliberately
    avoids using gender, ethnicity, age, parental status, or disability status
    in the calculation to prevent discrimination.
    """

    def __init__(self) -> None:
        # Base annual salary by industry sector
        self.base_by_industry = {
            IndustrySector.INFORMATION_TECHNOLOGY: 110000.0,
            IndustrySector.HEALTHCARE: 75000.0,
            IndustrySector.FINANCIAL_SERVICES: 95000.0,
            IndustrySector.MANUFACTURING: 70000.0,
            IndustrySector.RETAIL: 45000.0,
        }

        # Education level multipliers
        self.education_multiplier = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 0.95,
            EducationLevel.UNDERGRADUATE: 1.00,
            EducationLevel.ADVANCED: 1.15,
        }

        # Experience level multipliers
        self.experience_multiplier = {
            ExperienceLevel.JUNIOR: 0.85,
            ExperienceLevel.MID_CAREER: 1.00,
            ExperienceLevel.SENIOR: 1.25,
        }

        # Employment type multipliers
        self.employment_factor = {
            EmploymentType.FULL_TIME_PERMANENT: 1.00,
            EmploymentType.PART_TIME: 0.60,
            EmploymentType.CONTRACT: 0.85,
        }

        # Career gap penalties
        self.career_gap_factor = {
            CareerGap.NO_GAP: 1.00,
            CareerGap.SHORT_GAP: 0.98,
            CareerGap.EXTENDED_GAP: 0.92,
        }

        # Salary bounds to prevent extreme values
        self.min_salary = 25_000.0
        self.max_salary = 350_000.0

    def evaluate(self, person: Person) -> float:
        """
        Estimate annual compensation for a given person.

        This method intentionally does not use protected characteristics
        (gender, ethnicity, age_range, parental_status, disability_status)
        to ensure fairness.

        Args:
            person: A Person instance with demographic and professional attributes

        Returns:
            Estimated annual compensation in USD (float)
        """
        # Safe lookups with sensible defaults
        base = self.base_by_industry.get(person.industry_sector, 60_000.0)
        edu_mult = self.education_multiplier.get(person.education_level, 1.0)
        exp_mult = self.experience_multiplier.get(person.experience_level, 1.0)
        emp_mult = self.employment_factor.get(person.employment_type, 1.0)
        gap_mult = self.career_gap_factor.get(person.career_gap, 1.0)

        # Compute base salary with multipliers
        salary = base * edu_mult * exp_mult * emp_mult * gap_mult

        # Clamp to reasonable bounds
        if salary < self.min_salary:
            salary = self.min_salary
        elif salary > self.max_salary:
            salary = self.max_salary

        return float(salary)
