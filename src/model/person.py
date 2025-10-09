from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-binary"


class Race(str, Enum):
    WHITE = "White"
    BLACK = "Black/African American"
    HISPANIC = "Hispanic/Latino"
    ASIAN = "Asian"
    NATIVE_AMERICAN = "Native American"
    PACIFIC_ISLANDER = "Pacific Islander"
    MIXED_RACE = "Mixed Race"


class AgeRange(str, Enum):
    AGE_18_24 = "18-24"
    AGE_25_34 = "25-34"
    AGE_35_44 = "35-44"
    AGE_45_54 = "45-54"
    AGE_55_64 = "55-64"
    AGE_65_PLUS = "65+"


class EducationLevel(str, Enum):
    HIGH_SCHOOL = "High School Diploma"
    BACHELOR = "Bachelor's Degree"
    MASTER = "Master's Degree"


class IndustrySector(str, Enum):
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    HEALTHCARE = "Healthcare"
    INFORMATION_TECHNOLOGY = "Information Technology"
    FINANCIAL_SERVICES = "Financial Services"


class Person(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
        arbitrary_types_allowed=False,
        extra="forbid"
    )

    gender: Gender = Field(..., description="The person's gender identity")
    race: Race = Field(..., description="The person's racial or ethnic background")
    age_range: AgeRange = Field(..., description="The person's age bracket")
    education_level: EducationLevel = Field(..., description="The highest level of education completed")
    years_of_experience: int = Field(..., ge=0, le=50, description="Total years of professional work experience")
    industry_sector: IndustrySector = Field(..., description="The industry sector in which the person works")
