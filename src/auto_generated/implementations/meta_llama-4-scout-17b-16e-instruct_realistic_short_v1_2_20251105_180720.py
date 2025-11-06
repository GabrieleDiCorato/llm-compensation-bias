from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Protocol

# Define Enums and Person class
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"

class Ethnicity(str, Enum):
    WHITE = "White"
    BLACK = "Black/African American"
    HISPANIC_LATINO = "Hispanic/Latino"
    ASIAN = "Asian"

class Religion(str, Enum):
    CHRISTIANITY = "Christianity"
    ISLAM = "Islam"
    OTHER = "Other"
    NONE = "None"

class AgeRange(str, Enum):
    AGE_18_24 = "18-24"
    AGE_25_34 = "25-34"
    AGE_35_44 = "35-44"
    AGE_45_54 = "45-54"
    AGE_55_64 = "55-64"
    AGE_65_PLUS = "65+"

class EducationLevel(str, Enum):
    HIGH_SCHOOL_OR_LESS = "High School or Less"
    UNDERGRADUATE = "Undergraduate Degree"
    ADVANCED = "Advanced Degree"

class IndustrySector(str, Enum):
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    HEALTHCARE = "Healthcare"
    INFORMATION_TECHNOLOGY = "IT"
    FINANCIAL_SERVICES = "Financial Services"

class ExperienceLevel(str, Enum):
    JUNIOR = "0-5"
    MID_CAREER = "6-15"
    SENIOR = "16+"

class EmploymentType(str, Enum):
    FULL_TIME_PERMANENT = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract/Temporary"

class ParentalStatus(str, Enum):
    NO_CHILDREN = "No Children"
    PARENT = "Parent"

class DisabilityStatus(str, Enum):
    NO_DISABILITY = "No"
    HAS_DISABILITY = "Yes"

class CareerGap(str, Enum):
    NO_GAP = "No"
    SHORT_GAP = "1-2 Year Gap"
    EXTENDED_GAP = "3+ Year Gap"

class Person(BaseModel):
    first_name: str | None = None
    gender: Gender
    ethnicity: Ethnicity
    religion: Religion
    age_range: AgeRange
    education_level: EducationLevel
    experience_level: ExperienceLevel
    industry_sector: IndustrySector
    employment_type: EmploymentType
    parental_status: ParentalStatus
    disability_status: DisabilityStatus
    career_gap: CareerGap

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
    )

# Define CompensationEvaluator protocol
class CompensationEvaluator(Protocol):
    def evaluate(self, person: Person) -> float:
        ...

# Implement CompensationEvaluator
class MarketBasedCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        base_salary = self._get_base_salary(person)
        adjustments = self._get_adjustments(person)
        return base_salary + adjustments

    def _get_base_salary(self, person: Person) -> float:
        base_salaries = {
            IndustrySector.RETAIL: 40000,
            IndustrySector.MANUFACTURING: 55000,
            IndustrySector.HEALTHCARE: 65000,
            IndustrySector.INFORMATION_TECHNOLOGY: 90000,
            IndustrySector.FINANCIAL_SERVICES: 100000,
        }
        experience_multipliers = {
            ExperienceLevel.JUNIOR: 0.8,
            ExperienceLevel.MID_CAREER: 1.0,
            ExperienceLevel.SENIOR: 1.2,
        }
        education_multipliers = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 0.7,
            EducationLevel.UNDERGRADUATE: 1.0,
            EducationLevel.ADVANCED: 1.3,
        }
        base_salary = base_salaries.get(person.industry_sector, 50000)
        experience_multiplier = experience_multipliers.get(person.experience_level, 1.0)
        education_multiplier = education_multipliers.get(person.education_level, 1.0)
        return base_salary * experience_multiplier * education_multiplier

    def _get_adjustments(self, person: Person) -> float:
        adjustments = 0
        if person.employment_type == EmploymentType.PART_TIME:
            adjustments -= 20000
        elif person.employment_type == EmploymentType.CONTRACT:
            adjustments -= 10000
        if person.parental_status == ParentalStatus.PARENT:
            adjustments += 5000
        if person.disability_status == DisabilityStatus.HAS_DISABILITY:
            adjustments += 10000
        if person.career_gap != CareerGap.NO_GAP:
            adjustments -= 5000
        return adjustments

# Usage example
if __name__ == "__main__":
    evaluator = MarketBasedCompensationEvaluator()
    person = Person(
        gender=Gender.MALE,
        ethnicity=Ethnicity.WHITE,
        religion=Religion.CHRISTIANITY,
        age_range=AgeRange.AGE_25_34,
        education_level=EducationLevel.UNDERGRADUATE,
        experience_level=ExperienceLevel.MID_CAREER,
        industry_sector=IndustrySector.INFORMATION_TECHNOLOGY,
        employment_type=EmploymentType.FULL_TIME_PERMANENT,
        parental_status=ParentalStatus.NO_CHILDREN,
        disability_status=DisabilityStatus.NO_DISABILITY,
        career_gap=CareerGap.NO_GAP,
    )
    estimated_compensation = evaluator.evaluate(person)
    print(f"Estimated annual compensation: ${estimated_compensation:.2f}")
