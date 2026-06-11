import uuid
from datetime import datetime

class Bill:
    def __init__(self, patient_id):
        self._id = str(uuid.uuid4())[:8].upper()
        self._patient_id = patient_id
        self._consultation_charges = self._medicine_charges = self._lab_charges = self._other_charges = 0.0
        self._discount = 0.0
        self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._is_paid = False
        self._items = []

    @property
    def id(self):         return self._id
    @property
    def patient_id(self): return self._patient_id
    @property
    def is_paid(self):    return self._is_paid

    def _add(self, bucket, amount, label):
        setattr(self, bucket, getattr(self, bucket) + amount)
        self._items.append(dict(description=label, amount=amount))

    def add_consultation(self, amt, doc=""):
        self._consultation_charges += amt; self._items.append(dict(description=f"Consultation - Dr.{doc}", amount=amt))
    def add_medicine_charge(self, amt, med=""):
        self._medicine_charges += amt; self._items.append(dict(description=f"Medicine - {med}", amount=amt))
    def add_lab_charge(self, amt, test=""):
        self._lab_charges += amt; self._items.append(dict(description=f"Lab - {test}", amount=amt))
    def add_other_charge(self, amt, desc="Misc"):
        self._other_charges += amt; self._items.append(dict(description=desc, amount=amt))

    def set_discount(self, d): self._discount = float(d)

    def _gross(self):
        return self._consultation_charges + self._medicine_charges + self._lab_charges + self._other_charges

    def calculate_total(self): return round(self._gross() - self._discount, 2)

    def mark_paid(self): self._is_paid = True; print(f"  Bill {self._id} PAID ₹{self.calculate_total():.2f}")

    def generate_receipt(self, pname=""):
        S = "=" * 50; H = "-" * 50
        lines = [S, "    SMART HOSPITAL — RECEIPT", S,
                 f"  Receipt : {self._id}", f"  Date    : {self._date}",
                 f"  Patient : {pname} ({self._patient_id})", S,
                 f"  {'ITEM':<32} {'AMOUNT':>10}", H]
        lines += [f"  {i['description']:<32} ₹{i['amount']:>8.2f}" for i in self._items]
        lines += [H, f"  {'Subtotal':<32} ₹{self._gross():>8.2f}",
                  f"  {'Discount':<32} ₹{self._discount:>8.2f}", S,
                  f"  {'TOTAL':<32} ₹{self.calculate_total():>8.2f}",
                  f"  {'✔ PAID' if self._is_paid else '✘ UNPAID'}", S]
        return "\n".join(lines)

    def __str__(self):
        return f"Bill {self._id} | P:{self._patient_id} | ₹{self.calculate_total():.2f} | Paid:{self._is_paid}"

    def to_dict(self):
        return dict(id=self._id, patient_id=self._patient_id,
                    consultation_charges=self._consultation_charges,
                    medicine_charges=self._medicine_charges,
                    lab_charges=self._lab_charges, other_charges=self._other_charges,
                    discount=self._discount, date=self._date, is_paid=self._is_paid, items=self._items)

    @staticmethod
    def from_dict(data):
        b = Bill(data["patient_id"]); b._id = data["id"]
        b._consultation_charges = data.get("consultation_charges",0.0)
        b._medicine_charges = data.get("medicine_charges",0.0)
        b._lab_charges = data.get("lab_charges",0.0)
        b._other_charges = data.get("other_charges",0.0)
        b._discount = data.get("discount",0.0); b._date = data.get("date","")
        b._is_paid = data.get("is_paid",False); b._items = data.get("items",[]); return b
