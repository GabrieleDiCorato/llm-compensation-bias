from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator
import random

from .name_pools import NAME_POOLS


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
        
        # Create a deterministic seed from person attributes for reproducibility
        seed_string = f"{self.race.value}-{self.gender.value}-{self.age_range.value}-{self.education_level.value}"
        seed = hash(seed_string) % (2**31)
        
        # Use seeded random to ensure reproducibility
        rng = random.Random(seed)
        return rng.choice(name_pool)

    @model_validator(mode="after")
    def validate_age_experience_consistency(self) -> "Person":
        """Validate that experience level is consistent with age range."""
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
            raise ValueError(
                f"Experience level '{self.experience_level.value}' is not consistent "
                f"with age range '{self.age_range.value}'"
            )

        return self

    @model_validator(mode="after")
    def validate_age_education_consistency(self) -> "Person":
        """Validate that education level is realistic for age range."""
        if self.age_range == AgeRange.AGE_18_24 and self.education_level == EducationLevel.ADVANCED:
            raise ValueError(
                f"Age range '{self.age_range.value}' is too young for "
                f"education level '{self.education_level.value}'"
            )

        return self