from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType

class SimpleCompensationEvaluator:
    """
    A simple implementation of CompensationEvaluator protocol using basic rules
    and multipliers to estimate annual compensation.
    """

    def __init__(self):
        # Base salary by experience level (USD)
        self.base_salary_by_experience = {
            ExperienceLevel.JUNIOR: 40000.0,
            ExperienceLevel.MID_CAREER: 70000.0,
            ExperienceLevel.SENIOR: 100000.0
        }

        # Multipliers for education level
        self.education_multipliers = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 0.8,
            EducationLevel.UNDERGRADUATE: 1.0,
            EducationLevel.ADVANCED: 1.3
        }

        # Multipliers for industry sector
        self.industry_multipliers = {
            IndustrySector.RETAIL: 0.8,
            IndustrySector.MANUFACTURING: 0.9,
            IndustrySector.HEALTHCARE: 1.1,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.3,
            IndustrySector.FINANCIAL_SERVICES: 1.4
        }

        # Multipliers for employment type
        self.employment_multipliers = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 0.9
        }

    def evaluate(self, person: Person) -> float:
        """
        Evaluate expected annual compensation for a person based on their attributes.

        Args:
            person: Person instance with demographic and professional attributes

        Returns:
            Annual compensation in USD as a float
        """
        # Start with base salary based on experience level
        base_salary = self.base_salary_by_experience[person.experience_level]

        # Apply education multiplier
        salary = base_salary * self.education_multipliers[person.education_level]

        # Apply industry multiplier
        salary *= self.industry_multipliers[person.industry_sector]

        # Apply employment type multiplier
        salary *= self.employment_multipliers[person.employment_type]

        return round(salary, 2)
