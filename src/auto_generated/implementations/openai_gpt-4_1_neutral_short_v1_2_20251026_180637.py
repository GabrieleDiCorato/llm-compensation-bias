from typing import Protocol

class CompensationEvaluator(Protocol):
    def evaluate(self, person: "Person") -> float:
        ...


class SimpleCompensationEvaluator:
    """
    A simple rule-based implementation of CompensationEvaluator.
    Estimates annual compensation based on Person attributes using
    base salary and additive/multiplicative adjustments.
    """

    BASE_SALARY = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 60000,
        IndustrySector.INFORMATION_TECHNOLOGY: 90000,
        IndustrySector.FINANCIAL_SERVICES: 85000,
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
        EmploymentType.CONTRACT: 0.8,
    }

    AGE_RANGE_BONUS = {
        AgeRange.AGE_18_24: -2000,
        AgeRange.AGE_25_34: 0,
        AgeRange.AGE_35_44: 2000,
        AgeRange.AGE_45_54: 2500,
        AgeRange.AGE_55_64: 1500,
        AgeRange.AGE_65_PLUS: -1000,
    }

    CAREER_GAP_PENALTY = {
        CareerGap.NO_GAP: 0.0,
        CareerGap.SHORT_GAP: -0.05,     # -5%
        CareerGap.EXTENDED_GAP: -0.12,  # -12%
    }

    DISABILITY_PENALTY = {
        DisabilityStatus.NO_DISABILITY: 0.0,
        DisabilityStatus.HAS_DISABILITY: -0.03, # -3%
    }

    PARENTAL_BONUS = {
        ParentalStatus.NO_CHILDREN: 0.0,
        ParentalStatus.PARENT: 1000,
    }

    ETHNICITY_ADJUSTMENT = {
        Ethnicity.WHITE: 1.00,
        Ethnicity.ASIAN: 1.02,   # +2%
        Ethnicity.HISPANIC_LATINO: 0.97, # -3%
        Ethnicity.BLACK: 0.96,   # -4%
    }

    GENDER_ADJUSTMENT = {
        Gender.MALE: 1.00,
        Gender.FEMALE: 0.97,      # -3%
        Gender.NON_BINARY: 0.96,  # -4%
    }

    def evaluate(self, person: "Person") -> float:
        base = self.BASE_SALARY[person.industry_sector]
        
        # Additive bonuses/penalties
        base += self.EDUCATION_BONUS[person.education_level]
        base += self.AGE_RANGE_BONUS[person.age_range]
        base += self.PARENTAL_BONUS[person.parental_status]
        
        # Multiplicative adjustments
        base *= self.EXPERIENCE_MULTIPLIER[person.experience_level]
        base *= self.EMPLOYMENT_TYPE_MULTIPLIER[person.employment_type]

        # Career gap and disability are percentage penalties
        penalty_multiplier = (
            1 +
            self.CAREER_GAP_PENALTY[person.career_gap] +
            self.DISABILITY_PENALTY[person.disability_status]
        )
        
        base *= penalty_multiplier

        # Demographic adjustments (ethnicity/gender)
        base *= self.ETHNICITY_ADJUSTMENT[person.ethnicity]
        base *= self.GENDER_ADJUSTMENT[person.gender]

        # Clamp to reasonable range
        min_salary = 20000
        max_salary = 350000
        return float(max(min_salary, min(max_salary, round(base, 2))))