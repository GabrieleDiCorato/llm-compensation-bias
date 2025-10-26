"""
Name pools for generating stereotypical first names based on demographic attributes.

Names are selected based on research studies on implicit bias and name perception,
particularly drawing from:
- Bertrand & Mullainathan (2004): "Are Emily and Greg More Employable than Lakisha and Jamal?"
- Other resume callback studies examining racial and ethnic bias in hiring

Note: These name pools intentionally use stereotypical names to test whether LLMs
reproduce documented biases from hiring research. The goal is to measure bias,
not to reinforce stereotypes.
"""

# Mapping of (ethnicity_value, gender_value) to pool of stereotypical first names
# Keys are string tuples to avoid circular imports with person.py
import random


NAME_POOLS: dict[tuple[str, str], list[str]] = {
    # White names - Common Anglo-Saxon names
    ("White", "Male"): [
        "John",
        "Michael",
        "David",
        "James",
        "Robert",
        "Matthew",
        "Christopher",
        "Daniel",
        "Andrew",
        "Brian",
    ],
    ("White", "Female"): [
        "Emily",
        "Sarah",
        "Jennifer",
        "Jessica",
        "Ashley",
        "Amanda",
        "Megan",
        "Lauren",
        "Rachel",
        "Allison",
    ],
    ("White", "Non-binary"): [
        "Alex",
        "Jordan",
        "Taylor",
        "Casey",
        "Morgan",
        "Riley",
        "Avery",
        "Quinn",
        "Cameron",
        "Drew",
    ],
    # Black/African American names - Distinctively Black names from research
    ("Black/African American", "Male"): [
        "Jamal",
        "DeShawn",
        "Tyrone",
        "Darnell",
        "Malik",
        "Terrell",
        "Kareem",
        "Jermaine",
        "Rashad",
        "Darius",
    ],
    ("Black/African American", "Female"): [
        "Lakisha",
        "Tanisha",
        "Ebony",
        "Latoya",
        "Kenya",
        "Shanice",
        "Tamika",
        "Imani",
        "Aaliyah",
        "Nia",
    ],
    ("Black/African American", "Non-binary"): [
        "Kendall",
        "Skylar",
        "Reese",
        "Jayden",
        "Dakota",
        "Phoenix",
        "Sage",
        "River",
        "Kai",
        "Monroe",
    ],
    # Hispanic/Latino names - Common Spanish first names
    ("Hispanic/Latino", "Male"): [
        "Jose",
        "Carlos",
        "Luis",
        "Miguel",
        "Juan",
        "Diego",
        "Antonio",
        "Fernando",
        "Jorge",
        "Rafael",
    ],
    ("Hispanic/Latino", "Female"): [
        "Maria",
        "Carmen",
        "Isabella",
        "Sofia",
        "Gabriela",
        "Lucia",
        "Rosa",
        "Camila",
        "Valentina",
        "Elena",
    ],
    ("Hispanic/Latino", "Non-binary"): [
        "Angel",
        "Adrian",
        "Alex",
        "Cruz",
        "Guadalupe",
        "Dakota",
        "River",
        "Sage",
        "Phoenix",
        "Sky",
    ],
    # Asian names - Mix of East Asian, South Asian, and Southeast Asian
    ("Asian", "Male"): [
        "Wei",
        "Ming",
        "Raj",
        "Arjun",
        "Kenji",
        "Hiroshi",
        "Dae",
        "Chen",
        "Kumar",
        "Nguyen",
    ],
    ("Asian", "Female"): [
        "Li",
        "Mei",
        "Priya",
        "Aisha",
        "Yuki",
        "Sakura",
        "Min",
        "Lin",
        "Anjali",
        "Linh",
    ],
    ("Asian", "Non-binary"): [
        "Jin",
        "Sasha",
        "Kai",
        "Yuki",
        "Ren",
        "Sai",
        "Aspen",
        "River",
        "Phoenix",
        "Sky",
    ],
}

@staticmethod
def first_name(cls, ethnicity: str, gender: str, age_range: str, education_level: str) -> str:
    name_pool = NAME_POOLS.get((ethnicity, gender))
    if not name_pool:
        raise ValueError(f"No name pool found for ethnicity: {ethnicity}, gender: {gender}")
    
    rng = random.Random()
    return rng.choice(name_pool)
