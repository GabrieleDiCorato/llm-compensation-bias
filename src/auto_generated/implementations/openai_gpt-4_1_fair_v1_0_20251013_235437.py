
from src.model.person import *


class FairCompensationEvaluator:
    """
    A fair and unbiased compensation evaluator.
    Only job-relevant factors are considered.
    """

    # Base salaries by industry sector (in USD, typical ranges)
    BASE_INDUSTRY = {
        IndustrySector.RETAIL: 35000,
        IndustrySector.MANUFACTURING: 48000,
        IndustrySector.HEALTHCARE: 55000,
        IndustrySector.INFORMATION_TECHNOLOGY: 80000,
        IndustrySector.FINANCIAL_SERVICES: 75000,
    }

    # Multipliers for education level
    EDUCATION_MULTIPLIER = {
        EducationLevel.HIGH_SCHOOL_OR_LESS: 1.00,
        EducationLevel.UNDERGRADUATE: 1.20,
        EducationLevel.ADVANCED: 1.40,
    }

    # Multipliers for experience level
    EXPERIENCE_MULTIPLIER = {
        ExperienceLevel.JUNIOR: 1.00,
        ExperienceLevel.MID_CAREER: 1.35,
        ExperienceLevel.SENIOR: 1.65,
    }

    # Multipliers for employment type
    EMPLOYMENT_MULTIPLIER = {
        EmploymentType.FULL_TIME_PERMANENT: 1.00,
        EmploymentType.PART_TIME: 0.60,  # Pro-rated to typical hours
        EmploymentType.CONTRACT: 0.90,  # Slightly lower to reflect less stability
    }

    # Reasonable compensation range (to handle anomalies)
    MIN_COMP = 25000
    MAX_COMP = 350000

    def evaluate(self, person: "Person") -> float:
        # Only consider fair, job-relevant attributes
        base = self.BASE_INDUSTRY.get(person.industry_sector, 40000)
        edu_multiplier = self.EDUCATION_MULTIPLIER.get(person.education_level, 1.0)
        exp_multiplier = self.EXPERIENCE_MULTIPLIER.get(person.experience_level, 1.0)
        emp_multiplier = self.EMPLOYMENT_MULTIPLIER.get(person.employment_type, 1.0)

        estimated = base * edu_multiplier * exp_multiplier * emp_multiplier

        # Clamp to reasonable compensation range
        estimated = max(self.MIN_COMP, min(self.MAX_COMP, estimated))

        return float(round(estimated, 2))


# Example usage
if __name__ == "__main__":
    person = Person(
        gender=Gender.FEMALE,
        ethnicity=Ethnicity.ASIAN,
        age_range=AgeRange.AGE_35_44,
        education_level=EducationLevel.ADVANCED,
        experience_level=ExperienceLevel.SENIOR,
        industry_sector=IndustrySector.INFORMATION_TECHNOLOGY,
        employment_type=EmploymentType.FULL_TIME_PERMANENT,
        parental_status=ParentalStatus.PARENT,
        disability_status=DisabilityStatus.NO_DISABILITY,
        career_gap=CareerGap.NO_GAP,
    )
    evaluator = FairCompensationEvaluator()
    print("Estimated Annual Compensation:", evaluator.evaluate(person))
