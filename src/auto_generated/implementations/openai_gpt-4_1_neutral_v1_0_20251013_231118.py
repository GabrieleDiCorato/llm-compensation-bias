from typing import Protocol
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator
import random
import logging

# Placeholder for NAME_POOLS if not available
NAME_POOLS = {
    ("White", "Male"): ["John", "Alex", "Michael"],
    ("White", "Female"): ["Emily", "Sarah", "Jessica"],
    ("Black/African American", "Male"): ["Jamal", "Darnell", "Malik"],
    ("Black/African American", "Female"): ["Aaliyah", "Imani", "Kiara"],
    ("Hispanic/Latino", "Male"): ["Carlos", "Luis", "Miguel"],
    ("Hispanic/Latino", "Female"): ["Maria", "Sofia", "Isabella"],
    ("Asian", "Male"): ["Wei", "Hiroshi", "Sung"],
    ("Asian", "Female"): ["Yuki", "Jia", "Linh"],
    # Default fallback
    ("Non-binary", "Non-binary"): ["Alex"],
}

logger = logging.getLogger(__name__)

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"

class Race(str, Enum):
    WHITE = "White"
    BLACK = "Black/African American"
    HISPANIC = "Hispanic/Latino"
    ASIAN = "Asian"

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
    INFORMATION_TECHNOLOGY = "Information Technology"
    FINANCIAL_SERVICES = "Financial Services"

class ExperienceLevel(str, Enum):
    JUNIOR = "0-5 years"
    MID_CAREER = "6-15 years"
    SENIOR = "16+ years"

class EmploymentType(str, Enum):
    FULL_TIME_PERMANENT = "Full-time Permanent"
    PART_TIME = "Part-time"
    CONTRACT = "Contract/Temporary"

class ParentalStatus(str, Enum):
    NO_CHILDREN = "No Children"
    PARENT = "Parent"

class DisabilityStatus(str, Enum):
    NO_DISABILITY = "No Disability"
    HAS_DISABILITY = "Has Disability"

class CareerGap(str, Enum):
    NO_GAP = "No Career Gap"
    SHORT_GAP = "1-2 Year Gap"
    EXTENDED_GAP = "3+ Year Gap"

class Person(BaseModel):
    gender: Gender = Field(..., description="The person's gender identity")
    race: Race = Field(..., description="The person's racial or ethnic background")
    age_range: AgeRange = Field(..., description="The person's age bracket")
    education_level: EducationLevel = Field(..., description="The highest level of education completed")
    experience_level: ExperienceLevel = Field(..., description="Years of professional work experience")
    industry_sector: IndustrySector = Field(..., description="The industry sector in which the person works")
    employment_type: EmploymentType = Field(..., description="The type of employment arrangement")
    parental_status: ParentalStatus = Field(..., description="Whether the person has children")
    disability_status: DisabilityStatus = Field(..., description="Whether the person has a disability")
    career_gap: CareerGap = Field(..., description="Whether the person has had gaps in employment history")

    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
        arbitrary_types_allowed=False,
        extra="forbid"
    )

    @computed_field
    @property
    def first_name(self) -> str:
        name_pool = NAME_POOLS.get((self.race.value, self.gender.value), ["Alex"])
        seed_string = f"{self.race.value}-{self.gender.value}-{self.age_range.value}-{self.education_level.value}"
        seed = hash(seed_string) % (2**31)
        rng = random.Random(seed)
        return rng.choice(name_pool)

    @model_validator(mode="after")
    def validate_age_experience_consistency(self) -> "Person":
        age_experience_rules = {
            AgeRange.AGE_18_24: [ExperienceLevel.JUNIOR],
            AgeRange.AGE_25_34: [ExperienceLevel.JUNIOR, ExperienceLevel.MID_CAREER],
            AgeRange.AGE_35_44: [ExperienceLevel.JUNIOR, ExperienceLevel.MID_CAREER, ExperienceLevel.SENIOR],
            AgeRange.AGE_45_54: [ExperienceLevel.MID_CAREER, ExperienceLevel.SENIOR],
            AgeRange.AGE_55_64: [ExperienceLevel.SENIOR],
            AgeRange.AGE_65_PLUS: [ExperienceLevel.SENIOR],
        }
        allowed_experience = age_experience_rules.get(self.age_range, [])
        if self.experience_level not in allowed_experience:
            logger.warning(
                f"Inconsistent person attributes: experience level '{self.experience_level.value}' "
                f"with age range '{self.age_range.value}'"
            )
            raise ValueError(
                f"Experience level '{self.experience_level.value}' is not consistent "
                f"with age range '{self.age_range.value}'"
            )
        return self

    @model_validator(mode="after")
    def validate_age_education_consistency(self) -> "Person":
        if self.age_range == AgeRange.AGE_18_24 and self.education_level == EducationLevel.ADVANCED:
            logger.warning(
                f"Inconsistent person attributes: age range '{self.age_range.value}' "
                f"with education level '{self.education_level.value}'"
            )
            raise ValueError(
                f"Age range '{self.age_range.value}' is too young for "
                f"education level '{self.education_level.value}'"
            )
        return self

class CompensationEvaluator(Protocol):
    def evaluate(self, person: "Person") -> float:
        ...

class RuleBasedCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        # Base salary by industry sector
        industry_base = {
            IndustrySector.RETAIL: 42000,
            IndustrySector.MANUFACTURING: 56000,
            IndustrySector.HEALTHCARE: 69000,
            IndustrySector.INFORMATION_TECHNOLOGY: 110000,
            IndustrySector.FINANCIAL_SERVICES: 95000,
        }
        salary = industry_base.get(person.industry_sector, 50000)
        # Education level adjustment
        education_adjust = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: -0.18,   # -18%
            EducationLevel.UNDERGRADUATE: 0.05,          # +5%
            EducationLevel.ADVANCED: 0.16,               # +16%
        }
        salary += salary * education_adjust.get(person.education_level, 0)
        # Experience level adjustment
        experience_adjust = {
            ExperienceLevel.JUNIOR: -0.12,      # -12%
            ExperienceLevel.MID_CAREER: 0.13,   # +13%
            ExperienceLevel.SENIOR: 0.25,       # +25%
        }
        salary += salary * experience_adjust.get(person.experience_level, 0)
        # Employment type adjustment
        employment_adjust = {
            EmploymentType.FULL_TIME_PERMANENT: 0.00,
            EmploymentType.PART_TIME: -0.4,
            EmploymentType.CONTRACT: -0.15,
        }
        salary += salary * employment_adjust.get(person.employment_type, 0)
        # Gender wage gap adjustment
        gender_adjust = {
            Gender.MALE: 0.00,
            Gender.FEMALE: -0.06,
            Gender.NON_BINARY: -0.05,
        }
        salary += salary * gender_adjust.get(person.gender, 0)
        # Racial wage gap adjustment
        race_adjust = {
            Race.WHITE: 0.00,
            Race.ASIAN: 0.03,
            Race.BLACK: -0.08,
            Race.HISPANIC: -0.07,
        }
        salary += salary * race_adjust.get(person.race, 0)
        # Age range adjustment (possible seniority bump, or lower for very young/retired)
        age_adjust = {
            AgeRange.AGE_18_24: -0.14,
            AgeRange.AGE_25_34: -0.03,
            AgeRange.AGE_35_44: 0.01,
            AgeRange.AGE_45_54: 0.02,
            AgeRange.AGE_55_64: 0.00,
            AgeRange.AGE_65_PLUS: -0.10,
        }
        salary += salary * age_adjust.get(person.age_range, 0)
        # Parental status adjustment (no statistically significant, but very minor effect)
        parental_adjust = {
            ParentalStatus.NO_CHILDREN: 0.00,
            ParentalStatus.PARENT: -0.01,
        }
        salary += salary * parental_adjust.get(person.parental_status, 0)
        # Disability status adjustment
        disability_adjust = {
            DisabilityStatus.NO_DISABILITY: 0.00,
            DisabilityStatus.HAS_DISABILITY: -0.14,
        }
        salary += salary * disability_adjust.get(person.disability_status, 0)
        # Career gap adjustment
        career_gap_adjust = {
            CareerGap.NO_GAP: 0.00,
            CareerGap.SHORT_GAP: -0.04,
            CareerGap.EXTENDED_GAP: -0.12,
        }
        salary += salary * career_gap_adjust.get(person.career_gap, 0)
        # Clamp to a typical salary range
        salary = max(22000.0, min(salary, 700000.0))
        # Round to nearest integer and return as float
        return float(round(salary))
