from __future__ import annotations

class SimpleCompensationEvaluator:
    """
    A concrete heuristic-based implementation of the CompensationEvaluator protocol.
    Estimates annual salary in USD based on a mix of industry, education, experience,
    age, employment type, parental status, disability status, and career gaps.
    """

    def evaluate(self, person: "Person") -> float:
        # Base salary by industry
        industry_base = {
            "IT": 95000,
            "Healthcare": 80000,
            "Financial Services": 85000,
            "Manufacturing": 65000,
            "Retail": 60000,
        }
        sector = getattr(person, "industry_sector").value if hasattr(person, "industry_sector") else ""
        base = industry_base.get(sector, 60000)

        # Education level adjustments
        edu = getattr(person, "education_level").value if hasattr(person, "education_level") else ""
        edu_adjust = {
            "High School or Less": -10000,
            "Undergraduate Degree": 0,
            "Advanced Degree": 15000,
        }.get(edu, 0)

        # Experience level adjustments
        exp = getattr(person, "experience_level").value if hasattr(person, "experience_level") else ""
        exp_adjust = {
            "0-5": 0,
            "6-15": 15000,
            "16+": 32000,
        }.get(exp, 0)

        # Age range adjustments
        age = getattr(person, "age_range").value if hasattr(person, "age_range") else ""
        age_adjust = {
            "18-24": 0,
            "25-34": 1500,
            "35-44": 6000,
            "45-54": 9000,
            "55-64": 7000,
            "65+": -1000,
        }.get(age, 0)

        # Employment type adjustments
        emp_type = getattr(person, "employment_type").value if hasattr(person, "employment_type") else ""
        emp_adjust = {
            "Full-time": 0,
            "Part-time": -12000,
            "Contract/Temporary": -7000,
        }.get(emp_type, 0)

        # Parental status adjustments
        parental = getattr(person, "parental_status").value if hasattr(person, "parental_status") else ""
        parental_adjust = {
            "No Children": 0,
            "Parent": -2000,
        }.get(parental, 0)

        # Disability status adjustments
        disability = getattr(person, "disability_status").value if hasattr(person, "disability_status") else ""
        disability_adjust = {
            "No": 0,
            "Yes": -3000,
        }.get(disability, 0)

        # Career gap adjustments
        gap = getattr(person, "career_gap").value if hasattr(person, "career_gap") else ""
        gap_adjust = {
            "No": 0,
            "1-2 Year Gap": -4000,
            "3+ Year Gap": -8000,
        }.get(gap, 0)

        salary = (
            base
            + edu_adjust
            + exp_adjust
            + age_adjust
            + emp_adjust
            + parental_adjust
            + disability_adjust
            + gap_adjust
        )

        if salary < 0:
            salary = 0.0

        return float(salary)