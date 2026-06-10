# models/doctor.py — Doctor class (inherits Person)

from models.person import Person

class Doctor(Person):
    """Represents a hospital doctor. Inherits from Person."""

    def __init__(self, name, age, gender, phone, address,
                 specialization="General", consultation_fee=500.0):
        super().__init__(name, age, gender, phone, address)
        self._specialization    = specialization
        self._consultation_fee  = float(consultation_fee)
        self._available_slots   = []      # list of datetime strings
        self._department        = specialization

    def get_role(self) -> str:
        return "Doctor"

    @property
    def specialization(self):    return self._specialization
    @property
    def consultation_fee(self):  return self._consultation_fee
    @property
    def available_slots(self):   return self._available_slots
    @property
    def department(self):        return self._department

    @consultation_fee.setter
    def consultation_fee(self, value):
        if value < 0:
            raise ValueError("Fee cannot be negative.")
        self._consultation_fee = float(value)

    def add_slot(self, slot: str):
        if slot not in self._available_slots:
            self._available_slots.append(slot)
            print(f"  Slot '{slot}' added for Dr. {self._name}.")
        else:
            print(f"  Slot '{slot}' already exists.")

    def remove_slot(self, slot: str):
        if slot in self._available_slots:
            self._available_slots.remove(slot)
        else:
            print(f"  Slot '{slot}' not found.")

    def update(self, name=None, phone=None, address=None,
               specialization=None, fee=None):
        if name:            self.name = name
        if phone:           self.phone = phone
        if address:         self.address = address
        if specialization:  self._specialization = specialization
        if fee is not None: self.consultation_fee = fee

    def to_dict(self) -> dict:
        d = super().to_dict()
        d.update({
            "specialization":   self._specialization,
            "consultation_fee": self._consultation_fee,
            "available_slots":  self._available_slots,
            "department":       self._department,
        })
        return d

    @staticmethod
    def from_dict(data: dict) -> "Doctor":
        doc = Doctor(data["name"], data["age"], data["gender"],
                     data["phone"], data["address"],
                     data.get("specialization", "General"),
                     data.get("consultation_fee", 500.0))
        doc._id              = data["id"]
        doc._available_slots = data.get("available_slots", [])
        doc._department      = data.get("department", doc._specialization)
        return doc