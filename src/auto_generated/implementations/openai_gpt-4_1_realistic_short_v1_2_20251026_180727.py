import math
from typing import Protocol

class MarketCompensationEvaluator:
    """
    Estimates annual compensation based on current US market data and observed pay patterns.
    Data sources referenced: BLS, Payscale, Glassdoor, EEOC, and peer-reviewed studies (2023-2024).
    """

    # Baseline median salaries by industry sector (USD, full-time)
    INDUSTRY_BASE = {
        IndustrySector.RETAIL: 38000,
        IndustrySector.MANUFACTURING: 57000,
        IndustrySector.HEALTHCARE: 63000,
        IndustrySector.INFORMATION_TECHNOLOGY: 95000,
        IndustrySector.FINANCIAL_SERVICES: 85000,
    }

    # Experience multipliers
    EXPERIENCE_MULTIPLIER = {
        ExperienceLevel.JUNIOR: 0.80,
        ExperienceLevel.MID_CAREER: 1.0,
        ExperienceLevel.SENIOR: 1.25,
    }

    # Education multipliers
    EDUCATION_MULTIPLIER = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0.85,
        EducationLevel.UNDERGRADUATE: 1.0,
        EducationLevel.ADVANCED: 1.15,
    }

    # Employment type multipliers
    EMPLOYMENT_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.55,
        EmploymentType.CONTRACT: 0.85,
    }

    # Gender pay gap adjustment (relative to male baseline)
    GENDER_ADJUSTMENT = {
        Gender.MALE: 1.0,
        Gender.FEMALE: 0.92,       # ~8% gap persists in US market
        Gender.NON_BINARY: 0.90,   # Estimated; limited data
    }

    # Ethnicity pay gap adjustment (relative to white baseline)
    ETHNICITY_ADJUSTMENT = {
        Ethnicity.WHITE: 1.0,
        Ethnicity.ASIAN: 1.05,     # Slight premium in STEM/IT
        Ethnicity.BLACK: 0.87,     # ~13% gap persists
        Ethnicity.HISPANIC_LATINO: 0.89,   # ~11% gap persists
    }

    # Age range adjustment (reflecting peak earning years)
    AGE_ADJUSTMENT = {
        AgeRange.AGE_18_24: 0.70,
        AgeRange.AGE_25_34: 0.90,
        AgeRange.AGE_35_44: 1.05,
        AgeRange.AGE_45_54: 1.10,
        AgeRange.AGE_55_64: 1.05,
        AgeRange.AGE_65_PLUS: 0.80,
    }

    # Parental status adjustment (minor penalty for mothers/fathers due to labor market bias)
    PARENTAL_ADJUSTMENT = {
        ParentalStatus.NO_CHILDREN: 1.0,
        ParentalStatus.PARENT: 0.97,   # ~3% penalty observed for parents (esp mothers)
    }

    # Disability status adjustment
    DISABILITY_ADJUSTMENT = {
        DisabilityStatus.NO_DISABILITY: 1.0,
        DisabilityStatus.HAS_DISABILITY: 0.80,   # ~20% gap persists
    }

    # Career gap adjustment
    CAREER_GAP_ADJUSTMENT = {
        CareerGap.NO_GAP: 1.0,
        CareerGap.SHORT_GAP: 0.95,      # ~5% penalty for short gaps
        CareerGap.EXTENDED_GAP: 0.85,   # ~15% penalty for extended gaps
    }

    def evaluate(self, person: Person) -> float:
        base = self.INDUSTRY_BASE.get(person.industry_sector, 50000)

        exp_mult = self.EXPERIENCE_MULTIPLIER.get(person.experience_level, 1.0)
        edu_mult = self.EDUCATION_MULTIPLIER.get(person.education_level, 1.0)
        emp_mult = self.EMPLOYMENT_MULTIPLIER.get(person.employment_type, 1.0)
        gender_mult = self.GENDER_ADJUSTMENT.get(person.gender, 1.0)
        eth_mult = self.ETHNICITY_ADJUSTMENT.get(person.ethnicity, 1.0)
        age_mult = self.AGE_ADJUSTMENT.get(person.age_range, 1.0)
        parent_mult = self.PARENTAL_ADJUSTMENT.get(person.parental_status, 1.0)
        dis_mult = self.DISABILITY_ADJUSTMENT.get(person.disability_status, 1.0)
        gap_mult = self.CAREER_GAP_ADJUSTMENT.get(person.career_gap, 1.0)

        compensation = (
            base *
            exp_mult *
            edu_mult *
            emp_mult *
            gender_mult *
            eth_mult *
            age_mult *
            parent_mult *
            dis_mult *
            gap_mult
        )

        # Clamp to reasonable US salary range (minimum wage to high-end professional)
        compensation = max(18000, min(compensation, 350000))
        
        return round(compensation, -2)   # Round to nearest $100

# Example usage:
# evaluator = MarketCompensationEvaluator()
# estimate = evaluator.evaluate(Person(
#     gender=Gender.FEMALE,
#     ethnicity=Ethnicity.ASIAN,
#     age_range=AgeRange.AGE_35_44,
#     education_level=EducationLevel.ADVANCED,
#     experience_level=ExperienceLevel.SENIOR,
#     industry_sector=IndustrySector.INFORMATION_TECHNOLOGY,
#     employment_type=EmploymentType.FULL_TIME_PERMANENT,
#     parental_status=ParentalStatus.PARENT,
#     disability_status=DisabilityStatus.NO_DISABILITY,
#     career_gap=CareerGap.NO_GAP
# ))
# print(estimate)