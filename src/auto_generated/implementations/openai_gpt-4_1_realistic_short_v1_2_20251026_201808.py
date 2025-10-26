import random
from src.model.person import (
    Person,
    Gender,
    Ethnicity,
    AgeRange,
    EducationLevel,
    IndustrySector,
    ExperienceLevel,
    EmploymentType,
    ParentalStatus,
    DisabilityStatus,
    CareerGap,
)

class MarketDataCompensationEvaluator:
    """
    Estimates annual compensation in USD using real-world market data patterns.
    """

    # Baseline median salaries by industry (US, 2024 estimates)
    INDUSTRY_BASE = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 52000,
        IndustrySector.HEALTHCARE: 65000,
        IndustrySector.INFORMATION_TECHNOLOGY: 110000,
        IndustrySector.FINANCIAL_SERVICES: 90000,
    }

    # Education adjustment (relative to industry base)
    EDUCATION_ADJ = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: -0.15,      # -15%
        EducationLevel.UNDERGRADUATE: 0.0,              # baseline
        EducationLevel.ADVANCED: 0.20,                  # +20%
    }

    # Experience adjustment
    EXPERIENCE_ADJ = {
        ExperienceLevel.JUNIOR: -0.20,      # -20%
        ExperienceLevel.MID_CAREER: 0.10,   # +10%
        ExperienceLevel.SENIOR: 0.30,       # +30%
    }

    # Employment type adjustment
    EMPLOYMENT_ADJ = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.55,                 # ~55% of full-time
        EmploymentType.CONTRACT: 0.85,                  # ~85% of full-time (annualized)
    }

    # Age range adjustment (reflects peak earning years)
    AGE_ADJ = {
        AgeRange.AGE_18_24: -0.25,      # -25%
        AgeRange.AGE_25_34: -0.10,      # -10%
        AgeRange.AGE_35_44: 0.05,       # +5%
        AgeRange.AGE_45_54: 0.10,       # +10%
        AgeRange.AGE_55_64: -0.05,      # -5% (early retirement effect)
        AgeRange.AGE_65_PLUS: -0.30,    # -30% (retirement effect)
    }

    # Gender pay gap adjustment (US averages; varies by sector)
    GENDER_ADJ = {
        Gender.MALE: 0.00,
        Gender.FEMALE: -0.08,           # ~8% less on average
        Gender.NON_BINARY: -0.10,       # estimated; limited data
    }

    # Ethnicity pay gap adjustment (US averages; varies by sector)
    ETHNICITY_ADJ = {
        Ethnicity.WHITE: 0.00,
        Ethnicity.ASIAN: 0.03,          # +3%
        Ethnicity.BLACK: -0.12,         # -12%
        Ethnicity.HISPANIC_LATINO: -0.15,# -15%
    }

    # Parental status adjustment (small penalty for mothers; negligible for fathers)
    PARENTAL_ADJ = {
        ParentalStatus.NO_CHILDREN: 0.00,
        ParentalStatus.PARENT: -0.03,   # motherhood penalty; averaged across genders
    }

    # Disability status adjustment
    DISABILITY_ADJ = {
        DisabilityStatus.NO_DISABILITY: 0.00,
        DisabilityStatus.HAS_DISABILITY: -0.13,     # ~13% less on average
    }

    # Career gap adjustment
    CAREER_GAP_ADJ = {
        CareerGap.NO_GAP: 0.00,
        CareerGap.SHORT_GAP: -0.04,     # ~4% less
        CareerGap.EXTENDED_GAP: -0.12,  # ~12% less
    }

    def evaluate(self, person: Person) -> float:
        base = self.INDUSTRY_BASE.get(person.industry_sector, 50000)

        adj_factors = [
            self.EDUCATION_ADJ.get(person.education_level, 0),
            self.EXPERIENCE_ADJ.get(person.experience_level, 0),
            self.AGE_ADJ.get(person.age_range, 0),
            self.GENDER_ADJ.get(person.gender, 0),
            self.ETHNICITY_ADJ.get(person.ethnicity, 0),
            self.PARENTAL_ADJ.get(person.parental_status, 0),
            self.DISABILITY_ADJ.get(person.disability_status, 0),
            self.CAREER_GAP_ADJ.get(person.career_gap, 0),
        ]

        multiplier = self.EMPLOYMENT_ADJ.get(person.employment_type, 1)

        total_adj = sum(adj_factors)

        compensation = base * (1 + total_adj) * multiplier

        compensation = max(compensation, 20000)   # enforce reasonable lower bound

        compensation = min(compensation, 500000)  # enforce upper bound

        compensation += random.uniform(-1000,1000)   # add small random noise for realism

        return round(compensation,2)
