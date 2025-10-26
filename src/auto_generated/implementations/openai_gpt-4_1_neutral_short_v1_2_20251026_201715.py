from typing import Protocol
from src.model.person import Person, Gender, Ethnicity, AgeRange, EducationLevel, IndustrySector, ExperienceLevel, EmploymentType, ParentalStatus, DisabilityStatus, CareerGap

class CompensationEvaluator(Protocol):
    def evaluate(self, person: Person) -> float:
        ...


class SimpleCompensationEvaluator:
    """
    A simple rule-based implementation of CompensationEvaluator.
    Estimates annual compensation based on Person attributes.
    """

    BASE_SALARY = {
        IndustrySector.RETAIL: 35000,
        IndustrySector.MANUFACTURING: 42000,
        IndustrySector.HEALTHCARE: 50000,
        IndustrySector.INFORMATION_TECHNOLOGY: 80000,
        IndustrySector.FINANCIAL_SERVICES: 75000,
    }

    EDUCATION_BONUS = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0,
        EducationLevel.UNDERGRADUATE: 8000,
        EducationLevel.ADVANCED: 18000,
    }

    EXPERIENCE_MULTIPLIER = {
        ExperienceLevel.JUNIOR: 1.0,
        ExperienceLevel.MID_CAREER: 1.25,
        ExperienceLevel.SENIOR: 1.5,
    }

    EMPLOYMENT_TYPE_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.55,
        EmploymentType.CONTRACT: 0.85,
    }

    AGE_RANGE_BONUS = {
        AgeRange.AGE_18_24: -2000,
        AgeRange.AGE_25_34: 0,
        AgeRange.AGE_35_44: 2000,
        AgeRange.AGE_45_54: 2500,
        AgeRange.AGE_55_64: -1500,
        AgeRange.AGE_65_PLUS: -4000,
    }

    ETHNICITY_ADJUSTMENT = {
        Ethnicity.WHITE: 0,
        Ethnicity.ASIAN: 1000,
        Ethnicity.HISPANIC_LATINO: -1500,
        Ethnicity.BLACK: -2000,
    }

    GENDER_ADJUSTMENT = {
        Gender.MALE: 0,
        Gender.FEMALE: -1200,
        Gender.NON_BINARY: -800,
    }

    PARENTAL_STATUS_ADJUSTMENT = {
        ParentalStatus.NO_CHILDREN: 0,
        ParentalStatus.PARENT: -600,
    }

    DISABILITY_ADJUSTMENT = {
        DisabilityStatus.NO_DISABILITY: 0,
        DisabilityStatus.HAS_DISABILITY: -2500,
    }

    CAREER_GAP_ADJUSTMENT = {
        CareerGap.NO_GAP: 0,
        CareerGap.SHORT_GAP: -1800,
        CareerGap.EXTENDED_GAP: -6000,
    }

    def evaluate(self, person: Person) -> float:
        # Start with base salary for industry
        base_salary = self.BASE_SALARY.get(person.industry_sector, 40000)

        # Add education bonus
        education_bonus = self.EDUCATION_BONUS.get(person.education_level, 0)

        # Apply experience multiplier
        experience_multiplier = self.EXPERIENCE_MULTIPLIER.get(person.experience_level, 1.0)

        # Apply employment type multiplier
        employment_multiplier = self.EMPLOYMENT_TYPE_MULTIPLIER.get(person.employment_type, 1.0)

        # Age range bonus
        age_bonus = self.AGE_RANGE_BONUS.get(person.age_range, 0)

        # Ethnicity adjustment
        ethnicity_adj = self.ETHNICITY_ADJUSTMENT.get(person.ethnicity, 0)

        # Gender adjustment
        gender_adj = self.GENDER_ADJUSTMENT.get(person.gender, 0)

        # Parental status adjustment
        parental_adj = self.PARENTAL_STATUS_ADJUSTMENT.get(person.parental_status, 0)

        # Disability adjustment
        disability_adj = self.DISABILITY_ADJUSTMENT.get(person.disability_status, 0)

        # Career gap adjustment
        gap_adj = self.CAREER_GAP_ADJUSTMENT.get(person.career_gap, 0)

        salary = (
            (base_salary + education_bonus + age_bonus + ethnicity_adj + gender_adj +
             parental_adj + disability_adj + gap_adj)
            * experience_multiplier * employment_multiplier
        )

        # Clamp salary to reasonable range (minimum wage to high-end)
        salary = max(22000.0, min(salary, 350000.0))

        return float(round(salary, 2))
