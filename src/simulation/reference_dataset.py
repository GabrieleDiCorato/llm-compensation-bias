"""
Generate standard reference dataset of Person instances with stratified sampling.

This project is focused on bias research; thus, the reference dataset must ensure
adequate representation of minority groups across key demographic and professional
attributes. It provides stratified sampling to ensure proportional
representation, not realistic population distributions.
"""

import itertools
import logging
import random
from enum import Enum
from typing import Any

from src.model.person import (
    AgeRange,
    CareerGap,
    DisabilityStatus,
    EducationLevel,
    EmploymentType,
    Ethnicity,
    ExperienceLevel,
    Gender,
    IndustrySector,
    ParentalStatus,
    Person,
)

logger = logging.getLogger(__name__)


class ReferenceDatasetGenerator:
    """
    Generate reference dataset with stratified sampling.

    Implements equal-allocation stratified sampling where the population is divided
    into homogeneous subgroups (strata) and equal samples are drawn from each
    stratum. This ensures balanced representation of key demographic attributes
    critical for bias detection, including adequate representation of minority groups.
    """

    # Class constants
    DEFAULT_SEED = 42
    DEFAULT_TOLERANCE = 0.05
    DEFAULT_STRATA = ["gender", "ethnicity", "parental_status", "disability_status"]
    MIN_SAMPLES_PER_STRATUM = 3

    def __init__(self, seed: int = DEFAULT_SEED):
        """
        Initialize the dataset generator.

        Args:
            seed: Random seed for reproducibility
        """
        self.seed = seed
        self.rng = random.Random(seed)
        logger.debug(f"Initialized ReferenceDatasetGenerator with seed {seed}")

    def generate_stratified_sample(
        self,
        size: int,
        stratify_by: list[str] = DEFAULT_STRATA,
        validate_realism: bool = False,
    ) -> list[Person]:
        """
        Generate stratified sample with equal allocation across strata.

        Divides the population into strata based on specified attributes and draws
        equal samples from each stratum. Since population proportions are unknown,
        equal allocation ensures adequate representation of all groups, including
        minorities. This is critical for bias detection where minority groups must
        be sufficiently represented.

        Args:
            size: Target number of Person instances to generate
            stratify_by: Attributes to stratify on. Defaults to protected characteristics
            validate_realism: If True, reject unrealistic attribute combinations
                            (e.g., age 18-24 with 16+ years experience)

        Returns:
            List of Person instances with equal stratified distribution

        Raises:
            ValueError: If size is non-positive, strata are empty, or size is insufficient
        """
        if size <= 0:
            raise ValueError(f"Size must be positive, got {size}")

        logger.info(f"Generating stratified sample of size {size}, stratified by: {stratify_by}")

        # Build strata based on specified attributes
        strata_enums = self._get_strata_enums(stratify_by)
        strata_combinations = list(itertools.product(*strata_enums))

        if not strata_combinations:
            raise ValueError("No strata combinations found. Check stratify_by attributes.")

        num_strata = len(strata_combinations)
        logger.info(f"Strata combinations size: {num_strata}")

        # Validate sample size sufficiency
        if size < num_strata:
            raise ValueError(f"Size ({size}) must be at least equal to number of strata ({num_strata}) " f"to ensure representation of all strata.")

        min_recommended_size = num_strata * self.MIN_SAMPLES_PER_STRATUM
        if size < min_recommended_size:
            logger.warning(f"Sample size ({size}) is small relative to number of strata ({num_strata}). " f"Recommend at least {min_recommended_size} samples (>= {self.MIN_SAMPLES_PER_STRATUM} per stratum) " f"for statistical validity.")

        # Calculate samples per stratum (equal allocation)
        samples_per_stratum = size // num_strata
        remainder = size % num_strata
        logger.debug(f"Equal allocation: {samples_per_stratum} per stratum, {remainder} remainder distributed")

        persons = []
        strata_attr_names = stratify_by

        # Generate samples for each stratum
        for idx, stratum_values in enumerate(strata_combinations):
            # Determine number of samples for this stratum
            n_samples = samples_per_stratum
            if idx < remainder:  # Distribute remainder samples
                n_samples += 1

            if n_samples == 0:
                continue

            # Build stratum specification
            stratum_spec = dict(zip(strata_attr_names, stratum_values, strict=False))

            # Generate samples within this stratum
            for _ in range(n_samples):
                person = self._generate_person_in_stratum(stratum_spec, validate_realism)
                persons.append(person)

        # Shuffle to avoid clustering by strata
        self.rng.shuffle(persons)

        # Log stratification report
        self._log_stratification_report(persons, stratify_by)

        logger.info(f"Generated {len(persons)} instances across {num_strata} strata")
        return persons

    def _get_strata_enums(self, stratify_by: list[str]) -> list[list[Enum]]:
        """
        Get enum classes for stratification attributes.

        Dynamically builds attribute map by inspecting Person model annotations.

        Args:
            stratify_by: List of attribute names to stratify on

        Returns:
            List of enum value lists for each attribute

        Raises:
            ValueError: If attribute name is not recognized or not an enum
        """
        # Build attribute map dynamically from Person model
        attribute_map: dict[str, list[Enum]] = {}
        for field_name, field_type in Person.model_fields.items():
            # Get the actual type (handles Optional types)
            annotation = field_type.annotation

            # Check if it's an Enum subclass
            if isinstance(annotation, type) and issubclass(annotation, Enum):
                attribute_map[field_name] = list(annotation)

        enums = []
        for attr in stratify_by:
            if attr not in attribute_map:
                raise ValueError(f"Unknown attribute '{attr}'. Valid attributes: {list(attribute_map.keys())}")
            enums.append(attribute_map[attr])

        return enums

    def _generate_person_in_stratum(self, stratum_spec: dict[str, Any], validate_realism: bool = False, max_retries: int = 100) -> Person:
        """
        Generate a Person instance with fixed stratum attributes and random others.

        Args:
            stratum_spec: Dictionary of attribute names to fixed values
            validate_realism: If True, reject unrealistic attribute combinations
            max_retries: Maximum attempts to generate realistic combination

        Returns:
            Person instance with specified stratum attributes
        """
        person = None
        for _attempt in range(max_retries):
            # Start with random values for all attributes
            attributes = {
                "gender": self.rng.choice(list(Gender)),
                "ethnicity": self.rng.choice(list(Ethnicity)),
                "age_range": self.rng.choice(list(AgeRange)),
                "education_level": self.rng.choice(list(EducationLevel)),
                "experience_level": self.rng.choice(list(ExperienceLevel)),
                "industry_sector": self.rng.choice(list(IndustrySector)),
                "employment_type": self.rng.choice(list(EmploymentType)),
                "parental_status": self.rng.choice(list(ParentalStatus)),
                "disability_status": self.rng.choice(list(DisabilityStatus)),
                "career_gap": self.rng.choice(list(CareerGap)),
            }

            # Override with stratum-specific values
            attributes.update(stratum_spec)

            person = Person(**attributes)

            if not validate_realism or self._is_realistic(person):
                return person

        # If we couldn't generate realistic combination, log warning and return anyway
        logger.warning(f"Could not generate realistic combination after {max_retries} attempts " f"for stratum {stratum_spec}. Returning potentially unrealistic instance.")
        # Person is guaranteed to be assigned by the loop
        return person  # type: ignore[return-value]

    def _is_realistic(self, person: Person) -> bool:
        """
        Check for obviously unrealistic attribute combinations.

        Validates age-experience consistency and age-education plausibility.

        Args:
            person: Person instance to validate

        Returns:
            True if combination is realistic, False otherwise
        """
        # Age-experience consistency: younger people can't have extensive experience
        age_to_max_experience = {
            AgeRange.AGE_18_24: ExperienceLevel.JUNIOR,  # Max 5 years
            AgeRange.AGE_25_34: ExperienceLevel.MID_CAREER,  # Max 15 years
            AgeRange.AGE_35_44: ExperienceLevel.SENIOR,  # Can have 16+
            AgeRange.AGE_45_54: ExperienceLevel.SENIOR,
            AgeRange.AGE_55_64: ExperienceLevel.SENIOR,
            AgeRange.AGE_65_PLUS: ExperienceLevel.SENIOR,
        }

        max_allowed_exp = age_to_max_experience.get(person.age_range)
        if max_allowed_exp:
            # Compare experience levels by their position in the enum
            person_exp_index = list(ExperienceLevel).index(person.experience_level)
            max_exp_index = list(ExperienceLevel).index(max_allowed_exp)
            if person_exp_index > max_exp_index:
                return False

        # Age-education plausibility: advanced degrees unlikely for very young
        if person.age_range == AgeRange.AGE_18_24 and person.education_level == EducationLevel.ADVANCED:
            # Rare but possible (e.g., prodigies), so allow with low probability
            if self.rng.random() > 0.1:  # 90% rejection rate
                return False

        return True

    def _log_stratification_report(self, dataset: list[Person], stratify_by: list[str]) -> None:
        """
        Log stratification summary statistics.

        Args:
            dataset: Generated dataset
            stratify_by: Attributes that were stratified
        """
        try:
            distribution = self.compute_distribution(dataset)
            logger.info("Stratification report:")
            for attr in stratify_by:
                if attr not in distribution:
                    continue
                attr_data = distribution[attr]
                props = attr_data["proportions"]
                balance = attr_data["balance_metrics"]
                min_prop = min(props.values())
                max_prop = max(props.values())
                logger.info(f"  {attr}: n_values={len(props)}, min={min_prop:.3f}, max={max_prop:.3f}, " f"CV={balance['coefficient_of_variation']:.3f}, " f"balanced={balance['is_balanced']}")
        except Exception as e:
            logger.warning(f"Could not generate stratification report: {e}")

    def compute_distribution(self, dataset: list[Person]) -> dict[str, dict[str, Any]]:
        """
        Compute proportional distribution with balance metrics.

        Returns proportions (0.0-1.0) and statistical balance measures including
        coefficient of variation to assess distribution uniformity.

        Args:
            dataset: List of Person instances

        Returns:
            Dictionary mapping attribute names to distribution data containing:
                - proportions: Dict of value -> proportion
                - balance_metrics: Dict with coefficient_of_variation and is_balanced

        Raises:
            ValueError: If dataset is empty
        """
        if not dataset:
            raise ValueError("Cannot compute distribution of empty dataset")

        # Initialize counts dynamically from Person model fields
        counts: dict[str, dict[str, int]] = {}
        for field_name, field_type in Person.model_fields.items():
            annotation = field_type.annotation
            # Only include Enum fields (skip first_name which is str | None)
            if isinstance(annotation, type) and issubclass(annotation, Enum):
                counts[field_name] = {}

        # Count occurrences for each person
        for person in dataset:
            for field_name in counts.keys():
                value = getattr(person, field_name).value
                counts[field_name][value] = counts[field_name].get(value, 0) + 1

        # Convert to proportions and calculate balance metrics
        result: dict[str, dict[str, Any]] = {}
        for attr_name, attr_counts in counts.items():
            total = sum(attr_counts.values())
            proportions = {value: count / total for value, count in attr_counts.items()}

            # Calculate balance metrics
            values_list = list(proportions.values())
            if len(values_list) == 0:
                # Edge case: no values (should never happen with valid data)
                cv = float("inf")
                is_balanced = False
            elif len(values_list) == 1:
                # Perfect balance with single value
                cv = 0.0
                is_balanced = True
            else:
                mean_prop = sum(values_list) / len(values_list)
                variance = sum((p - mean_prop) ** 2 for p in values_list) / len(values_list)
                std_prop = variance**0.5
                cv = std_prop / mean_prop if mean_prop > 0 else float("inf")
                is_balanced = cv < 0.1  # CV < 10% indicates good balance

            result[attr_name] = {
                "proportions": proportions,
                "balance_metrics": {
                    "coefficient_of_variation": cv,
                    "is_balanced": is_balanced,
                },
            }

        return result

    def validate_stratification(
        self,
        dataset: list[Person],
        stratify_by: list[str],
        tolerance: float = DEFAULT_TOLERANCE,
        use_chi_square: bool = False,
        significance_level: float = 0.05,
    ) -> dict[str, dict[str, Any]]:
        """
        Validate that stratification is balanced within tolerance.

        Checks if the distribution of stratified attributes is uniform using
        simple tolerance-based validation or chi-square goodness-of-fit test.

        Args:
            dataset: List of Person instances to validate
            stratify_by: Attributes that should be stratified
            tolerance: Acceptable deviation from perfect balance (default 5%)
            use_chi_square: If True, perform chi-square goodness-of-fit test
            significance_level: Alpha level for chi-square test (default 0.05)

        Returns:
            Dictionary mapping attribute names to validation results containing:
                - is_balanced: bool
                - max_deviation: float (for tolerance-based)
                - chi2_statistic, p_value, significance_level (for chi-square)
        """
        distribution = self.compute_distribution(dataset)
        n = len(dataset)

        results = {}
        for attr in stratify_by:
            if attr not in distribution:
                logger.warning(f"Attribute '{attr}' not found in distribution")
                results[attr] = {"is_balanced": False, "error": "Attribute not found"}
                continue

            attr_data = distribution[attr]
            attr_dist = attr_data["proportions"]
            n_values = len(attr_dist)

            if n_values == 0:
                logger.warning(f"Attribute '{attr}' has no values in distribution")
                results[attr] = {"is_balanced": False, "error": "No values"}
                continue

            expected_proportion = 1.0 / n_values

            if use_chi_square:
                # Chi-square goodness-of-fit test
                try:
                    from scipy.stats import chisquare

                    # Observed frequencies
                    observed = [int(prop * n) for prop in attr_dist.values()]
                    expected = [n / n_values] * n_values

                    chi2_stat, p_value = chisquare(observed, expected)

                    is_balanced = p_value > significance_level

                    results[attr] = {
                        "is_balanced": is_balanced,
                        "chi2_statistic": float(chi2_stat),
                        "p_value": float(p_value),
                        "significance_level": significance_level,
                        "interpretation": (f"Fail to reject null hypothesis (uniform distribution) at α={significance_level}" if is_balanced else f"Reject null hypothesis at α={significance_level}"),
                    }

                    if not is_balanced:
                        logger.warning(f"Attribute '{attr}' failed chi-square test: χ²={chi2_stat:.3f}, " f"p={p_value:.4f} (α={significance_level})")
                except ImportError:
                    logger.warning("scipy not available for chi-square test. Install scipy for statistical testing.")
                    # Fall back to tolerance-based validation
                    use_chi_square = False

            if not use_chi_square:
                # Tolerance-based validation
                deviations = [abs(proportion - expected_proportion) for proportion in attr_dist.values()]
                max_deviation = max(deviations)

                is_balanced = all(deviation <= tolerance for deviation in deviations)

                results[attr] = {
                    "is_balanced": is_balanced,
                    "max_deviation": max_deviation,
                    "expected_proportion": expected_proportion,
                    "tolerance": tolerance,
                }

                if not is_balanced:
                    logger.warning(f"Attribute '{attr}' not balanced: max deviation {max_deviation:.3f} " f"(expected {expected_proportion:.3f} ± {tolerance:.3f})")

        return results


def generate_reference_dataset(
    size: int = 100,
    stratify_by: list[str] | None = None,
    validate_realism: bool = False,
    seed: int = ReferenceDatasetGenerator.DEFAULT_SEED,
) -> list[Person]:
    """
    Generate reference dataset with stratified sampling.

    Convenience function for generating datasets with equal-allocation stratification.
    Ensures balanced representation of protected characteristics for bias analysis,
    with adequate representation of minority groups.

    Args:
        size: Target number of Person instances
        stratify_by: Attributes to stratify on. Defaults to ['gender', 'ethnicity', 'education_level']
        validate_realism: If True, reject unrealistic combinations (e.g., young age with high experience)
        seed: Random seed for reproducibility

    Returns:
        List of Person instances with stratified distribution

    Example:
        >>> # Generate 108 instances stratified by gender, ethnicity, education
        >>> # (3 genders × 4 ethnicities × 3 education levels = 36 strata, 3 samples per stratum)
        >>> dataset = generate_reference_dataset(size=108)
        >>> len(dataset)
        108
        >>>
        >>> # Verify balanced distribution
        >>> generator = ReferenceDatasetGenerator(seed=42)
        >>> dist = generator.compute_distribution(dataset)
        >>> dist['gender']['proportions']
        {'Male': 0.333, 'Female': 0.333, 'Non-binary': 0.333}
        >>>
        >>> # Generate with custom stratification
        >>> dataset = generate_reference_dataset(
        ...     size=200,
        ...     stratify_by=['gender', 'industry_sector'],
        ...     seed=42
        ... )
    """
    generator = ReferenceDatasetGenerator(seed=seed)

    # Use default strata if not specified
    if stratify_by is None:
        stratify_by = ReferenceDatasetGenerator.DEFAULT_STRATA

    return generator.generate_stratified_sample(
        size=size,
        stratify_by=stratify_by,
        validate_realism=validate_realism,
    )
