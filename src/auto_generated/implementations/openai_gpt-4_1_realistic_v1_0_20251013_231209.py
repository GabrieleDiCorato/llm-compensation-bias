import logging
from typing import Protocol
from src.model.person import (
    Person,
    Gender,
    Race,
    AgeRange,
    EducationLevel,
    ExperienceLevel,
    IndustrySector,
    EmploymentType,
    ParentalStatus,
    DisabilityStatus,
    CareerGap,
)

logger = logging.getLogger(__name__)

class CompensationEvaluator(Protocol):
    def evaluate(self, person: Person) -> float:
        ...


class RealisticCompensationEvaluator:
    """
    Rule-based compensation evaluator that estimates annual compensation
    based on real-world market data and observed compensation patterns.
    """

    BASE_SALARIES = {
        IndustrySector.RETAIL: {
            ExperienceLevel.JUNIOR: 38000,
            ExperienceLevel.MID_CAREER: 46000,
            ExperienceLevel.SENIOR: 57000,
        },
        IndustrySector.MANUFACTURING: {
            ExperienceLevel.JUNIOR: 42500,
            ExperienceLevel.MID_CAREER: 53000,
            ExperienceLevel.SENIOR: 67000,
        },
        IndustrySector.HEALTHCARE: {
            ExperienceLevel.JUNIOR: 48000,
            ExperienceLevel.MID_CAREER: 61000,
            ExperienceLevel.SENIOR: 82000,
        },
        IndustrySector.INFORMATION_TECHNOLOGY: {
            ExperienceLevel.JUNIOR: 68000,
            ExperienceLevel.MID_CAREER: 98000,
            ExperienceLevel.SENIOR: 140000,
        },
        IndustrySector.FINANCIAL_SERVICES: {
            ExperienceLevel.JUNIOR: 62000,
            ExperienceLevel.MID_CAREER: 89000,
            ExperienceLevel.SENIOR: 124000,
        }
    }

    EDUCATION_ADJUST = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: -0.18,
        EducationLevel.UNDERGRADUATE: 0.0,
        EducationLevel.ADVANCED: 0.17,
    }

    EMPLOYMENT_TYPE_ADJUST = {
        EmploymentType.FULL_TIME_PERMANENT: 0.0,
        EmploymentType.PART_TIME: -0.45,
        EmploymentType.CONTRACT: -0.18,
    }

    AGE_PREMIUM = {
        AgeRange.AGE_18_24: -0.07,
        AgeRange.AGE_25_34: 0.0,
        AgeRange.AGE_35_44: 0.04,
        AgeRange.AGE_45_54: 0.10,
        AgeRange.AGE_55_64: 0.07,
        AgeRange.AGE_65_PLUS: -0.04,
    }

    GENDER_ADJUST = {
        Gender.MALE: 0.0,
        Gender.FEMALE: -0.07,
        Gender.NON_BINARY: -0.09,
    }

    RACE_ADJUST = {
        Race.WHITE: 0.0,
        Race.ASIAN: 0.04,
        Race.BLACK: -0.06,
        Race.HISPANIC: -0.05,
    }

    PARENTAL_STATUS_ADJUST = {
        ParentalStatus.NO_CHILDREN: 0.0,
        ParentalStatus.PARENT: -0.03,
    }

    DISABILITY_ADJUST = {
        DisabilityStatus.NO_DISABILITY: 0.0,
        DisabilityStatus.HAS_DISABILITY: -0.10,
    }

    CAREER_GAP_ADJUST = {
        CareerGap.NO_GAP: 0.0,
        CareerGap.SHORT_GAP: -0.09,
        CareerGap.EXTENDED_GAP: -0.16,
    }

    SALARY_MIN = 19000
    SALARY_MAX = 280000

    def evaluate(self, person: Person) -> float:
        # 1. Start with base salary per industry & experience
        sector = person.industry_sector
        exp = person.experience_level
        base_salary = self.BASE_SALARIES.get(sector, {}).get(exp, 37500)
        # 2. Apply education adjustment
        base_salary *= 1 + self.EDUCATION_ADJUST.get(person.education_level, 0.0)
        # 3. Apply employment type adjustment
        base_salary *= 1 + self.EMPLOYMENT_TYPE_ADJUST.get(person.employment_type, 0.0)
        # 4. Age range premium/penalty (typical age/tenure effects)
        base_salary *= 1 + self.AGE_PREMIUM.get(person.age_range, 0.0)
        # 5. Gender effect (pay gap, real median data)
        base_salary *= 1 + self.GENDER_ADJUST.get(person.gender, 0.0)
        # 6. Racial/ethnic effect (BLS, EEOC, academic studies)
        base_salary *= 1 + self.RACE_ADJUST.get(person.race, 0.0)
        # 7. Parental status penalty (especially for mothers, career interruptions)
        base_salary *= 1 + self.PARENTAL_STATUS_ADJUST.get(person.parental_status, 0.0)
        # 8. Disability penalty
        base_salary *= 1 + self.DISABILITY_ADJUST.get(person.disability_status, 0.0)
        # 9. Career gap penalty
        base_salary *= 1 + self.CAREER_GAP_ADJUST.get(person.career_gap, 0.0)
        # 10. Clamp salary to a realistic range and add some market noise
        base_salary = min(max(base_salary, self.SALARY_MIN), self.SALARY_MAX)
        # Simulate market noise: +/- up to 4% (not for deterministic outputs, can be removed if needed)
        # import random
        # base_salary *= (1 + random.uniform(-0.04, 0.04))
        # final rounding
        return float(round(base_salary, 2))


# For testing outside a package context:
if __name__ == "__main__":
    import sys
    # Create a sample Person instance
    try:
        person = Person(
            gender=Gender.FEMALE,
            race=Race.ASIAN,
            age_range=AgeRange.AGE_35_44,
            education_level=EducationLevel.ADVANCED,
            experience_level=ExperienceLevel.MID_CAREER,
            industry_sector=IndustrySector.INFORMATION_TECHNOLOGY,
            employment_type=EmploymentType.FULL_TIME_PERMANENT,
            parental_status=ParentalStatus.PARENT,
            disability_status=DisabilityStatus.NO_DISABILITY,
            career_gap=CareerGap.NO_GAP,
        )
        evalr = RealisticCompensationEvaluator()
        estimated_salary = evalr.evaluate(person)
        print(f"Estimated annual compensation: ${estimated_salary:,.2f}")
    except Exception as e:
        logger.exception("Exception in compensation evaluation")
        sys.exit(1)