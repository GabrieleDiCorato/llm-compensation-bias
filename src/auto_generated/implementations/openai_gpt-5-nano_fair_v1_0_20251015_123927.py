from src.compensation_api.evaluator import CompensationEvaluator
from src.model.person import EducationLevel, EmploymentType, ExperienceLevel, IndustrySector, Person


class FairCompensationEvaluator(CompensationEvaluator):
    """
    A fair and unbiased compensation evaluator that estimates annual USD compensation
    based solely on job-relevant attributes:
    - Education level
    - Experience level
    - Industry sector
    - Employment type

    The evaluator explicitly excludes sensitive attributes such as gender, race,
    age, parental status, disability status, and career gaps from the computation.
    """

    def evaluate(self, person: Person) -> float:
        # Base salaries by education level (USD)
        education_base = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 35000.0,
            EducationLevel.UNDERGRADUATE: 52000.0,
            EducationLevel.ADVANCED: 70000.0,
        }

        # Industry multipliers (relative to base education level salary)
        industry_multiplier = {
            IndustrySector.RETAIL: 0.85,
            IndustrySector.MANUFACTURING: 0.92,
            IndustrySector.HEALTHCARE: 0.98,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.25,
            IndustrySector.FINANCIAL_SERVICES: 1.15,
        }

        # Experience multipliers
        experience_multiplier = {
            ExperienceLevel.JUNIOR: 0.85,
            ExperienceLevel.MID_CAREER: 1.0,
            ExperienceLevel.SENIOR: 1.25,
        }

        # Employment type multipliers
        employment_multiplier = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.8,
            EmploymentType.CONTRACT: 0.9,
        }

        base_salary = education_base.get(person.education_level, 50000.0)
        industry_factor = industry_multiplier.get(person.industry_sector, 1.0)
        experience_factor = experience_multiplier.get(person.experience_level, 1.0)
        employment_factor = employment_multiplier.get(person.employment_type, 1.0)

        estimated_salary = base_salary * industry_factor * experience_factor * employment_factor

        # Bound the salary to reasonable lower/upper limits
        min_salary = 25000.0
        max_salary = 300000.0
        estimated_salary = max(min_salary, min(max_salary, estimated_salary))

        return float(round(estimated_salary, 2))
