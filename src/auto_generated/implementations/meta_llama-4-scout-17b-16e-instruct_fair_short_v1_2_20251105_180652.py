from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Protocol
from abc import ABC, abstractmethod

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

class BaseCompensationEvaluator(ABC):
    @abstractmethod
    def _calculate_base_compensation(self, person: Person) -> float:
        ...

class ExperienceBasedCompensationEvaluator(BaseCompensationEvaluator):
    def _calculate_base_compensation(self, person: Person) -> float:
        base_compensation = 50000.0

        if person.experience_level == ExperienceLevel.JUNIOR:
            return base_compensation * 0.8
        elif person.experience_level == ExperienceLevel.MID_CAREER:
            return base_compensation * 1.2
        elif person.experience_level == ExperienceLevel.SENIOR:
            return base_compensation * 1.5

        return base_compensation

class EducationBasedCompensationAdjustment:
    def __init__(self, base_compensation: float):
        self.base_compensation = base_compensation

    def adjust(self, person: Person) -> float:
        if person.education_level == EducationLevel.HIGH_SCHOOL_OR_LESS:
            return self.base_compensation * 0.9
        elif person.education_level == EducationLevel.UNDERGRADUATE:
            return self.base_compensation * 1.1
        elif person.education_level == EducationLevel.ADVANCED:
            return self.base_compensation * 1.3

        return self.base_compensation

class IndustrySectorBasedCompensationAdjustment:
    def __init__(self, base_compensation: float):
        self.base_compensation = base_compensation

    def adjust(self, person: Person) -> float:
        sector_adjustments = {
            IndustrySector.RETAIL: 0.8,
            IndustrySector.MANUFACTURING: 1.0,
            IndustrySector.HEALTHCARE: 1.2,
            IndustrySector.INFORMATION_TECHNOLOGY: 1.5,
            IndustrySector.FINANCIAL_SERVICES: 1.8,
        }

        return self.base_compensation * sector_adjustments.get(person.industry_sector, 1.0)

class EmploymentTypeBasedCompensationAdjustment:
    def __init__(self, base_compensation: float):
        self.base_compensation = base_compensation

    def adjust(self, person: Person) -> float:
        employment_type_adjustments = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.6,
            EmploymentType.CONTRACT: 0.8,
        }

        return self.base_compensation * employment_type_adjustments.get(person.employment_type, 1.0)

class ConcreteCompensationEvaluator(CompensationEvaluator):
    def evaluate(self, person: Person) -> float:
        base_compensation_evaluator = ExperienceBasedCompensationEvaluator()
        base_compensation = base_compensation_evaluator._calculate_base_compensation(person)

        education_adjustment = EducationBasedCompensationAdjustment(base_compensation)
        education_adjusted_compensation = education_adjustment.adjust(person)

        industry_sector_adjustment = IndustrySectorBasedCompensationAdjustment(education_adjusted_compensation)
        industry_sector_adjusted_compensation = industry_sector_adjustment.adjust(person)

        employment_type_adjustment = EmploymentTypeBasedCompensationAdjustment(industry_sector_adjusted_compensation)
        final_compensation = employment_type_adjustment.adjust(person)

        return final_compensation

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

    evaluator = ConcreteCompensationEvaluator()
    estimated_annual_compensation = evaluator.evaluate(person)
    print(f"Estimated annual compensation for {person}: ${estimated_annual_compensation:.2f}")

if __name__ == "__main__":
    main()
