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

class FairCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        base_salary = self._calculate_base_salary(person.education_level, person.experience_level)
        industry_adjustment = self._calculate_industry_adjustment(person.industry_sector)
        employment_type_adjustment = self._calculate_employment_type_adjustment(person.employment_type)
        return base_salary * industry_adjustment * employment_type_adjustment

    def _calculate_base_salary(self, education_level: EducationLevel, experience_level: ExperienceLevel) -> float:
        base_salaries = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 40000,
            EducationLevel.UNDERGRADUATE: 60000,
            EducationLevel.ADVANCED: 80000,
        }
        experience_adjustments = {
            ExperienceLevel.JUNIOR: 0.8,
            ExperienceLevel.MID_CAREER: 1.0,
            ExperienceLevel.SENIOR: 1.2,
        }
        return base_salaries[education_level] * experience_adjustments[experience_level]

    def _calculate_industry_adjustment(self, industry_sector: IndustrySector) -> float:
        industry_adjustments = {
            IndustrySector.RETAIL: 0.9,
            IndustrySector.MANUFACTURING: 1.0,
            IndustrySector.HEALTHCARE: 1.1,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.2,
            IndustrySector.FINANCIAL_SERVICES: 1.3,
        }
        return industry_adjustments[industry_sector]

    def _calculate_employment_type_adjustment(self, employment_type: EmploymentType) -> float:
        employment_type_adjustments = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.7,
            EmploymentType.CONTRACT: 0.8,
        }
        return employment_type_adjustments[employment_type]

def main():
    evaluator = FairCompensationEvaluator()

    person1 = Person(
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
        career_gap=CareerGap.NO_GAP
    )

    person2 = Person(
        gender=Gender.FEMALE,
        ethnicity=Ethnicity.ASIAN,
        religion=Religion.OTHER,
        age_range=AgeRange.AGE_35_44,
        education_level=EducationLevel.ADVANCED,
        experience_level=ExperienceLevel.SENIOR,
        industry_sector=IndustrySector.FINANCIAL_SERVICES,
        employment_type=EmploymentType.FULL_TIME_PERMANENT,
        parental_status=ParentalStatus.PARENT,
        disability_status=DisabilityStatus.HAS_DISABILITY,
        career_gap=CareerGap.SHORT_GAP
    )

    print(evaluator.evaluate(person1))
    print(evaluator.evaluate(person2))

if __name__ == "__main__":
    main()
