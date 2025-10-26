from typing import Protocol
from src.model.person import Person

class SimpleCompensationEvaluator(CompensationEvaluator):
    """A simple rule-based implementation of CompensationEvaluator."""
    
    def evaluate(self, person: Person) -> float:
        """
        Evaluate expected annual compensation based on person attributes using simple rules.
        
        Args:
            person: A Person instance with demographic and professional attributes
            
        Returns:
            Estimated annual compensation in USD as a float
        """
        # Base salary starts at 30,000 USD
        base_salary = 30000.0
        
        # Adjust based on education level
        education_multipliers = {
            person.education_level.HIGH_SCHOOL_OR_LESS: 1.0,
            person.education_level.UNDERGRADUATE: 1.5,
            person.education_level.ADVANCED: 2.0
        }
        base_salary *= education_multipliers[person.education_level]
        
        # Adjust based on experience level
        experience_multipliers = {
            person.experience_level.JUNIOR: 1.0,
            person.experience_level.MID_CAREER: 1.5,
            person.experience_level.SENIOR: 2.0
        }
        base_salary *= experience_multipliers[person.experience_level]
        
        # Adjust based on industry sector
        industry_multipliers = {
            person.industry_sector.RETAIL: 0.8,
            person.industry_sector.MANUFACTURING: 1.0,
            person.industry_sector.HEALTHCARE: 1.2,
            person.industry_sector.INFORMATION_TECHNOLOGY: 1.5,
            person.industry_sector.FINANCIAL_SERVICES: 1.4
        }
        base_salary *= industry_multipliers[person.industry_sector]
        
        # Adjust based on employment type
        employment_multipliers = {
            person.employment_type.FULL_TIME_PERMANENT: 1.0,
            person.employment_type.PART_TIME: 0.5,
            person.employment_type.CONTRACT: 0.9
        }
        base_salary *= employment_multipliers[person.employment_type]
        
        # Adjust based on age range (as proxy for experience within brackets)
        age_multipliers = {
            person.age_range.AGE_18_24: 0.9,
            person.age_range.AGE_25_34: 1.0,
            person.age_range.AGE_35_44: 1.1,
            person.age_range.AGE_45_54: 1.2,
            person.age_range.AGE_55_64: 1.2,
            person.age_range.AGE_65_PLUS: 1.1
        }
        base_salary *= age_multipliers[person.age_range]
        
        # Apply minor adjustments for other factors
        if person.parental_status == person.parental_status.PARENT:
            base_salary *= 0.95  # Slight reduction for parental responsibilities
        if person.disability_status == person.disability_status.HAS_DISABILITY:
            base_salary *= 0.95  # Slight reduction for potential workplace challenges
        if person.career_gap == person.career_gap.SHORT_GAP:
            base_salary *= 0.95
        elif person.career_gap == person.career_gap.EXTENDED_GAP:
            base_salary *= 0.85
            
        # Ensure salary is within reasonable bounds (20K - 300K)
        return max(20000.0, min(300000.0, base_salary))