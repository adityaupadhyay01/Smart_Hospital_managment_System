# =============================================================================
# models/lab_report.py — LabReport class
# =============================================================================

import uuid
from datetime import datetime


class LabReport:
    """Represents a laboratory test report for a patient."""

    def __init__(self, patient_id: str, test_name: str,
                 technician: str = "Lab Tech"):
        self._id         = str(uuid.uuid4())[:8].upper()
        self._patient_id = patient_id
        self._test_name  = test_name
        self._technician = technician
        self._result     = "Pending"
        self._remarks    = ""
        self._date       = datetime.now().strftime("%Y-%m-%d")
        self._cost       = 0.0
        self._status     = "Pending"

    @property
    def id(self):          return self._id
    @property
    def patient_id(self):  return self._patient_id
    @property
    def test_name(self):   return self._test_name
    @property
    def result(self):      return self._result
    @property
    def status(self):      return self._status
    @property
    def cost(self):        return self._cost
    @property
    def date(self):        return self._date

    def set_result(self, result: str, remarks: str = "", cost: float = 0.0):
        self._result  = result
        self._remarks = remarks
        self._cost    = float(cost)
        self._status  = "Completed"
        print(f"  Lab report {self._id} updated with result.")

    def __str__(self):
        return (f"Lab Report ID={self._id} | Patient={self._patient_id} | "
                f"Test={self._test_name} | Result={self._result} | "
                f"Status={self._status} | Date={self._date} | Cost=₹{self._cost:.2f}")

    def to_dict(self) -> dict:
        return {
            "id":          self._id,
            "patient_id":  self._patient_id,
            "test_name":   self._test_name,
            "technician":  self._technician,
            "result":      self._result,
            "remarks":     self._remarks,
            "date":        self._date,
            "cost":        self._cost,
            "status":      self._status,
        }

    @staticmethod
    def from_dict(data: dict) -> "LabReport":
        lr = LabReport(data["patient_id"], data["test_name"],
                       data.get("technician", "Lab Tech"))
        lr._id       = data["id"]
        lr._result   = data.get("result", "Pending")
        lr._remarks  = data.get("remarks", "")
        lr._date     = data.get("date", "")
        lr._cost     = data.get("cost", 0.0)
        lr._status   = data.get("status", "Pending")
        return lr
