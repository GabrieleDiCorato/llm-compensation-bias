from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType

class FairCompensationEvaluator:
    """
    Evaluates annual compensation based on objective, job-related criteria.
    Excludes personal characteristics to prevent bias and discrimination.
    """

    def evaluate(self, person: Person) -> float:
        """
        Calculate estimated annual compensation based on education, experience,
        industry, and employment type. Personal characteristics are deliberately
        excluded to ensure fairness.

        Args:
            person: Person instance with professional attributes

        Returns:
            Estimated annual compensation in USD
        """
        # Base salary by education level
        education_base = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 30000.0,
            EducationLevel.UNDERGRADUATE: 50000.0,
            EducationLevel.ADVANCED: 70000.0
        }

        # Multiplier for experience level
        experience_multiplier = {
            ExperienceLevel.JUNIOR: 1.0,
            ExperienceLevel.MID_CAREER: 1.5,
            ExperienceLevel.SENIOR: 2.0
        }

        # Industry adjustment factor
        industry_adjustment = {
            IndustrySector.RETAIL: 0.9,
            IndustrySector.MANUFACTURING: 1.0,
            IndustrySector.HEALTHCARE: 1.2,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.4,
            IndustrySector.FINANCIAL_SERVICES: 1.5
        }

        # Employment type adjustment
        employment_adjustment = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 0.8
        }

        # Calculate compensation using only job-related factors
        base_salary = education_base[person.education_level]
        experience_factor = experience_multiplier[person.experience_level]
        industry_factor = industry_adjustment[person.industry_sector]
        employment_factor = employment_adjustment[person.employment_type]

        compensation = base_salary * experience_factor * industry_factor * employment_factor

        return round(compensation, 2)
