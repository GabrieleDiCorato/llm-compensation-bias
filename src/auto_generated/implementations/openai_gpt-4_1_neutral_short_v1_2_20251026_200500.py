from typing import Protocol
from src.model.person import Person, Gender, Ethnicity, AgeRange, EducationLevel, IndustrySector, ExperienceLevel, EmploymentType, ParentalStatus, DisabilityStatus, CareerGap

class CompensationEvaluator(Protocol):
    def evaluate(self, person: Person) -> float:
        ...


class BaselineCompensationEvaluator:
    """
    Simple rule-based compensation evaluator for demonstration.
    Adjusts base salary by factors from person attributes.
    """

    BASE_SALARY = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 60000,
        IndustrySector.INFORMATION_TECHNOLOGY: 90000,
        IndustrySector.FINANCIAL_SERVICES: 80000,
    }

    EDUCATION_BONUS = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0,
        EducationLevel.UNDERGRADUATE: 10000,
        EducationLevel.ADVANCED: 20000,
    }

    EXPERIENCE_BONUS = {
        ExperienceLevel.JUNIOR: 0,
        ExperienceLevel.MID_CAREER: 15000,
        ExperienceLevel.SENIOR: 30000,
    }

    EMPLOYMENT_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.6,
        EmploymentType.CONTRACT: 0.8,
    }

    AGE_BONUS = {
        AgeRange.AGE_18_24: -2000,
        AgeRange.AGE_25_34: 0,
        AgeRange.AGE_35_44: 2000,
        AgeRange.AGE_45_54: 4000,
        AgeRange.AGE_55_64: 2000,
        AgeRange.AGE_65_PLUS: -5000,
    }

    CAREER_GAP_PENALTY = {
        CareerGap.NO_GAP: 0,
        CareerGap.SHORT_GAP: -3000,
        CareerGap.EXTENDED_GAP: -7000,
    }

    DISABILITY_PENALTY = {
        DisabilityStatus.NO_DISABILITY: 0,
        DisabilityStatus.HAS_DISABILITY: -2000
    }

    PARENTAL_PENALTY = {
        ParentalStatus.NO_CHILDREN: 0,
        ParentalStatus.PARENT: -1000
    }

    ETHNICITY_BONUS = {
        Ethnicity.WHITE: 0,
        Ethnicity.BLACK: -1000,
        Ethnicity.HISPANIC_LATINO: -1000,
        Ethnicity.ASIAN: 500
    }

    GENDER_BONUS = {
        Gender.MALE: 1000,
        Gender.FEMALE: -1000,
        Gender.NON_BINARY: -500
    }

    def evaluate(self, person: Person) -> float:
        base = self.BASE_SALARY.get(person.industry_sector, 45000)
        
        total = base
        total += self.EDUCATION_BONUS.get(person.education_level, 0)
        total += self.EXPERIENCE_BONUS.get(person.experience_level, 0)
        total += self.AGE_BONUS.get(person.age_range, 0)
        total += self.CAREER_GAP_PENALTY.get(person.career_gap, 0)
        total += self.DISABILITY_PENALTY.get(person.disability_status, 0)
        total += self.PARENTAL_PENALTY.get(person.parental_status, 0)
        total += self.ETHNICITY_BONUS.get(person.ethnicity, 0)
        total += self.GENDER_BONUS.get(person.gender, 0)

        multiplier = self.EMPLOYMENT_MULTIPLIER.get(person.employment_type, 1.0)
        
        estimated = total * multiplier

        # Clamp to reasonable range
        estimated = max(25000.0, min(estimated, 350000.0))
        
        return float(round(estimated, 2))