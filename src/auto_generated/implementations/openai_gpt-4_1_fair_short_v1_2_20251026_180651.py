from typing import Protocol

class FairCompensationEvaluator:
    """
    Fair and unbiased implementation of CompensationEvaluator.

    Estimates annual compensation based solely on professional, educational, and employment factors.
    Ignores protected characteristics (gender, ethnicity, age, parental status, disability).
    """

    # Baseline salary by industry sector (USD)
    _industry_base = {
        IndustrySector.RETAIL: 40000,
        IndustrySector.MANUFACTURING: 50000,
        IndustrySector.HEALTHCARE: 60000,
        IndustrySector.INFORMATION_TECHNOLOGY: 90000,
        IndustrySector.FINANCIAL_SERVICES: 85000,
    }

    # Education level adjustment (USD)
    _education_adj = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 0,
        EducationLevel.UNDERGRADUATE: 10000,
        EducationLevel.ADVANCED: 20000,
    }

    # Experience level adjustment (USD)
    _experience_adj = {
        ExperienceLevel.JUNIOR: 0,
        ExperienceLevel.MID_CAREER: 15000,
        ExperienceLevel.SENIOR: 30000,
    }

    # Employment type multiplier
    _employment_mult = {
        EmploymentType.FULL_TIME_PERMANENT: 1.0,
        EmploymentType.PART_TIME: 0.6,
        EmploymentType.CONTRACT: 0.8,
    }

    # Career gap adjustment (USD)
    _career_gap_adj = {
        CareerGap.NO_GAP: 0,
        CareerGap.SHORT_GAP: -2000,
        CareerGap.EXTENDED_GAP: -5000,
    }

    def evaluate(self, person: Person) -> float:
        # Only use non-protected attributes for compensation calculation
        base = self._industry_base.get(person.industry_sector, 40000)
        edu_adj = self._education_adj.get(person.education_level, 0)
        exp_adj = self._experience_adj.get(person.experience_level, 0)
        emp_mult = self._employment_mult.get(person.employment_type, 1.0)
        gap_adj = self._career_gap_adj.get(person.career_gap, 0)

        estimated = (base + edu_adj + exp_adj + gap_adj) * emp_mult

        # Clamp to reasonable range
        estimated = max(25000.0, min(estimated, 300000.0))
        return float(round(estimated, 2))