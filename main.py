import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from pathlib import Path

# -------------------------------
# Data Models (Pydantic)
# -------------------------------
class PatientBase(BaseModel):
    id: str
    Name: str
    City: str
    Age: int
    Gender: str
    Height: float
    Weight: float
    Blood_Pressure: str
    Heart_Rate: int
    Medical_History: List[str]
    Verdict: str

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    Name: Optional[str] = None
    City: Optional[str] = None
    Age: Optional[int] = None
    Gender: Optional[str] = None
    Height: Optional[float] = None
    Weight: Optional[float] = None
    Blood_Pressure: Optional[str] = None
    Heart_Rate: Optional[int] = None
    Medical_History: Optional[List[str]] = None
    Verdict: Optional[str] = None

class PatientResponse(PatientBase):
    pass

# -------------------------------
# JSON "Database" Helper
# -------------------------------
DATA_FILE = Path("patients.json")

def read_data() -> dict:
    """Read JSON file and return dict keyed by patient id."""
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    # Ensure data is a dict {id: record}
    if isinstance(data, list):
        # Convert old list format to dict
        return {item["id"]: item for item in data}
    return data

def write_data(patients: dict) -> None:
    """Write the entire patient dictionary to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(list(patients.values()), f, indent=2)

# -------------------------------
# FastAPI App
# -------------------------------
app = FastAPI(title="Patient Management API")

# ---------- CRUD Endpoints ----------
@app.get("/patients", response_model=List[PatientResponse])
async def get_patients(
    city: Optional[str] = None,
    gender: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    medical_history: Optional[str] = Query(None, description="Comma-separated list of conditions")
):
    """
    Retrieve all patients with optional filtering.
    - `medical_history`: comma-separated values, e.g. "hypertension,diabetes"
    """
    patients_dict = read_data()
    result = list(patients_dict.values())

    if city:
        result = [p for p in result if p["City"].lower() == city.lower()]
    if gender:
        result = [p for p in result if p["Gender"].lower() == gender.lower()]
    if min_age is not None:
        result = [p for p in result if p["Age"] >= min_age]
    if max_age is not None:
        result = [p for p in result if p["Age"] <= max_age]
    if medical_history:
        conditions = [cond.strip().lower() for cond in medical_history.split(",")]
        result = [
            p for p in result
            if any(cond in [h.lower() for h in p["Medical_History"]] for cond in conditions)
        ]
    return result

@app.get("/patients/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    patients = read_data()
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients[patient_id]

@app.post("/patients", response_model=PatientResponse, status_code=201)
async def create_patient(patient: PatientCreate):
    patients = read_data()
    if patient.id in patients:
        raise HTTPException(status_code=409, detail="Patient ID already exists")
    patients[patient.id] = patient.dict()
    write_data(patients)
    return patient

@app.put("/patients/{patient_id}", response_model=PatientResponse)
async def update_patient(patient_id: str, update_data: PatientUpdate):
    patients = read_data()
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    current = patients[patient_id]
    # Update only provided fields
    for field, value in update_data.dict(exclude_unset=True).items():
        current[field] = value
    patients[patient_id] = current
    write_data(patients)
    return current

@app.delete("/patients/{patient_id}", status_code=204)
async def delete_patient(patient_id: str):
    patients = read_data()
    if patient_id not in patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    del patients[patient_id]
    write_data(patients)
    return