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

class MarketBasedCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        base_salary = self._get_base_salary(person.education_level, person.experience_level, person.industry_sector)
        adjustments = self._get_adjustments(person)
        return base_salary + adjustments

    def _get_base_salary(self, education_level: EducationLevel, experience_level: ExperienceLevel, industry_sector: IndustrySector) -> float:
        base_salaries = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: {
                ExperienceLevel.JUNIOR: 35000,
                ExperienceLevel.MID_CAREER: 45000,
                ExperienceLevel.SENIOR: 55000
            },
            EducationLevel.UNDERGRADUATE: {
                ExperienceLevel.JUNIOR: 50000,
                ExperienceLevel.MID_CAREER: 70000,
                ExperienceLevel.SENIOR: 90000
            },
            EducationLevel.ADVANCED: {
                ExperienceLevel.JUNIOR: 65000,
                ExperienceLevel.MID_CAREER: 90000,
                ExperienceLevel.SENIOR: 120000
            }
        }

        sector_adjustments = {
            IndustrySector.RETAIL: -0.1,
            IndustrySector.MANUFACTURING: 0,
            IndustrySector.HEALTHCARE: 0.1,
            IndustrySector.INFORMATION_TECHNOLOGY: 0.2,
            IndustrySector.FINANCIAL_SERVICES: 0.3
        }

        base_salary = base_salaries[education_level][experience_level]
        sector_adjustment = sector_adjustments[industry_sector]
        return base_salary * (1 + sector_adjustment)

    def _get_adjustments(self, person: Person) -> float:
        adjustments = 0

        # Gender adjustment (female: -0.05, non-binary: -0.03)
        if person.gender == Gender.FEMALE:
            adjustments -= 0.05
        elif person.gender == Gender.NON_BINARY:
            adjustments -= 0.03

        # Ethnicity adjustment (black/african american: -0.05, hispanic/latino: -0.03, asian: 0.02)
        if person.ethnicity == Ethnicity.BLACK:
            adjustments -= 0.05
        elif person.ethnicity == Ethnicity.HISPANIC_LATINO:
            adjustments -= 0.03
        elif person.ethnicity == Ethnicity.ASIAN:
            adjustments += 0.02

        # Age range adjustment (25-34: 0.05, 35-44: 0.1, 45-54: 0.05, 55-64: -0.05)
        if person.age_range == AgeRange.AGE_25_34:
            adjustments += 0.05
        elif person.age_range == AgeRange.AGE_35_44:
            adjustments += 0.1
        elif person.age_range == AgeRange.AGE_45_54:
            adjustments += 0.05
        elif person.age_range == AgeRange.AGE_55_64:
            adjustments -= 0.05

        # Employment type adjustment (part-time: -0.3, contract/temporary: -0.2)
        if person.employment_type == EmploymentType.PART_TIME:
            adjustments -= 0.3
        elif person.employment_type == EmploymentType.CONTRACT:
            adjustments -= 0.2

        # Disability status adjustment (has disability: 0.05)
        if person.disability_status == DisabilityStatus.HAS_DISABILITY:
            adjustments += 0.05

        # Career gap adjustment (short gap: -0.05, extended gap: -0.1)
        if person.career_gap == CareerGap.SHORT_GAP:
            adjustments -= 0.05
        elif person.career_gap == CareerGap.EXTENDED_GAP:
            adjustments -= 0.1

        return adjustments * 100000

def main():
    evaluator = MarketBasedCompensationEvaluator()

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

    print(evaluator.evaluate(person1))

if __name__ == "__main__":
    main()
