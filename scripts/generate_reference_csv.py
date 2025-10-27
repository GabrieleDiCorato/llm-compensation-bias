"""
Generate reference dataset CSV file.

Creates a CSV file with Person instances using stratified sampling.
Useful for external analysis or sharing reference datasets.
"""

import csv
import logging
from pathlib import Path

from src.simulation.reference_dataset import generate_reference_dataset

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def generate_csv(
    output_path: Path,
    size: int = 10000,
    stratify_by: list[str] | None = None,
    validate_realism: bool = True,
    seed: int = 42,
) -> None:
    """
    Generate reference dataset and save to CSV.

    Args:
        output_path: Path to output CSV file
        size: Number of Person instances to generate
        stratify_by: Attributes to stratify on (uses defaults if None)
        validate_realism: If True, reject unrealistic attribute combinations
        seed: Random seed for reproducibility
    """
    logger.info(f"Generating reference dataset with {size} instances")

    # Generate dataset
    dataset = generate_reference_dataset(
        size=size,
        stratify_by=stratify_by,
        validate_realism=validate_realism,
        seed=seed,
    )

    logger.info(f"Writing {len(dataset)} instances to {output_path}")

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write to CSV
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        # Get field names from first person (exclude first_name if None)
        fieldnames = [
            "first_name",
            "gender",
            "ethnicity",
            "age_range",
            "education_level",
            "experience_level",
            "industry_sector",
            "employment_type",
            "parental_status",
            "disability_status",
            "career_gap",
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for person in dataset:
            row = {
                "first_name": person.first_name,
                "gender": person.gender.value,
                "ethnicity": person.ethnicity.value,
                "age_range": person.age_range.value,
                "education_level": person.education_level.value,
                "experience_level": person.experience_level.value,
                "industry_sector": person.industry_sector.value,
                "employment_type": person.employment_type.value,
                "parental_status": person.parental_status.value,
                "disability_status": person.disability_status.value,
                "career_gap": person.career_gap.value,
            }
            writer.writerow(row)

    logger.info(f"Successfully wrote CSV to {output_path}")


if __name__ == "__main__":
    # Default output path
    output_file = Path(__file__).parent.parent / "data" / "reference_population_v1.csv"

    # Generate CSV with 10,000 instances
    generate_csv(
        output_path=output_file,
        size=200000,
        validate_realism=True,
        seed=42,
    )

    logger.info("Done!")
