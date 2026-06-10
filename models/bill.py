# models/bill.py — Bill class

import uuid
from datetime import datetime

class Bill:
    """Represents a patient bill with itemized charges."""

    def __init__(self, patient_id: str):
        self._id                   = str(uuid.uuid4())[:8].upper()
        self._patient_id           = patient_id
        self._consultation_charges = 0.0
        self._medicine_charges     = 0.0
        self._lab_charges          = 0.0
        self._other_charges        = 0.0
        self._discount             = 0.0
        self._date                 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._is_paid              = False
        self._items                = []   # [{"description": str, "amount": float}]

    @property
    def id(self):          return self._id
    @property
    def patient_id(self):  return self._patient_id
    @property
    def is_paid(self):     return self._is_paid

    def add_consultation(self, amount: float, doctor_name: str = ""):
        self._consultation_charges += amount
        self._items.append({"description": f"Consultation - Dr.{doctor_name}",
                             "amount": amount})

    def add_medicine_charge(self, amount: float, medicine_name: str = ""):
        self._medicine_charges += amount
        self._items.append({"description": f"Medicine - {medicine_name}",
                             "amount": amount})

    def add_lab_charge(self, amount: float, test_name: str = ""):
        self._lab_charges += amount
        self._items.append({"description": f"Lab Test - {test_name}",
                             "amount": amount})

    def add_other_charge(self, amount: float, description: str = "Miscellaneous"):
        self._other_charges += amount
        self._items.append({"description": description, "amount": amount})

    def set_discount(self, discount: float):
        self._discount = float(discount)

    def calculate_total(self) -> float:
        gross = (self._consultation_charges + self._medicine_charges +
                 self._lab_charges + self._other_charges)
        return round(gross - self._discount, 2)

    def mark_paid(self):
        self._is_paid = True
        print(f"  Bill {self._id} marked as PAID. Total: ₹{self.calculate_total():.2f}")

    def generate_receipt(self, patient_name: str = "") -> str:
        """Returns a formatted receipt string."""
        sep   = "=" * 55
        gross = (self._consultation_charges + self._medicine_charges +
                 self._lab_charges + self._other_charges)
        lines = [
            sep,
            "       SMART HOSPITAL MANAGEMENT SYSTEM",
            "              PAYMENT RECEIPT",
            sep,
            f"  Receipt No : {self._id}",
            f"  Date       : {self._date}",
            f"  Patient ID : {self._patient_id}",
            f"  Patient    : {patient_name}",
            sep,
            f"  {'DESCRIPTION':<35} {'AMOUNT':>10}",
            "-" * 55,
        ]
        for item in self._items:
            lines.append(f"  {item['description']:<35} ₹{item['amount']:>8.2f}")
        lines += [
            "-" * 55,
            f"  {'Subtotal':<35} ₹{gross:>8.2f}",
            f"  {'Discount':<35} ₹{self._discount:>8.2f}",
            sep,
            f"  {'TOTAL AMOUNT':<35} ₹{self.calculate_total():>8.2f}",
            f"  Status: {'✔ PAID' if self._is_paid else '✘ UNPAID'}",
            sep,
            "     Thank you for choosing Smart Hospital!",
            sep,
        ]
        return "\n".join(lines)

    def __str__(self):
        return (f"Bill ID={self._id} | Patient={self._patient_id} | "
                f"Total=₹{self.calculate_total():.2f} | Paid={self._is_paid}")

    def to_dict(self) -> dict:
        return {
            "id":                    self._id,
            "patient_id":            self._patient_id,
            "consultation_charges":  self._consultation_charges,
            "medicine_charges":      self._medicine_charges,
            "lab_charges":           self._lab_charges,
            "other_charges":         self._other_charges,
            "discount":              self._discount,
            "date":                  self._date,
            "is_paid":               self._is_paid,
            "items":                 self._items,
        }

    @staticmethod
    def from_dict(data: dict) -> "Bill":
        b = Bill(data["patient_id"])
        b._id                   = data["id"]
        b._consultation_charges = data.get("consultation_charges", 0.0)
        b._medicine_charges     = data.get("medicine_charges", 0.0)
        b._lab_charges          = data.get("lab_charges", 0.0)
        b._other_charges        = data.get("other_charges", 0.0)
        b._discount             = data.get("discount", 0.0)
        b._date                 = data.get("date", "")
        b._is_paid              = data.get("is_paid", False)
        b._items                = data.get("items", [])
        return b