from dataclasses import dataclass, field

# BMI cut-offs. These are the Asian-Indian values (overweight 23, obese 25).
# Check them against ICMR or WHO guidance. Use 25 and 30 for the standard WHO values.
OVERWEIGHT_BMI = 23.0
OBESE_BMI = 25.0

CONDITION_COLUMNS = {
    "diabetes": "risk_diabetes",
    "hypertension": "risk_hypertension",
    "obesity": "risk_obesity",
}


@dataclass
class Profile:
    age: int | None = None
    gender: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    bmi: float | None = None
    diabetes: bool = False
    hypertension: bool = False
    obesity: bool = False
    notes: list = field(default_factory=list)


def compute_bmi(p: Profile):
    if p.bmi:
        return round(p.bmi, 1)
    if p.height_cm and p.weight_kg and p.height_cm > 0:
        return round(p.weight_kg / (p.height_cm / 100) ** 2, 1)
    return None


def validate(p: Profile):
    """Raise ValueError for impossible values, so bad input never reaches the verdict."""
    if p.age is not None and not (0 <= p.age <= 120):
        raise ValueError("age must be between 0 and 120")
    bmi = compute_bmi(p)
    if bmi is not None and not (10 <= bmi <= 80):
        raise ValueError("BMI looks wrong. Check height and weight")


def active_conditions(p: Profile):
    """Which condition columns apply to this person."""
    validate(p)
    bmi = compute_bmi(p)
    active = []
    if p.diabetes:
        active.append("diabetes")
    if p.hypertension:
        active.append("hypertension")
    if p.obesity or (bmi is not None and bmi >= OBESE_BMI):
        active.append("obesity")
    return active


def profile_notes(p: Profile):
    notes = []
    bmi = compute_bmi(p)
    if bmi is not None and OVERWEIGHT_BMI <= bmi < OBESE_BMI and not p.obesity:
        notes.append("BMI is in the overweight range. Obesity risks are not applied unless you indicate obesity.")

    if p.age is not None or p.gender:
        notes.append("Age and gender are recorded and do not change the verdict.")
    return notes


def personal_risk(row, p: Profile):
    """Highest of the general risk and every active condition risk for one ingredient row."""
    risks = [row["risk_general"]] + [row[CONDITION_COLUMNS[c]] for c in active_conditions(p)]
    return max(risks)