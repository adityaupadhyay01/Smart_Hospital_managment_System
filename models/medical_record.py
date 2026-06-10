# =============================================================================
# models/medical_record.py — MedicalRecord class
# =============================================================================

import uuid
from datetime import datetime


class MedicalRecord:
    """Stores diagnosis and prescription data for a patient visit."""

    def __init__(self, patient_id: str, doctor_id: str):
        self._id            = str(uuid.uuid4())[:8].upper()
        self._patient_id    = patient_id
        self._doctor_id     = doctor_id
        self._date          = datetime.now().strftime("%Y-%m-%d")
        self._diagnoses     = []      # list of strings
        self._prescriptions = []      # list of {"medicine", "dosage", "days"}
        self._notes         = ""

    @property
    def id(self):             return self._id
    @property
    def patient_id(self):     return self._patient_id
    @property
    def doctor_id(self):      return self._doctor_id
    @property
    def date(self):           return self._date
    @property
    def diagnoses(self):      return self._diagnoses
    @property
    def prescriptions(self):  return self._prescriptions

    def add_diagnosis(self, diagnosis: str):
        self._diagnoses.append(diagnosis)
        print(f"  Diagnosis '{diagnosis}' added to record {self._id}.")

    def add_prescription(self, medicine: str, dosage: str, days: int):
        self._prescriptions.append({
            "medicine": medicine,
            "dosage":   dosage,
            "days":     days,
        })
        print(f"  Prescription for '{medicine}' added.")

    def add_notes(self, notes: str):
        self._notes = notes

    def __str__(self):
        diag  = ", ".join(self._diagnoses) if self._diagnoses else "None"
        presc = len(self._prescriptions)
        return (f"Record ID={self._id} | Patient={self._patient_id} | "
                f"Doctor={self._doctor_id} | Date={self._date} | "
                f"Diagnoses={diag} | Prescriptions={presc}")

    def to_dict(self) -> dict:
        return {
            "id":            self._id,
            "patient_id":    self._patient_id,
            "doctor_id":     self._doctor_id,
            "date":          self._date,
            "diagnoses":     self._diagnoses,
            "prescriptions": self._prescriptions,
            "notes":         self._notes,
        }

    @staticmethod
    def from_dict(data: dict) -> "MedicalRecord":
        mr = MedicalRecord(data["patient_id"], data["doctor_id"])
        mr._id            = data["id"]
        mr._date          = data.get("date", "")
        mr._diagnoses     = data.get("diagnoses", [])
        mr._prescriptions = data.get("prescriptions", [])
        mr._notes         = data.get("notes", "")
        return mr
