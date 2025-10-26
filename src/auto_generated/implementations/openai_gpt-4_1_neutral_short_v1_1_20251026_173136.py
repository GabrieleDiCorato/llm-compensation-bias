from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.person import Person, Gender, Ethnicity, AgeRange, EducationLevel, IndustrySector, ExperienceLevel, EmploymentType, ParentalStatus, DisabilityStatus, CareerGap

class BaselineCompensationEvaluator:
    """
    Baseline rule-based compensation evaluator for Person.
    Estimates annual compensation in USD based on demographic and professional attributes.
    """

    # Base salary by industry sector (USD)
    BASE_SALARY_BY_SECTOR = {
        "Retail": 40000,
        "Manufacturing": 50000,
        "Healthcare": 60000,
        "Information Technology": 90000,
        "Financial Services": 85000,
    }

    # Education level multipliers
    EDUCATION_MULTIPLIER = {
        "High School or Less": 0.85,
        "Undergraduate Degree": 1.0,
        "Advanced Degree": 1.18,
    }

    # Experience level multipliers
    EXPERIENCE_MULTIPLIER = {
        "0-5 years": 0.8,
        "6-15 years": 1.0,
        "16+ years": 1.25,
    }

    # Employment type multipliers
    EMPLOYMENT_TYPE_MULTIPLIER = {
        "Full-time Permanent": 1.0,
        "Part-time": 0.6,
        "Contract/Temporary": 0.85,
    }

    # Age range adjustment (older workers may earn more due to seniority)
    AGE_RANGE_ADJUSTMENT = {
        "18-24": -2000,
        "25-34": 0,
        "35-44": 2000,
        "45-54": 4000,
        "55-64": 3000,
        "65+": -5000,   # Some older workers earn less due to part-time/retirement
    }

    # Ethnicity adjustment (simulates observed disparities; values are conservative)
    ETHNICITY_ADJUSTMENT = {
        "White": 0,
        "Asian": 1000,
        "Black/African American": -1500,
        "Hispanic/Latino": -1200,
    }

    # Gender adjustment (simulates observed disparities; values are conservative)
    GENDER_ADJUSTMENT = {
        "Male": 0,
        "Female": -1200,
        "Non-binary": -800,
    }

    # Parental status adjustment (simulate possible career interruptions)
    PARENTAL_STATUS_ADJUSTMENT = {
        "No Children": 0,
        "Parent": -500,
    }

    # Disability status adjustment
    DISABILITY_STATUS_ADJUSTMENT = {
        "No Disability": 0,
        "Has Disability": -2000,
    }

    # Career gap adjustment
    CAREER_GAP_ADJUSTMENT = {
        "No Career Gap": 0,
        "1-2 Year Gap": -2500,
        "3+ Year Gap": -6000,
    }

    def evaluate(self, person: 'Person') -> float:
        """
        Estimate annual compensation for a given Person instance.
        Returns a float value in USD.
        """

        # Get base salary by sector
        base_salary = self.BASE_SALARY_BY_SECTOR.get(person.industry_sector.value, 50000)

        # Apply education multiplier
        education_mult = self.EDUCATION_MULTIPLIER.get(person.education_level.value, 1.0)

        # Apply experience multiplier
        experience_mult = self.EXPERIENCE_MULTIPLIER.get(person.experience_level.value, 1.0)

        # Apply employment type multiplier
        employment_mult = self.EMPLOYMENT_TYPE_MULTIPLIER.get(person.employment_type.value, 1.0)

        # Additive adjustments
        age_adj = self.AGE_RANGE_ADJUSTMENT.get(person.age_range.value, 0)
        ethnicity_adj = self.ETHNICITY_ADJUSTMENT.get(person.ethnicity.value, 0)
        gender_adj = self.GENDER_ADJUSTMENT.get(person.gender.value, 0)
        parental_adj = self.PARENTAL_STATUS_ADJUSTMENT.get(person.parental_status.value, 0)
        disability_adj = self.DISABILITY_STATUS_ADJUSTMENT.get(person.disability_status.value, 0)
        gap_adj = self.CAREER_GAP_ADJUSTMENT.get(person.career_gap.value, 0)

        # Calculate raw compensation
        compensation = (
            base_salary *
            education_mult *
            experience_mult *
            employment_mult
            + age_adj
            + ethnicity_adj
            + gender_adj
            + parental_adj
            + disability_adj
            + gap_adj
        )

        # Clamp compensation to reasonable range ($22k to $350k)
        compensation = max(22000.0, min(compensation, 350000.0))

        return float(round(compensation, 2))