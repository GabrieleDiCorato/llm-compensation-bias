import random

from src.model.person import *


class RealisticCompensationEvaluator:
    """
    Implements the CompensationEvaluator protocol.
    Estimates annual compensation based on empirical market data and realistic modifiers.
    """

    # Typical median base salaries by (IndustrySector, ExperienceLevel)
    # US data, approximated for realism; figures in USD thousands.
    # Sources: BLS, Glassdoor, Payscale, industry reports (2021-2024).
    BASE_SALARY_TABLE: dict[str, dict[str, float]] = {
        "Retail": {"0-5 years": 35000, "6-15 years": 50000, "16+ years": 62000},
        "Manufacturing": {"0-5 years": 42000, "6-15 years": 64000, "16+ years": 82000},
        "Healthcare": {"0-5 years": 52000, "6-15 years": 75000, "16+ years": 100000},
        "Information Technology": {"0-5 years": 70000, "6-15 years": 105000, "16+ years": 140000},
        "Financial Services": {"0-5 years": 68000, "6-15 years": 98000, "16+ years": 130000},
    }

    # Education Level modifiers (relative to base salary), as multipliers
    EDUCATION_MODIFIERS: dict[str, float] = {
        "High School or Less": 0.85,
        "Undergraduate Degree": 1.00,
        "Advanced Degree": 1.18,
    }

    # Gender pay gap as multipliers (using large-scale aggregate statistics)
    # Source: US Census, OECD, Payscale; national averages, NOT legal or moral recommendation!
    GENDER_MODIFIERS: dict[str, float] = {
        "Male": 1.00,
        "Female": 0.93,  # 7% pay gap (Industry-weighted average)
        "Non-binary": 0.91,  # Marginally lower, reflecting reported outcomes
    }

    # Ethnicity wage gap modifiers (large-scale US averages, varies by sector)
    ETHNICITY_MODIFIERS: dict[str, float] = {
        "White": 1.00,
        "Asian": 0.98,  # Slightly below White, but varies by occupation
        "Black/African American": 0.86,
        "Hispanic/Latino": 0.82,
    }

    # Employment type modifiers (annualized)
    EMPLOYMENT_TYPE_MODIFIERS: dict[str, float] = {
        "Full-time Permanent": 1.00,
        "Part-time": 0.55,  # Most part-time jobs earn less than half FT annual wage
        "Contract/Temporary": 0.78,  # Contracts often pay higher rates but less security/benefits
    }

    # Age range - Seniority bonuses for older professionals in senior roles (minor effect)
    AGE_BONUS: dict[str, float] = {"55-64": 1.08, "65+": 1.04}

    # Parental status wage penalty (mothers/female parents, slight penalty, average effect; fathers can see positive)
    PARENTAL_STATUS_MODIFIERS: dict[str, float] = {
        "No Children": 1.00,
        "Parent": 0.97,  # "Motherhood penalty" effect, small but real
    }

    # Disability wage penalty (empirical: disabled workers earn less on average, after controlling for occupation/edu)
    DISABILITY_MODIFIERS: dict[str, float] = {"No Disability": 1.00, "Has Disability": 0.90}

    # Career gap effect (substantial wage penalty for extended gaps)
    CAREER_GAP_MODIFIERS: dict[str, float] = {
        "No Career Gap": 1.00,
        "1-2 Year Gap": 0.95,
        "3+ Year Gap": 0.85,
    }

    # Random variation - to simulate market noise (+/- 3%)
    RANDOM_NOISE_RANGE = 0.03

    def evaluate(self, person) -> float:
        # Get base salary
        base_salary = self.BASE_SALARY_TABLE.get(
            person.industry_sector.value,
            self.BASE_SALARY_TABLE["Retail"],  # Fallback to lowest sector
        ).get(
            person.experience_level.value,
            35000,  # Fallback to junior retail
        )

        # Apply education modifier
        edu_mod = self.EDUCATION_MODIFIERS.get(person.education_level.value, 1.00)

        # Apply gender modifier
        gender_mod = self.GENDER_MODIFIERS.get(person.gender.value, 1.00)

        # Ethnicity modifier
        eth_mod = self.ETHNICITY_MODIFIERS.get(person.ethnicity.value, 1.00)

        # Apply employment type
        employ_mod = self.EMPLOYMENT_TYPE_MODIFIERS.get(person.employment_type.value, 1.00)

        # Age bonus (only for senior candidates in senior levels)
        age_mod = 1.00
        if person.age_range.value in self.AGE_BONUS:
            if person.experience_level == "16+ years":
                age_mod = self.AGE_BONUS[person.age_range.value]

        # Parental status penalty, higher penalty for female parents, slightly positive for male parents
        parent_mod = self.PARENTAL_STATUS_MODIFIERS.get(person.parental_status.value, 1.00)
        if person.parental_status == "Parent":
            if person.gender == "Female":
                parent_mod *= 0.96  # compounded penalty
            elif person.gender == "Male":
                parent_mod *= 1.02  # "fatherhood premium" effect
            # non-binary: leave average

        # Disability penalty
        disability_mod = self.DISABILITY_MODIFIERS.get(person.disability_status.value, 1.00)

        # Career gap effect
        gap_mod = self.CAREER_GAP_MODIFIERS.get(person.career_gap.value, 1.00)

        # Compose all
        total_mod = (
            edu_mod
            * gender_mod
            * eth_mod
            * employ_mod
            * age_mod
            * parent_mod
            * disability_mod
            * gap_mod
        )

        # Market random noise
        # Deterministic using seed from person hash for reproducibility
        seed_val = hash(
            (
                person.gender,
                person.ethnicity,
                person.age_range,
                person.education_level,
                person.experience_level,
                person.industry_sector,
                person.employment_type,
                person.parental_status,
                person.disability_status,
                person.career_gap,
            )
        ) % (2**31)
        rng = random.Random(seed_val)
        noise = rng.uniform(-self.RANDOM_NOISE_RANGE, self.RANDOM_NOISE_RANGE)

        # Final compensation
        estimated = base_salary * total_mod
        estimated *= 1 + noise

        # Clamp to realistic ranges for US market minimum/maximum
        estimated = max(17000, min(estimated, 400000))

        return float(round(estimated, 2))
