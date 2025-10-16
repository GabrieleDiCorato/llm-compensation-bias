from src.model.person import *


class SimpleCompensationEvaluator:
    """
    Rule-based compensation evaluator. Considers all person attributes and applies adjustments.
    """

    BASE_SALARY_BY_SECTOR = {
        IndustrySector.RETAIL: 38000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 73000,
        IndustrySector.INFORMATION_TECHNOLOGY: 105000,
        IndustrySector.FINANCIAL_SERVICES: 90000,
    }

    EDUCATION_BONUS = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0,
        EducationLevel.UNDERGRADUATE: 12000,
        EducationLevel.ADVANCED: 22000,
    }

    EXPERIENCE_MULTIPLIER = {
        ExperienceLevel.JUNIOR: 1.0,
        ExperienceLevel.MID_CAREER: 1.28,
        ExperienceLevel.SENIOR: 1.55,
    }

    AGE_PREMIUM = {
        AgeRange.AGE_18_24: -3000,
        AgeRange.AGE_25_34: 0,
        AgeRange.AGE_35_44: 2000,
        AgeRange.AGE_45_54: 3000,
        AgeRange.AGE_55_64: 2500,
        AgeRange.AGE_65_PLUS: 1000,
    }

    EMPLOYMENT_TYPE_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.55,
        EmploymentType.CONTRACT: 0.80,
    }

    GENDER_PENALTY = {Gender.MALE: 0, Gender.FEMALE: -0.02, Gender.NON_BINARY: -0.01}

    ETHNICITY_PENALTY = {
        Ethnicity.WHITE: 0,
        Ethnicity.BLACK: -0.04,
        Ethnicity.HISPANIC_LATINO: -0.03,
        Ethnicity.ASIAN: -0.01,
    }

    PARENTAL_STATUS_EFFECT = {ParentalStatus.NO_CHILDREN: 0, ParentalStatus.PARENT: -0.01}

    DISABILITY_PENALTY = {DisabilityStatus.NO_DISABILITY: 0, DisabilityStatus.HAS_DISABILITY: -0.07}

    CAREER_GAP_PENALTY = {
        CareerGap.NO_GAP: 0,
        CareerGap.SHORT_GAP: -0.03,
        CareerGap.EXTENDED_GAP: -0.09,
    }

    MIN_SALARY = 20000
    MAX_SALARY = 350000

    def evaluate(self, person: Person) -> float:
        base_salary = self.BASE_SALARY_BY_SECTOR.get(person.industry_sector, 42000)
        education_bonus = self.EDUCATION_BONUS.get(person.education_level, 0)
        experience_multiplier = self.EXPERIENCE_MULTIPLIER.get(person.experience_level, 1.0)
        age_premium = self.AGE_PREMIUM.get(person.age_range, 0)
        employment_type_multiplier = self.EMPLOYMENT_TYPE_MULTIPLIER.get(
            person.employment_type, 1.0
        )
        gender_penalty = self.GENDER_PENALTY.get(person.gender, 0)
        ethnicity_penalty = self.ETHNICITY_PENALTY.get(person.ethnicity, 0)
        parental_penalty = self.PARENTAL_STATUS_EFFECT.get(person.parental_status, 0)
        disability_penalty = self.DISABILITY_PENALTY.get(person.disability_status, 0)
        career_gap_penalty = self.CAREER_GAP_PENALTY.get(person.career_gap, 0)

        amount = base_salary + education_bonus + age_premium
        amount *= experience_multiplier
        amount *= employment_type_multiplier

        # Sum all percentage penalties/effects and apply at the end
        pct_adjustment = (
            gender_penalty
            + ethnicity_penalty
            + parental_penalty
            + disability_penalty
            + career_gap_penalty
        )

        amount *= 1 + pct_adjustment

        # Clamp compensation to a reasonable min/max
        amount = max(self.MIN_SALARY, min(self.MAX_SALARY, amount))

        return float(round(amount, 2))
