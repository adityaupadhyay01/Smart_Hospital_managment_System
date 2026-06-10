# models/patient.py — Patient class (inherits Person)

from datetime import datetime
from models.person import Person

class Patient(Person):
    """Represents a hospital patient. Inherits from Person."""

    def __init__(self, name, age, gender, phone, address, blood_group="Unknown"):
        super().__init__(name, age, gender, phone, address)
        self._blood_group        = blood_group
        self._medical_history: list = []      # list of condition strings
        self._registration_date  = datetime.now().strftime("%Y-%m-%d")

    # Polymorphism: overrides abstract method
    def get_role(self) -> str:
        return "Patient"

    @property
    def blood_group(self):        return self._blood_group
    @property
    def medical_history(self):    return self._medical_history
    @property
    def registration_date(self):  return self._registration_date

    def add_history(self, condition: str):
        self._medical_history.append(condition)

    def update(self, name=None, age=None, phone=None, address=None, blood_group=None):
        if name:        self.name    = name
        if age:         self.age     = int(age)
        if phone:       self.phone   = phone
        if address:     self.address = address
        if blood_group: self._blood_group = blood_group

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "blood_group":       self._blood_group,
            "medical_history":   self._medical_history,
            "registration_date": self._registration_date,
        })
        return d

    @staticmethod
    def from_dict(data: dict) -> "Patient":
        p = Patient(data["name"], data["age"], data["gender"],
                    data["phone"], data["address"],
                    data.get("blood_group", "Unknown"))
        p._id                = data["id"]
        p._medical_history   = data.get("medical_history", [])
        p._registration_date = data.get("registration_date", "")
        return p