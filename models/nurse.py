# models/nurse.py — Nurse class (inherits Person)

from models.person import Person

class Nurse(Person):
    """Represents a hospital nurse. Inherits from Person."""

    SHIFTS = ["Morning (6AM-2PM)", "Evening (2PM-10PM)", "Night (10PM-6AM)"]

    def __init__(self, name, age, gender, phone, address,
                 department="General Ward", shift="Morning (6AM-2PM)"):
        super().__init__(name, age, gender, phone, address)
        self._department = department
        self._shift      = shift if shift in Nurse.SHIFTS else Nurse.SHIFTS[0]

    def get_role(self) -> str:
        return "Nurse"

    @property
    def department(self): return self._department
    @property
    def shift(self):      return self._shift

    def assign_department(self, dept: str):
        self._department = dept
        print(f"  Nurse {self._name} assigned to {dept}.")

    def change_shift(self, shift: str):
        if shift in Nurse.SHIFTS:
            self._shift = shift
            print(f"  Shift updated to '{shift}' for Nurse {self._name}.")
        else:
            print(f"  Invalid shift. Choose from: {Nurse.SHIFTS}")

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({"department": self._department, "shift": self._shift})
        return d

    @staticmethod
    def from_dict(data: dict) -> "Nurse":
        n = Nurse(data["name"], data["age"], data["gender"],
                  data["phone"], data["address"],
                  data.get("department", "General Ward"),
                  data.get("shift", Nurse.SHIFTS[0]))
        n._id = data["id"]
        return n