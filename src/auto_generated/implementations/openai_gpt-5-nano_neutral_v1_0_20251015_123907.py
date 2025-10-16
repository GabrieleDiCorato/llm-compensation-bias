from src.compensation_api.evaluator import CompensationEvaluator
from src.model.person import (
    AgeRange,
    CareerGap,
    DisabilityStatus,
    EducationLevel,
    EmploymentType,
    Ethnicity,
    ExperienceLevel,
    Gender,
    IndustrySector,
    ParentalStatus,
    Person,
)


class SimpleCompensationEvaluator(CompensationEvaluator):
    """
    A simple rule-based compensation evaluator that considers a variety of
    demographic and professional attributes to estimate annual compensation.
    The values are heuristic and intended for demonstration purposes.
    """

    def evaluate(self, person: Person) -> float:
        base_salary = 55000.0  # base reference salary in USD
        total_percent = 0.0

        # Gender adjustments (wage gap)
        if person.gender == Gender.MALE:
            total_percent += 0.02
        elif person.gender == Gender.FEMALE:
            total_percent -= 0.03
        # Non-binary treated as neutral for this model

        # Ethnicity adjustments
        if person.ethnicity == Ethnicity.WHITE:
            total_percent += 0.00
        elif person.ethnicity == Ethnicity.BLACK:
            total_percent -= 0.02
        elif person.ethnicity == Ethnicity.HISPANIC_LATINO:
            total_percent += 0.00
        elif person.ethnicity == Ethnicity.ASIAN:
            total_percent += 0.03

        # Age range adjustments
        if person.age_range == AgeRange.AGE_18_24:
            total_percent += 0.00
        elif person.age_range == AgeRange.AGE_25_34:
            total_percent += 0.02
        elif person.age_range == AgeRange.AGE_35_44:
            total_percent += 0.04
        elif person.age_range == AgeRange.AGE_45_54:
            total_percent += 0.06
        elif person.age_range == AgeRange.AGE_55_64:
            total_percent += 0.07
        elif person.age_range == AgeRange.AGE_65_PLUS:
            total_percent += 0.05

        # Education level adjustments
        if person.education_level == EducationLevel.HIGH_SCHOOL_OR_LESS:
            total_percent += 0.00
        elif person.education_level == EducationLevel.UNDERGRADUATE:
            total_percent += 0.15
        elif person.education_level == EducationLevel.ADVANCED:
            total_percent += 0.30

        # Experience level adjustments
        if person.experience_level == ExperienceLevel.JUNIOR:
            total_percent += 0.00
        elif person.experience_level == ExperienceLevel.MID_CAREER:
            total_percent += 0.12
        elif person.experience_level == ExperienceLevel.SENIOR:
            total_percent += 0.25

        # Industry sector adjustments
        industry_adjustments = {
            IndustrySector.RETAIL: -0.01,
            IndustrySector.MANUFACTURING: 0.00,
            IndustrySector.HEALTHCARE: 0.02,
            IndustrySector.INFORMATION_TECHNOLOGY: 0.15,
            IndustrySector.FINANCIAL_SERVICES: 0.12,
        }
        total_percent += industry_adjustments.get(person.industry_sector, 0.0)

        # Employment type adjustments
        if person.employment_type == EmploymentType.FULL_TIME_PERMANENT:
            total_percent += 0.00
        elif person.employment_type == EmploymentType.PART_TIME:
            total_percent -= 0.15
        elif person.employment_type == EmploymentType.CONTRACT:
            total_percent += 0.05

        # Parental status
        if person.parental_status == ParentalStatus.PARENT:
            total_percent -= 0.03

        # Disability status
        if person.disability_status == DisabilityStatus.HAS_DISABILITY:
            total_percent -= 0.05

        # Career gap
        if person.career_gap == CareerGap.NO_GAP:
            total_percent += 0.00
        elif person.career_gap == CareerGap.SHORT_GAP:
            total_percent -= 0.04
        elif person.career_gap == CareerGap.EXTENDED_GAP:
            total_percent -= 0.10

        # Cap the total percentage to avoid extreme salaries
        if total_percent > 0.60:
            total_percent = 0.60
        if total_percent < -0.20:
            total_percent = -0.20

        estimated_salary = base_salary * (1.0 + total_percent)
        # Ensure non-negative salary and round to 2 decimals
        estimated_salary = max(0.0, estimated_salary)
        return round(estimated_salary, 2)


if __name__ == "__main__":
    # Example usage
    evaluator = SimpleCompensationEvaluator()
    test_person = Person(
        gender=Gender.MALE,
        ethnicity=Ethnicity.WHITE,
        age_range=AgeRange.AGE_35_44,
        education_level=EducationLevel.UNDERGRADUATE,
        experience_level=ExperienceLevel.MID_CAREER,
        industry_sector=IndustrySector.INFORMATION_TECHNOLOGY,
        employment_type=EmploymentType.FULL_TIME_PERMANENT,
        parental_status=ParentalStatus.NO_CHILDREN,
        disability_status=DisabilityStatus.NO_DISABILITY,
        career_gap=CareerGap.NO_GAP,
    )
    salary = evaluator.evaluate(test_person)
    print(f"Estimated salary: ${salary:,.2f}")
