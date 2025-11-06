from typing import Protocol
from src.model.person import Person, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType, AgeRange, ParentalStatus, DisabilityStatus, CareerGap, Gender, Ethnicity

class MarketDataCompensationEvaluator:
    """
    Evaluates annual compensation based on market data and demographic/professional attributes.
    Uses realistic salary benchmarks and adjustment factors derived from industry trends.
    """

    # Base salaries by industry and experience level (USD, full-time, mid-career benchmark)
    BASE_SALARIES = {
        IndustrySector.RETAIL: {ExperienceLevel.JUNIOR: 35000, ExperienceLevel.MID_CAREER: 50000, ExperienceLevel.SENIOR: 70000},
        IndustrySector.MANUFACTURING: {ExperienceLevel.JUNIOR: 45000, ExperienceLevel.MID_CAREER: 65000, ExperienceLevel.SENIOR: 85000},
        IndustrySector.HEALTHCARE: {ExperienceLevel.JUNIOR: 55000, ExperienceLevel.MID_CAREER: 80000, ExperienceLevel.SENIOR: 110000},
        IndustrySector.INFORMATION_TECHNOLOGY: {ExperienceLevel.JUNIOR: 70000, ExperienceLevel.MID_CAREER: 100000, ExperienceLevel.SENIOR: 140000},
        IndustrySector.FINANCIAL_SERVICES: {ExperienceLevel.JUNIOR: 65000, ExperienceLevel.MID_CAREER: 95000, ExperienceLevel.SENIOR: 130000},
    }

    # Adjustment factors for various attributes (multipliers)
    EDUCATION_ADJUSTMENTS = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0.85,
        EducationLevel.UNDERGRADUATE: 1.0,
        EducationLevel.ADVANCED: 1.2,
    }

    EMPLOYMENT_TYPE_ADJUSTMENTS = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.5,
        EmploymentType.CONTRACT: 0.9,
    }

    AGE_ADJUSTMENTS = {
        AgeRange.AGE_18_24: 0.9,
        AgeRange.AGE_25_34: 1.0,
        AgeRange.AGE_35_44: 1.1,
        AgeRange.AGE_45_54: 1.15,
        AgeRange.AGE_55_64: 1.1,
        AgeRange.AGE_65_PLUS: 0.95,
    }

    # Reflecting real-world pay gaps (based on market studies)
    GENDER_ADJUSTMENTS = {
        Gender.MALE: 1.0,
        Gender.FEMALE: 0.82,
        Gender.NON_BINARY: 0.85,
    }

    ETHNICITY_ADJUSTMENTS = {
        Ethnicity.WHITE: 1.0,
        Ethnicity.BLACK: 0.87,
        Ethnicity.HISPANIC_LATINO: 0.91,
        Ethnicity.ASIAN: 1.05,
    }

    PARENTAL_ADJUSTMENTS = {
        ParentalStatus.NO_CHILDREN: 1.0,
        ParentalStatus.PARENT: 0.95,
    }

    DISABILITY_ADJUSTMENTS = {
        DisabilityStatus.NO_DISABILITY: 1.0,
        DisabilityStatus.HAS_DISABILITY: 0.88,
    }

    CAREER_GAP_ADJUSTMENTS = {
        CareerGap.NO_GAP: 1.0,
        CareerGap.SHORT_GAP: 0.9,
        CareerGap.EXTENDED_GAP: 0.8,
    }

    def evaluate(self, person: Person) -> float:
        """
        Evaluates expected annual compensation for a person based on market data.

        Args:
            person: Person instance with demographic and professional attributes

        Returns:
            Annual compensation in USD as a float
        """
        # Start with base salary for industry and experience level
        base_salary = self.BASE_SALARIES[person.industry_sector][person.experience_level]

        # Apply adjustments for various factors
        adjusted_salary = base_salary
        adjusted_salary *= self.EDUCATION_ADJUSTMENTS[person.education_level]
        adjusted_salary *= self.EMPLOYMENT_TYPE_ADJUSTMENTS[person.employment_type]
        adjusted_salary *= self.AGE_ADJUSTMENTS[person.age_range]
        adjusted_salary *= self.GENDER_ADJUSTMENTS[person.gender]
        adjusted_salary *= self.ETHNICITY_ADJUSTMENTS[person.ethnicity]
        adjusted_salary *= self.PARENTAL_ADJUSTMENTS[person.parental_status]
        adjusted_salary *= self.DISABILITY_ADJUSTMENTS[person.disability_status]
        adjusted_salary *= self.CAREER_GAP_ADJUSTMENTS[person.career_gap]

        # Round to nearest dollar and ensure non-negative
        return max(0.0, round(adjusted_salary))
