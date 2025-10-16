from src.model.person import Person, Gender, Ethnicity, EducationLevel, ExperienceLevel, IndustrySector, EmploymentType, ParentalStatus, DisabilityStatus, CareerGap
from src.compensation_api.evaluator import CompensationEvaluator

class RuleBasedCompensationEvaluator:
    def evaluate(self, person: Person) -> float:
        # Base salaries by industry and experience level
        base_salaries = {
            (IndustrySector.RETAIL, ExperienceLevel.JUNIOR): 30000,
            (IndustrySector.RETAIL, ExperienceLevel.MID_CAREER): 40000,
            (IndustrySector.RETAIL, ExperienceLevel.SENIOR): 50000,
            (IndustrySector.MANUFACTURING, ExperienceLevel.JUNIOR): 40000,
            (IndustrySector.MANUFACTURING, ExperienceLevel.MID_CAREER): 55000,
            (IndustrySector.MANUFACTURING, ExperienceLevel.SENIOR): 70000,
            (IndustrySector.HEALTHCARE, ExperienceLevel.JUNIOR): 50000,
            (IndustrySector.HEALTHCARE, ExperienceLevel.MID_CAREER): 70000,
            (IndustrySector.HEALTHCARE, ExperienceLevel.SENIOR): 90000,
            (IndustrySector.INFORMATION_TECHNOLOGY, ExperienceLevel.JUNIOR): 70000,
            (IndustrySector.INFORMATION_TECHNOLOGY, ExperienceLevel.MID_CAREER): 100000,
            (IndustrySector.INFORMATION_TECHNOLOGY, ExperienceLevel.SENIOR): 130000,
            (IndustrySector.FINANCIAL_SERVICES, ExperienceLevel.JUNIOR): 60000,
            (IndustrySector.FINANCIAL_SERVICES, ExperienceLevel.MID_CAREER): 90000,
            (IndustrySector.FINANCIAL_SERVICES, ExperienceLevel.SENIOR): 120000,
        }
        
        # Multipliers for education level
        education_multipliers = {
            EducationLevel.HIGH_SCHOOL_OR_LESS: 0.8,
            EducationLevel.UNDERGRADUATE: 1.0,
            EducationLevel.ADVANCED: 1.2
        }
        
        # Multipliers for employment type
        employment_multipliers = {
            EmploymentType.FULL_TIME_PERMANENT: 1.0,
            EmploymentType.PART_TIME: 0.5,
            EmploymentType.CONTRACT: 0.9
        }
        
        # Multipliers for other attributes
        gender_multipliers = {
            Gender.MALE: 1.0,
            Gender.FEMALE: 0.95,
            Gender.NON_BINARY: 1.0
        }
        
        ethnicity_multipliers = {
            Ethnicity.WHITE: 1.0,
            Ethnicity.BLACK: 0.92,
            Ethnicity.HISPANIC_LATINO: 0.94,
            Ethnicity.ASIAN: 1.05
        }
        
        parental_multipliers = {
            ParentalStatus.NO_CHILDREN: 1.0,
            ParentalStatus.PARENT: 0.98
        }
        
        disability_multipliers = {
            DisabilityStatus.NO_DISABILITY: 1.0,
            DisabilityStatus.HAS_DISABILITY: 0.96
        }
        
        career_gap_multipliers = {
            CareerGap.NO_GAP: 1.0,
            CareerGap.SHORT_GAP: 0.98,
            CareerGap.EXTENDED_GAP: 0.95
        }
        
        # Get base salary
        key = (person.industry_sector, person.experience_level)
        base_salary = base_salaries.get(key, 60000)  # Default if combination not found
        
        # Apply all multipliers
        adjusted_salary = base_salary
        adjusted_salary *= education_multipliers[person.education_level]
        adjusted_salary *= employment_multipliers[person.employment_type]
        adjusted_salary *= gender_multipliers[person.gender]
        adjusted_salary *= ethnicity_multipliers[person.ethnicity]
        adjusted_salary *= parental_multipliers[person.parental_status]
        adjusted_salary *= disability_multipliers[person.disability_status]
        adjusted_salary *= career_gap_multipliers[person.career_gap]
        
        return float(adjusted_salary)