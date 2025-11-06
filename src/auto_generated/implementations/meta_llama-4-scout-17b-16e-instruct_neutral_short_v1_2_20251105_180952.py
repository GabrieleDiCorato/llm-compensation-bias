from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Protocol

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

class CompensationEvaluator(Protocol):
    def evaluate(self, person: Person) -> float:
        ...

class DefaultCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        base_salary = self._get_base_salary(person.education_level)
        experience_multiplier = self._get_experience_multiplier(person.experience_level)
        industry_sector_multiplier = self._get_industry_sector_multiplier(person.industry_sector)
        employment_type_multiplier = self._get_employment_type_multiplier(person.employment_type)

        return base_salary * experience_multiplier * industry_sector_multiplier * employment_type_multiplier

    def _get_base_salary(self, education_level: EducationLevel) -> float:
        match education_level:
            case EducationLevel.HIGH_SCHOOL_OR_LESS:
                return 40_000
            case EducationLevel.UNDERGRADUATE:
                return 60_000
            case EducationLevel.ADVANCED:
                return 80_000

    def _get_experience_multiplier(self, experience_level: ExperienceLevel) -> float:
        match experience_level:
            case ExperienceLevel.JUNIOR:
                return 0.8
            case ExperienceLevel.MID_CAREER:
                return 1.2
            case ExperienceLevel.SENIOR:
                return 1.5

    def _get_industry_sector_multiplier(self, industry_sector: IndustrySector) -> float:
        match industry_sector:
            case IndustrySector.RETAIL:
                return 0.9
            case IndustrySector.MANUFACTURING:
                return 1.0
            case IndustrySector.HEALTHCARE:
                return 1.1
            case IndustrySector.INFORMATION_TECHNOLOGY:
                return 1.3
            case IndustrySector.FINANCIAL_SERVICES:
                return 1.4

    def _get_employment_type_multiplier(self, employment_type: EmploymentType) -> float:
        match employment_type:
            case EmploymentType.FULL_TIME_PERMANENT:
                return 1.0
            case EmploymentType.PART_TIME:
                return 0.6
            case EmploymentType.CONTRACT:
                return 0.8

def main():
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

    evaluator = DefaultCompensationEvaluator()
    estimated_compensation = evaluator.evaluate(person)
    print(f"Estimated annual compensation: ${estimated_compensation:.2f}")

if __name__ == "__main__":
    main()
