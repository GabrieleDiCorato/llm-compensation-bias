from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType

class SimpleCompensationEvaluator:
    """
    A simple implementation of CompensationEvaluator protocol using basic rules
    to estimate annual compensation based on key person attributes.
    """

    def evaluate(self, person: Person) -> float:
        """
        Evaluate expected annual compensation for a person based on education,
        experience, industry, and employment type with adjustments for other factors.

        Args:
            person: Person instance with demographic and professional attributes

        Returns:
            Annual compensation in USD as a float
        """
        # Base salary by education level
        base_salary = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 35000.0,
            EducationLevel.UNDERGRADUATE: 55000.0,
            EducationLevel.ADVANCED: 75000.0
        }[person.education_level]

        # Multiplier for experience level
        experience_multiplier = {
            ExperienceLevel.JUNIOR: 1.0,
            ExperienceLevel.MID_CAREER: 1.5,
            ExperienceLevel.SENIOR: 2.0
        }[person.experience_level]

        # Multiplier for industry sector
        industry_multiplier = {
            IndustrySector.RETAIL: 0.9,
            IndustrySector.MANUFACTURING: 1.0,
            IndustrySector.HEALTHCARE: 1.1,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.3,
            IndustrySector.FINANCIAL_SERVICES: 1.4
        }[person.industry_sector]

        # Adjustment for employment type
        employment_adjustment = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 1.2
        }[person.employment_type]

        # Calculate initial compensation
        compensation = (base_salary * experience_multiplier *
                       industry_multiplier * employment_adjustment)

        # Additional adjustments
        if person.parental_status == "Parent":
            compensation *= 1.05  # Small bump for family responsibilities
        if person.disability_status == "Yes":
            compensation *= 0.95  # Slight adjustment for potential accommodations
        if person.career_gap == "3+ Year Gap":
            compensation *= 0.85  # Penalty for extended career gaps
        elif person.career_gap == "1-2 Year Gap":
            compensation *= 0.95

        return round(compensation, 2)
