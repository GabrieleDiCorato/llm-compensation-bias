"""
Simulation and reference dataset generation for compensation evaluation.
"""

from ..simulation.name_pools import get_first_name
from .reference_dataset import ReferenceDatasetGenerator, generate_reference_dataset

__all__ = ["ReferenceDatasetGenerator", "generate_reference_dataset", "get_first_name"]
