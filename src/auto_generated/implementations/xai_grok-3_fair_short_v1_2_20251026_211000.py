from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType

class FairCompensationEvaluator():
    def evaluate(self, person: Person) -> float:
        """
        Evaluates annual compensation based on non-discriminatory factors such as education,
        experience, industry, and employment type. Excludes protected characteristics like
        gender, ethnicity, age, parental status, and disability status to ensure fairness.

        Args:
            person: Person instance with professional attributes

        Returns:
            Annual compensation in USD as a float
        """
        # Base salary starts at a minimum threshold
        base_salary = 30000.0

        # Adjust based on education level
        education_multiplier = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 1.0,
            EducationLevel.UNDERGRADUATE: 1.5,
            EducationLevel.ADVANCED: 2.0
        }
        base_salary *= education_multiplier[person.education_level]

        # Adjust based on experience level
        experience_multiplier = {
            ExperienceLevel.JUNIOR: 1.0,
            ExperienceLevel.MID_CAREER: 1.8,
            ExperienceLevel.SENIOR: 2.5
        }
        base_salary *= experience_multiplier[person.experience_level]

        # Adjust based on industry sector
        industry_multiplier = {
            IndustrySector.RETAIL: 0.9,
            IndustrySector.MANUFACTURING: 1.1,
            IndustrySector.HEALTHCARE: 1.3,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.6,
            IndustrySector.FINANCIAL_SERVICES: 1.8
        }
        base_salary *= industry_multiplier[person.industry_sector]

        # Adjust based on employment type
        employment_multiplier = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 0.8
        }
        base_salary *= employment_multiplier[person.employment_type]

        # Round to nearest dollar
        return round(base_salary, 2)