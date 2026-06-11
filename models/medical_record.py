import uuid
from datetime import datetime

class MedicalRecord:
    def __init__(self, patient_id, doctor_id):
        self._id = str(uuid.uuid4())[:8].upper()
        self._patient_id, self._doctor_id = patient_id, doctor_id
        self._date = datetime.now().strftime("%Y-%m-%d")
        self._diagnoses, self._prescriptions, self._notes = [], [], ""

    @property
    def id(self):            return self._id
    @property
    def patient_id(self):    return self._patient_id
    @property
    def doctor_id(self):     return self._doctor_id
    @property
    def date(self):          return self._date
    @property
    def diagnoses(self):     return self._diagnoses
    @property
    def prescriptions(self): return self._prescriptions

    def add_diagnosis(self, d):
        self._diagnoses.append(d); print(f"  Diagnosis '{d}' added.")
    def add_prescription(self, med, dosage, days):
        self._prescriptions.append(dict(medicine=med, dosage=dosage, days=days))
        print(f"  Rx '{med}' added.")
    def add_notes(self, n): self._notes = n

    def __str__(self):
        return f"Record {self._id} | P:{self._patient_id} D:{self._doctor_id} | {self._date} | Dx:{len(self._diagnoses)}"

    def to_dict(self):
        return dict(id=self._id, patient_id=self._patient_id, doctor_id=self._doctor_id,
                    date=self._date, diagnoses=self._diagnoses,
                    prescriptions=self._prescriptions, notes=self._notes)

    @staticmethod
    def from_dict(data):
        mr = MedicalRecord(data["patient_id"], data["doctor_id"])
        mr._id = data["id"]; mr._date = data.get("date","")
        mr._diagnoses = data.get("diagnoses",[]); mr._prescriptions = data.get("prescriptions",[])
        mr._notes = data.get("notes",""); return mr
