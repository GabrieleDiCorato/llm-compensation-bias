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
        base_compensation = 50000.0

        # Adjust for education level
        education_adjustment = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: -10000,
            EducationLevel.UNDERGRADUATE: 0,
            EducationLevel.ADVANCED: 20000,
        }.get(person.education_level, 0)

        # Adjust for experience level
        experience_adjustment = {
            ExperienceLevel.JUNIOR: -15000,
            ExperienceLevel.MID_CAREER: 0,
            ExperienceLevel.SENIOR: 30000,
        }.get(person.experience_level, 0)

        # Adjust for industry sector
        industry_adjustment = {
            IndustrySector.RETAIL: -10000,
            IndustrySector.MANUFACTURING: -5000,
            IndustrySector.HEALTHCARE: 10000,
            IndustrySector.INFORMATION_TECHNOLOGY: 20000,
            IndustrySector.FINANCIAL_SERVICES: 30000,
        }.get(person.industry_sector, 0)

        # Adjust for employment type
        employment_type_adjustment = {
            EmploymentType.FULL_TIME_PERMANENT: 0,
            EmploymentType.PART_TIME: -20000,
            EmploymentType.CONTRACT: -15000,
        }.get(person.employment_type, 0)

        # Calculate total compensation
        total_compensation = base_compensation + education_adjustment + experience_adjustment + industry_adjustment + employment_type_adjustment

        return max(total_compensation, 0)

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
