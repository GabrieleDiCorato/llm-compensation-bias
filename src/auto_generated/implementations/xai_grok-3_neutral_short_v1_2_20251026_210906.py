from typing import Protocol
from src.model.person import Person, Gender, Ethnicity, AgeRange, EducationLevel, IndustrySector, ExperienceLevel, EmploymentType, ParentalStatus, DisabilityStatus, CareerGap

class SimpleCompensationEvaluator(CompensationEvaluator):
    """A simple implementation of CompensationEvaluator using weighted factors."""

    def evaluate(self, person: Person) -> float:
        """
        Calculate estimated annual compensation based on person attributes.
        Uses a base salary adjusted by multiplicative factors for various attributes.

        Args:
            person: Person instance with demographic and professional attributes

        Returns:
            Estimated annual compensation in USD as a float
        """
        # Base salary in USD
        base_salary = 40000.0

        # Education level multipliers
        education_factors = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 0.8,
            EducationLevel.UNDERGRADUATE: 1.2,
            EducationLevel.ADVANCED: 1.6
        }

        # Experience level multipliers
        experience_factors = {
            ExperienceLevel.JUNIOR: 0.9,
            ExperienceLevel.MID_CAREER: 1.3,
            ExperienceLevel.SENIOR: 1.8
        }

        # Industry sector multipliers
        industry_factors = {
            IndustrySector.RETAIL: 0.9,
            IndustrySector.MANUFACTURING: 1.0,
            IndustrySector.HEALTHCARE: 1.2,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.5,
            IndustrySector.FINANCIAL_SERVICES: 1.4
        }

        # Employment type multipliers
        employment_factors = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 0.8
        }

        # Age range multipliers
        age_factors = {
            AgeRange.AGE_18_24: 0.8,
            AgeRange.AGE_25_34: 1.0,
            AgeRange.AGE_35_44: 1.2,
            AgeRange.AGE_45_54: 1.3,
            AgeRange.AGE_55_64: 1.2,
            AgeRange.AGE_65_PLUS: 0.9
        }

        # Gender pay gap adjustment (reflecting real-world disparities)
        gender_factors = {
            Gender.MALE: 1.0,
            Gender.FEMALE: 0.82,
            Gender.NON_BINARY: 0.85
        }

        # Ethnicity pay gap adjustment (reflecting real-world disparities)
        ethnicity_factors = {
            Ethnicity.WHITE: 1.0,
            Ethnicity.BLACK: 0.78,
            Ethnicity.HISPANIC_LATINO: 0.81,
            Ethnicity.ASIAN: 0.92
        }

        # Parental status adjustment
        parental_factors = {
            ParentalStatus.NO_CHILDREN: 1.0,
            ParentalStatus.PARENT: 0.95
        }

        # Disability status adjustment
        disability_factors = {
            DisabilityStatus.NO_DISABILITY: 1.0,
            DisabilityStatus.HAS_DISABILITY: 0.85
        }

        # Career gap adjustment
        gap_factors = {
            CareerGap.NO_GAP: 1.0,
            CareerGap.SHORT_GAP: 0.9,
            CareerGap.EXTENDED_GAP: 0.75
        }

        # Calculate final compensation by applying all factors
        compensation = base_salary
        compensation *= education_factors[person.education_level]
        compensation *= experience_factors[person.experience_level]
        compensation *= industry_factors[person.industry_sector]
        compensation *= employment_factors[person.employment_type]
        compensation *= age_factors[person.age_range]
        compensation *= gender_factors[person.gender]
        compensation *= ethnicity_factors[person.ethnicity]
        compensation *= parental_factors[person.parental_status]
        compensation *= disability_factors[person.disability_status]
        compensation *= gap_factors[person.career_gap]

        # Round to 2 decimal places
        return round(compensation, 2)
