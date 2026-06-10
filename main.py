import json
import os
import uuid
import functools
from abc import ABC, abstractmethod
from datetime import datetime, date

# JSON FILE PATHS
PATIENTS_FILE    = "patients.json"
DOCTORS_FILE     = "doctors.json"
APPOINTMENTS_FILE = "appointments.json"
MEDICINES_FILE   = "medicines.json"
RECORDS_FILE     = "records.json"
BILLS_FILE       = "bills.json"

#UTILITY: FILE HANDLING

def save_data(filename: str, data: list) -> None:
    """Save a list of dictionaries to a JSON file."""
    try:
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"  Data saved to {filename}")
    except IOError as e:
        print(f"  Failed to save {filename}: {e}")

def load_data(filename: str) -> list:
    """Load a list of dictionaries from a JSON file. Returns [] if not found."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"  [✘] Failed to load {filename}: {e}")
        return []

# Hospital Data and Folder Tree
# Root folder for all individual record files
_DATA_ROOT = "hospital_data"

def _ensure_dir(subfolder: str) -> str:
    """Create hospital_data/<subfolder> if it does not exist. Returns the path."""
    path = os.path.join(_DATA_ROOT, subfolder)
    os.makedirs(path, exist_ok=True)
    return path

def _write_file(filepath: str, content: str) -> None:
    """Write *content* to *filepath*, overwriting any previous version."""
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            fh.write(content)
        print(f"  [FILE] Saved → {filepath}")
    except IOError as e:
        print(f"  [FILE ✘] Could not write {filepath}: {e}")

def _sep(char: str = "=", width: int = 45) -> str:
    return char * width

def save_patient_to_file(patient) -> None:
    """Create/overwrite  hospital_data/patients/patient_<id>.txt"""
    folder   = _ensure_dir("patients")
    filepath = os.path.join(folder, f"patient_{patient.id}.txt")
    history  = "\n".join(f"    • {h}" for h in patient.medical_history) or "    None"
    content  = (
        f"{_sep()}\n"
        f"           PATIENT DETAILS\n"
        f"{_sep()}\n"
        f"  Patient ID   : {patient.id}\n"
        f"  Name         : {patient.name}\n"
        f"  Age          : {patient.age}\n"
        f"  Gender       : {patient.gender}\n"
        f"  Phone        : {patient.phone}\n"
        f"  Address      : {patient.address}\n"
        f"  Blood Group  : {patient.blood_group}\n"
        f"  Registered   : {patient.registration_date}\n"
        f"{_sep('-')}\n"
        f"  Medical History:\n{history}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_doctor_to_file(doctor) -> None:
    """Create/overwrite  hospital_data/doctors/doctor_<id>.txt"""
    folder   = _ensure_dir("doctors")
    filepath = os.path.join(folder, f"doctor_{doctor.id}.txt")
    slots    = "\n".join(f"    • {s}" for s in doctor.available_slots) or "    None"
    content  = (
        f"{_sep()}\n"
        f"           DOCTOR DETAILS\n"
        f"{_sep()}\n"
        f"  Doctor ID      : {doctor.id}\n"
        f"  Name           : {doctor.name}\n"
        f"  Age            : {doctor.age}\n"
        f"  Gender         : {doctor.gender}\n"
        f"  Phone          : {doctor.phone}\n"
        f"  Address        : {doctor.address}\n"
        f"  Specialization : {doctor.specialization}\n"
        f"  Department     : {doctor.department}\n"
        f"  Consult. Fee   : ₹{doctor.consultation_fee:.2f}\n"
        f"{_sep('-')}\n"
        f"  Available Slots:\n{slots}\n"
        f"{_sep()}\n"
        f"  Last Updated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_nurse_to_file(nurse) -> None:
    """Create/overwrite  hospital_data/nurses/nurse_<id>.txt"""
    folder   = _ensure_dir("nurses")
    filepath = os.path.join(folder, f"nurse_{nurse.id}.txt")
    content  = (
        f"{_sep()}\n"
        f"           NURSE DETAILS\n"
        f"{_sep()}\n"
        f"  Nurse ID     : {nurse.id}\n"
        f"  Name         : {nurse.name}\n"
        f"  Age          : {nurse.age}\n"
        f"  Gender       : {nurse.gender}\n"
        f"  Phone        : {nurse.phone}\n"
        f"  Address      : {nurse.address}\n"
        f"  Department   : {nurse.department}\n"
        f"  Shift        : {nurse.shift}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_appointment_to_file(appt) -> None:
    """Create/overwrite  hospital_data/appointments/appointment_<id>.txt"""
    folder   = _ensure_dir("appointments")
    filepath = os.path.join(folder, f"appointment_{appt.id}.txt")
    content  = (
        f"{_sep()}\n"
        f"         APPOINTMENT DETAILS\n"
        f"{_sep()}\n"
        f"  Appointment ID : {appt.id}\n"
        f"  Patient ID     : {appt.patient_id}\n"
        f"  Doctor ID      : {appt.doctor_id}\n"
        f"  Date & Time    : {appt.date_time}\n"
        f"  Reason         : {appt.reason}\n"
        f"  Status         : {appt.status}\n"
        f"{_sep()}\n"
        f"  Last Updated   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_record_to_file(record) -> None:
    """Create/overwrite  hospital_data/records/record_<id>.txt"""
    folder   = _ensure_dir("records")
    filepath = os.path.join(folder, f"record_{record.id}.txt")
    diag_txt = "\n".join(f"    • {d}" for d in record.diagnoses) or "    None"
    presc_txt = "\n".join(
        f"    • {p['medicine']} | Dosage: {p['dosage']} | Days: {p['days']}"
        for p in record.prescriptions
    ) or "    None"
    content  = (
        f"{_sep()}\n"
        f"         MEDICAL RECORD DETAILS\n"
        f"{_sep()}\n"
        f"  Record ID    : {record.id}\n"
        f"  Patient ID   : {record.patient_id}\n"
        f"  Doctor ID    : {record.doctor_id}\n"
        f"  Date         : {record.date}\n"
        f"{_sep('-')}\n"
        f"  Diagnoses:\n{diag_txt}\n"
        f"{_sep('-')}\n"
        f"  Prescriptions:\n{presc_txt}\n"
        f"{_sep('-')}\n"
        f"  Notes        : {record._notes or 'None'}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_medicine_to_file(medicine) -> None:
    """Create/overwrite  hospital_data/medicines/medicine_<id>.txt"""
    folder   = _ensure_dir("medicines")
    filepath = os.path.join(folder, f"medicine_{medicine.id}.txt")
    status   = ("EXPIRED" if medicine.is_expired()
                else ("Available" if medicine.stock > 0 else "Out of Stock"))
    content  = (
        f"{_sep()}\n"
        f"          MEDICINE DETAILS\n"
        f"{_sep()}\n"
        f"  Medicine ID  : {medicine.id}\n"
        f"  Name         : {medicine.name}\n"
        f"  Category     : {medicine.category}\n"
        f"  Price        : ₹{medicine.price:.2f}\n"
        f"  Stock        : {medicine.stock} units\n"
        f"  Expiry Date  : {medicine.expiry_date}\n"
        f"  Manufacturer : {medicine.manufacturer}\n"
        f"  Status       : {status}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_bill_to_file(bill, patient_name: str = "") -> None:
    """Create/overwrite  hospital_data/bills/bill_<id>.txt"""
    folder   = _ensure_dir("bills")
    filepath = os.path.join(folder, f"bill_{bill.id}.txt")
    items_txt = "\n".join(
        f"    {item['description']:<32} ₹{item['amount']:>8.2f}"
        for item in bill._items
    ) or "    (no items)"
    gross = (bill._consultation_charges + bill._medicine_charges +
             bill._lab_charges + bill._other_charges)
    content  = (
        f"{_sep()}\n"
        f"            BILL / RECEIPT\n"
        f"{_sep()}\n"
        f"  Bill ID      : {bill.id}\n"
        f"  Patient ID   : {bill.patient_id}\n"
        f"  Patient Name : {patient_name}\n"
        f"  Date         : {bill._date}\n"
        f"{_sep('-')}\n"
        f"  ITEMIZED CHARGES:\n{items_txt}\n"
        f"{_sep('-')}\n"
        f"  Subtotal     : ₹{gross:.2f}\n"
        f"  Discount     : ₹{bill._discount:.2f}\n"
        f"  TOTAL        : ₹{bill.calculate_total():.2f}\n"
        f"  Status       : {'✔ PAID' if bill.is_paid else '✘ UNPAID'}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

def save_lab_report_to_file(lab_report) -> None:
    """Create/overwrite  hospital_data/lab_reports/labreport_<id>.txt"""
    folder   = _ensure_dir("lab_reports")
    filepath = os.path.join(folder, f"labreport_{lab_report.id}.txt")
    content  = (
        f"{_sep()}\n"
        f"          LAB REPORT DETAILS\n"
        f"{_sep()}\n"
        f"  Report ID    : {lab_report.id}\n"
        f"  Patient ID   : {lab_report.patient_id}\n"
        f"  Test Name    : {lab_report.test_name}\n"
        f"  Technician   : {lab_report._technician}\n"
        f"  Date         : {lab_report.date}\n"
        f"{_sep('-')}\n"
        f"  Result       : {lab_report.result}\n"
        f"  Remarks      : {lab_report._remarks or 'None'}\n"
        f"  Cost         : ₹{lab_report.cost:.2f}\n"
        f"  Status       : {lab_report.status}\n"
        f"{_sep()}\n"
        f"  Last Updated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"{_sep()}\n"
    )
    _write_file(filepath, content)

# DECORATOR: Logging

def log_action(func):
    """Decorator that logs every action with a timestamp."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n  [LOG {timestamp}] Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [LOG {timestamp}] Completed: {func.__name__}")
        return result
    return wrapper

# ABSTRACT BASE CLASS: Person

class Person(ABC):
    """
    Abstract base class representing a generic person.
    Enforces implementation of get_role() in all derived classes.
    """

    def __init__(self, name: str, age: int, gender: str, phone: str, address: str):
        # Encapsulation: private attributes with underscore convention
        self._id      = str(uuid.uuid4())[:8].upper()
        self._name    = name
        self._age     = age
        self._gender  = gender
        self._phone   = phone
        self._address = address

    # Getters
    @property
    def id(self):       return self._id
    @property
    def name(self):     return self._name
    @property
    def age(self):      return self._age
    @property
    def gender(self):   return self._gender
    @property
    def phone(self):    return self._phone
    @property
    def address(self):  return self._address

    # Setters
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @age.setter
    def age(self, value):
        if not (0 < value < 150):
            raise ValueError("Age must be between 1 and 149.")
        self._age = value

    @phone.setter
    def phone(self, value):
        self._phone = value

    @address.setter
    def address(self, value):
        self._address = value

    # Abstract Method (Abstraction)
    @abstractmethod
    def get_role(self) -> str:
        """Every person must declare their role."""

    # Magic Method
    def __str__(self):
        return (f"[{self.get_role()}] ID={self._id} | Name={self._name} | "
                f"Age={self._age} | Gender={self._gender} | Phone={self._phone}")

    def to_dict(self) -> dict:
        """Serialize common person fields to a dictionary."""
        return {
            "id":      self._id,
            "name":    self._name,
            "age":     self._age,
            "gender":  self._gender,
            "phone":   self._phone,
            "address": self._address,
            "role":    self.get_role(),
        }

    @classmethod
    def from_dict_base(cls, data: dict):
        """Restore base fields from dictionary (used by subclasses)."""
        return data  

# DERIVED CLASS: Patient

class Patient(Person):
    """Represents a hospital patient. Inherits from Person."""

    def __init__(self, name, age, gender, phone, address, blood_group="Unknown"):
        super().__init__(name, age, gender, phone, address)
        self._blood_group  = blood_group
        self._medical_history: list = []   
        self._registration_date = datetime.now().strftime("%Y-%m-%d")

    # Polymorphism: overrides abstract method
    def get_role(self) -> str:
        return "Patient"

    @property
    def blood_group(self):         return self._blood_group
    @property
    def medical_history(self):     return self._medical_history
    @property
    def registration_date(self):   return self._registration_date

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
                    data["phone"], data["address"], data.get("blood_group", "Unknown"))
        p._id               = data["id"]
        p._medical_history  = data.get("medical_history", [])
        p._registration_date = data.get("registration_date", "")
        return p

# DERIVED CLASS: Doctor

class Doctor(Person):
    """Represents a hospital doctor. Inherits from Person."""

    def __init__(self, name, age, gender, phone, address,
                 specialization="General", consultation_fee=500.0):
        super().__init__(name, age, gender, phone, address)
        self._specialization   = specialization
        self._consultation_fee = float(consultation_fee)
        self._available_slots  = []  
        self._department       = specialization

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
        if name:           self.name = name
        if phone:          self.phone = phone
        if address:        self.address = address
        if specialization: self._specialization = specialization
        if fee is not None:self.consultation_fee = fee

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

# DERIVED CLASS: Nurse

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

# CLASS: Appointment

class Appointment:
    """Represents a scheduled appointment between a patient and a doctor."""

    STATUS_BOOKED     = "Booked"
    STATUS_CANCELLED  = "Cancelled"
    STATUS_COMPLETED  = "Completed"
    STATUS_RESCHEDULED = "Rescheduled"

    def __init__(self, patient_id: str, doctor_id: str,
                 date_time: str, reason: str = "General Checkup"):
        self._id         = str(uuid.uuid4())[:8].upper()
        self._patient_id = patient_id
        self._doctor_id  = doctor_id
        self._date_time  = date_time   # "YYYY-MM-DD HH:MM"
        self._reason     = reason
        self._status     = Appointment.STATUS_BOOKED
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self):          return self._id
    @property
    def patient_id(self):  return self._patient_id
    @property
    def doctor_id(self):   return self._doctor_id
    @property
    def date_time(self):   return self._date_time
    @property
    def status(self):      return self._status
    @property
    def reason(self):      return self._reason

    def cancel(self):
        if self._status == Appointment.STATUS_BOOKED:
            self._status = Appointment.STATUS_CANCELLED
            print(f"  Appointment {self._id} cancelled.")
        else:
            print(f"  Cannot cancel. Current status: {self._status}")

    def reschedule(self, new_date_time: str):
        if self._status in (Appointment.STATUS_BOOKED, Appointment.STATUS_RESCHEDULED):
            self._date_time = new_date_time
            self._status    = Appointment.STATUS_RESCHEDULED
            print(f"  Appointment {self._id} rescheduled to {new_date_time}.")
        else:
            print(f"  Cannot reschedule. Current status: {self._status}")

    def complete(self):
        self._status = Appointment.STATUS_COMPLETED

    def __str__(self):
        return (f"Appt ID={self._id} | Patient={self._patient_id} | "
                f"Doctor={self._doctor_id} | DateTime={self._date_time} | "
                f"Status={self._status} | Reason={self._reason}")

    def to_dict(self) -> dict:
        return {
            "id":         self._id,
            "patient_id": self._patient_id,
            "doctor_id":  self._doctor_id,
            "date_time":  self._date_time,
            "reason":     self._reason,
            "status":     self._status,
            "created_at": self._created_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Appointment":
        a = Appointment(data["patient_id"], data["doctor_id"],
                        data["date_time"], data.get("reason", "General Checkup"))
        a._id         = data["id"]
        a._status     = data.get("status", Appointment.STATUS_BOOKED)
        a._created_at = data.get("created_at", "")
        return a

# CLASS: MedicalRecord

class MedicalRecord:
    """Stores diagnosis and prescription data for a patient visit."""

    def __init__(self, patient_id: str, doctor_id: str):
        self._id           = str(uuid.uuid4())[:8].upper()
        self._patient_id   = patient_id
        self._doctor_id    = doctor_id
        self._date         = datetime.now().strftime("%Y-%m-%d")
        self._diagnoses    = []   
        self._prescriptions = []  
        self._notes        = ""

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

    def add_diagnosis(self, diagnosis: str):
        self._diagnoses.append(diagnosis)
        print(f"  Diagnosis '{diagnosis}' added to record {self._id}.")

    def add_prescription(self, medicine: str, dosage: str, days: int):
        self._prescriptions.append({
            "medicine": medicine,
            "dosage":   dosage,
            "days":     days
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

# CLASS: Medicine

class Medicine:
    """Represents a medicine in the hospital pharmacy."""

    def __init__(self, name: str, category: str, price: float,
                 stock: int, expiry_date: str, manufacturer: str = "Unknown"):
        self._id           = str(uuid.uuid4())[:8].upper()
        self._name         = name
        self._category     = category
        self._price        = float(price)
        self._stock        = int(stock)
        self._expiry_date  = expiry_date  # "YYYY-MM-DD"
        self._manufacturer = manufacturer

    @property
    def id(self):            return self._id
    @property
    def name(self):          return self._name
    @property
    def category(self):      return self._category
    @property
    def price(self):         return self._price
    @property
    def stock(self):         return self._stock
    @property
    def expiry_date(self):   return self._expiry_date
    @property
    def manufacturer(self):  return self._manufacturer

    def update_stock(self, quantity: int):
        """Add or subtract stock. Pass negative to reduce."""
        if self._stock + quantity < 0:
            raise ValueError(f"Insufficient stock. Available: {self._stock}")
        self._stock += quantity
        print(f"  Stock for '{self._name}' updated to {self._stock}.")

    def is_expired(self) -> bool:
        try:
            exp = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
            return exp < date.today()
        except ValueError:
            return False

    def is_available(self) -> bool:
        return self._stock > 0 and not self.is_expired()

    def __str__(self):
        status = "EXPIRED" if self.is_expired() else ("Available" if self._stock > 0 else "Out of Stock")
        return (f"Medicine ID={self._id} | Name={self._name} | "
                f"Category={self._category} | Price=₹{self._price:.2f} | "
                f"Stock={self._stock} | Expiry={self._expiry_date} | Status={status}")

    def to_dict(self) -> dict:
        return {
            "id":           self._id,
            "name":         self._name,
            "category":     self._category,
            "price":        self._price,
            "stock":        self._stock,
            "expiry_date":  self._expiry_date,
            "manufacturer": self._manufacturer,
        }

    @staticmethod
    def from_dict(data: dict) -> "Medicine":
        m = Medicine(data["name"], data["category"], data["price"],
                     data["stock"], data["expiry_date"],
                     data.get("manufacturer", "Unknown"))
        m._id = data["id"]
        return m

#CLASS: LabReport

class LabReport:
    """Represents a laboratory test report for a patient."""

    def __init__(self, patient_id: str, test_name: str,
                 technician: str = "Lab Tech"):
        self._id          = str(uuid.uuid4())[:8].upper()
        self._patient_id  = patient_id
        self._test_name   = test_name
        self._technician  = technician
        self._result      = "Pending"
        self._remarks     = ""
        self._date        = datetime.now().strftime("%Y-%m-%d")
        self._cost        = 0.0
        self._status      = "Pending"

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

#CLASS: Bill

class Bill:
    """Represents a patient bill with itemized charges."""

    def __init__(self, patient_id: str):
        self._id                  = str(uuid.uuid4())[:8].upper()
        self._patient_id          = patient_id
        self._consultation_charges = 0.0
        self._medicine_charges    = 0.0
        self._lab_charges         = 0.0
        self._other_charges       = 0.0
        self._discount            = 0.0
        self._date                = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._is_paid             = False
        self._items               = [] 

    @property
    def id(self):           return self._id
    @property
    def patient_id(self):   return self._patient_id
    @property
    def is_paid(self):      return self._is_paid

    def add_consultation(self, amount: float, doctor_name: str = ""):
        self._consultation_charges += amount
        self._items.append({"description": f"Consultation - Dr.{doctor_name}", "amount": amount})

    def add_medicine_charge(self, amount: float, medicine_name: str = ""):
        self._medicine_charges += amount
        self._items.append({"description": f"Medicine - {medicine_name}", "amount": amount})

    def add_lab_charge(self, amount: float, test_name: str = ""):
        self._lab_charges += amount
        self._items.append({"description": f"Lab Test - {test_name}", "amount": amount})

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
        sep = "=" * 55
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
            f"  {'Subtotal':<35} ₹{(self._consultation_charges + self._medicine_charges + self._lab_charges + self._other_charges):>8.2f}",
            f"  {'Discount':<35} ₹{self._discount:>8.2f}",
            sep,
            f"  {'TOTAL AMOUNT':<35} ₹{self.calculate_total():>8.2f}",
            f"  Status: {'PAID' if self._is_paid else '✘ UNPAID'}",
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
            "id":                     self._id,
            "patient_id":             self._patient_id,
            "consultation_charges":   self._consultation_charges,
            "medicine_charges":       self._medicine_charges,
            "lab_charges":            self._lab_charges,
            "other_charges":          self._other_charges,
            "discount":               self._discount,
            "date":                   self._date,
            "is_paid":                self._is_paid,
            "items":                  self._items,
        }

    @staticmethod
    def from_dict(data: dict) -> "Bill":
        b = Bill(data["patient_id"])
        b._id                    = data["id"]
        b._consultation_charges  = data.get("consultation_charges", 0.0)
        b._medicine_charges      = data.get("medicine_charges", 0.0)
        b._lab_charges           = data.get("lab_charges", 0.0)
        b._other_charges         = data.get("other_charges", 0.0)
        b._discount              = data.get("discount", 0.0)
        b._date                  = data.get("date", "")
        b._is_paid               = data.get("is_paid", False)
        b._items                 = data.get("items", [])
        return b

#CLASS: Hospital  (Composition — owns lists of all entities)

class Hospital:
    """
    Central class for the Smart Hospital Management System.
    Uses Composition to manage Patients, Doctors, Nurses,
    Appointments, MedicalRecords, LabReports, Medicines, and Bills.
    """

    _instance = None  # For singleton-like behaviour

    def __init__(self, name: str = "Smart Hospital"):
        self._name         = name
        self._patients:     list[Patient]       = []
        self._doctors:      list[Doctor]        = []
        self._nurses:       list[Nurse]         = []
        self._appointments: list[Appointment]   = []
        self._records:      list[MedicalRecord] = []
        self._lab_reports:  list[LabReport]     = []
        self._medicines:    list[Medicine]      = []
        self._bills:        list[Bill]          = []

    # HELPER: find by id using recursion

    def _recursive_find(self, collection: list, target_id: str, index: int = 0):
        """
        Recursion: Traverse a list to find an item by its id attribute.
        Returns the item or None.
        """
        if index >= len(collection):
            return None
        if collection[index].id == target_id:
            return collection[index]
        return self._recursive_find(collection, target_id, index + 1)

    # PATIENT MANAGEMENT
    @log_action
    def register_patient(self):
        print("\n Register New Patient")
        try:
            name        = input("  Full Name       : ").strip()
            age         = int(input("  Age             : "))
            gender      = input("  Gender (M/F/O)  : ").strip()
            phone       = input("  Phone           : ").strip()
            address     = input("  Address         : ").strip()
            blood_group = input("  Blood Group     : ").strip()
            p = Patient(name, age, gender, phone, address, blood_group)
            self._patients.append(p)
            save_patient_to_file(p) 
            print(f"\n  Patient registered successfully! ID: {p.id}")
            print(f"  {p}")
        except ValueError as e:
            print(f"  Error: {e}")

    @log_action
    def update_patient(self):
        print("\n  Update Patient")
        pid = input("  Enter Patient ID: ").strip().upper()
        p = self._recursive_find(self._patients, pid)
        if not p:
            print("  Patient not found.")
            return
        print(f"  Current: {p}")
        print("  (Press Enter to keep current value)")
        try:
            name        = input("  New Name        : ").strip() or None
            age_str     = input("  New Age         : ").strip()
            age         = int(age_str) if age_str else None
            phone       = input("  New Phone       : ").strip() or None
            address     = input("  New Address     : ").strip() or None
            blood_group = input("  New Blood Group : ").strip() or None
            p.update(name, age, phone, address, blood_group)
            save_patient_to_file(p)           # ← overwrite patient file with latest data
            print("  Patient updated successfully.")
        except ValueError as e:
            print(f"  Error: {e}")

    def search_patient(self):
        print("\n Search Patient")
        print("  1. Search by ID")
        print("  2. Search by Name")
        choice = input("  Choice: ").strip()
        if choice == "1":
            pid = input("  Patient ID: ").strip().upper()
            p = self._recursive_find(self._patients, pid)
            if p:
                print(f"\n  {p}")
                print(f"  Blood Group: {p.blood_group} | Registered: {p.registration_date}")
                print(f"  Medical History: {', '.join(p.medical_history) if p.medical_history else 'None'}")
            else:
                print("  ✘ Patient not found.")
        elif choice == "2":
            name = input("  Patient Name (partial): ").strip().lower()
            # List comprehension to filter patients by name
            results = [p for p in self._patients if name in p.name.lower()]
            if results:
                for p in results:
                    print(f"  {p}")
            else:
                print("  No patients found with that name.")
        else:
            print("  Invalid choice.")

    def view_patient_history(self):
        print("\n  Patient History")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print(" Patient not found.")
            return
        print(f"\n  Patient: {patient.name} | ID: {patient.id}")
        print(f"  Blood Group: {patient.blood_group}")

        # Medical records
        records = [r for r in self._records if r.patient_id == pid]
        print(f"\n  Medical Records ({len(records)}):")
        for r in records:
            print(f"    {r}")
            for d in r.diagnoses:
                print(f"Diagnosis: {d}")
            for pr in r.prescriptions:
                print(f"Rx: {pr['medicine']} | Dosage: {pr['dosage']} | {pr['days']} days")

        # Lab reports
        labs = [l for l in self._lab_reports if l.patient_id == pid]
        print(f"\n  Lab Reports ({len(labs)}):")
        for l in labs:
            print(f"    {l}")

        # Bills
        bills = [b for b in self._bills if b.patient_id == pid]
        print(f"\n  Bills ({len(bills)}):")
        for b in bills:
            print(f"    {b}")

    def list_all_patients(self):
        if not self._patients:
            print("  No patients registered.")
            return
        print(f"\n All Patients ({len(self._patients)})")
        for p in self._patients:
            print(f"  {p}")

    # DOCTOR MANAGEMENT

    @log_action
    def add_doctor(self):
        print("\n  Add New Doctor")
        try:
            name   = input("  Full Name        : ").strip()
            age    = int(input("  Age              : "))
            gender = input("  Gender (M/F/O)   : ").strip()
            phone  = input("  Phone            : ").strip()
            address = input("  Address          : ").strip()
            spec   = input("  Specialization   : ").strip()
            fee    = float(input("  Consultation Fee : ₹"))
            d = Doctor(name, age, gender, phone, address, spec, fee)
            self._doctors.append(d)
            save_doctor_to_file(d)          
            print(f"\n  Doctor added! ID: {d.id}")
            print(f"  {d}")
        except ValueError as e:
            print(f"  Error: {e}")

    @log_action
    def update_doctor(self):
        print("\n Update Doctor")
        did = input("  Doctor ID: ").strip().upper()
        d = self._recursive_find(self._doctors, did)
        if not d:
            print(" Doctor not found.")
            return
        print(f"  Current: {d}")
        print("  (Press Enter to keep current value)")
        try:
            name  = input("  New Name  : ").strip() or None
            phone = input("  New Phone : ").strip() or None
            addr  = input("  New Addr  : ").strip() or None
            spec  = input("  New Spec  : ").strip() or None
            fee_s = input("  New Fee   : ").strip()
            fee   = float(fee_s) if fee_s else None
            d.update(name, phone, addr, spec, fee)
            save_doctor_to_file(d)        
            print(" Doctor updated.")
        except ValueError as e:
            print(f" Error: {e}")

    def manage_doctor_slots(self):
        print("\n  Manage Doctor Slots")
        did = input("  Doctor ID: ").strip().upper()
        d = self._recursive_find(self._doctors, did)
        if not d:
            print(" Doctor not found.")
            return
        print(f"  Doctor: {d.name} | Current Slots: {d.available_slots}")
        print("  1. Add Slot   2. Remove Slot   3. View Slots")
        ch = input("  Choice: ").strip()
        if ch == "1":
            slot = input("  Slot (YYYY-MM-DD HH:MM): ").strip()
            d.add_slot(slot)
        elif ch == "2":
            slot = input("  Slot to remove: ").strip()
            d.remove_slot(slot)
        elif ch == "3":
            slots = d.available_slots
            if slots:
                print("  Available Slots:")
                for s in slots:
                    print(f"    - {s}")
            else:
                print("  No slots available.")
        else:
            print("  Invalid choice.")

    def list_all_doctors(self):
        if not self._doctors:
            print("  No doctors registered.")
            return
        # Lambda: sort doctors by consultation fee
        sorted_docs = sorted(self._doctors, key=lambda d: d.consultation_fee)
        print(f"\n All Doctors (sorted by fee, {len(sorted_docs)})")
        for d in sorted_docs:
            print(f"  {d} | Spec={d.specialization} | Fee=₹{d.consultation_fee:.2f}")

    # NURSE MANAGEMENT

    @log_action
    def add_nurse(self):
        print("\n Add New Nurse")
        try:
            name   = input("  Full Name   : ").strip()
            age    = int(input("  Age         : "))
            gender = input("  Gender      : ").strip()
            phone  = input("  Phone       : ").strip()
            address = input("  Address     : ").strip()
            dept   = input("  Department  : ").strip()
            print("  Shifts:")
            for i, s in enumerate(Nurse.SHIFTS, 1):
                print(f"    {i}. {s}")
            sc = int(input("  Choose Shift (1-3): ").strip()) - 1
            shift = Nurse.SHIFTS[sc] if 0 <= sc < len(Nurse.SHIFTS) else Nurse.SHIFTS[0]
            n = Nurse(name, age, gender, phone, address, dept, shift)
            self._nurses.append(n)
            save_nurse_to_file(n)          
            print(f"\n  Nurse added ID: {n.id}")
        except (ValueError, IndexError) as e:
            print(f" Error: {e}")

    def assign_nurse_department(self):
        print("\n Assign Nurse Department")
        nid = input("  Nurse ID  : ").strip().upper()
        n = self._recursive_find(self._nurses, nid)
        if not n:
            print("  Nurse not found.")
            return
        dept = input("  Department: ").strip()
        n.assign_department(dept)
        save_nurse_to_file(n)             

    def manage_nurse_shift(self):
        print("\n Manage Nurse Shift")
        nid = input("  Nurse ID: ").strip().upper()
        n = self._recursive_find(self._nurses, nid)
        if not n:
            print("  Nurse not found.")
            return
        print(f"  Current Shift: {n.shift}")
        for i, s in enumerate(Nurse.SHIFTS, 1):
            print(f"  {i}. {s}")
        try:
            sc = int(input("  New Shift (1-3): ").strip()) - 1
            n.change_shift(Nurse.SHIFTS[sc])
            save_nurse_to_file(n)          
        except (ValueError, IndexError):
            print("  Invalid selection.")

    def list_all_nurses(self):
        if not self._nurses:
            print("  No nurses registered.")
            return
        print(f"\n  All Nurses ({len(self._nurses)})")
        for n in self._nurses:
            print(f"  {n} | Dept={n.department} | Shift={n.shift}")

    # APPOINTMENT MANAGEMENT

    @log_action
    def book_appointment(self):
        print("\n Book Appointment")
        try:
            pid = input("  Patient ID : ").strip().upper()
            patient = self._recursive_find(self._patients, pid)
            if not patient:
                print("  Patient not found.")
                return
            did = input("  Doctor ID  : ").strip().upper()
            doctor = self._recursive_find(self._doctors, did)
            if not doctor:
                print("  Doctor not found.")
                return
            print(f"  Available slots for Dr. {doctor.name}:")
            if not doctor.available_slots:
                print("  No slots available. Please add slots first.")
                return
            for i, s in enumerate(doctor.available_slots, 1):
                print(f"    {i}. {s}")
            sc = int(input("  Select Slot #: ").strip()) - 1
            if not (0 <= sc < len(doctor.available_slots)):
                print("  Invalid slot selection.")
                return
            slot   = doctor.available_slots[sc]
            reason = input("  Reason      : ").strip() or "General Checkup"
            appt = Appointment(pid, did, slot, reason)
            doctor.remove_slot(slot)
            self._appointments.append(appt)
            save_appointment_to_file(appt)  
            print(f"\n  Appointment booked! ID: {appt.id}")
            print(f"  {appt}")
        except (ValueError, IndexError) as e:
            print(f"  Error: {e}")

    @log_action
    def cancel_appointment(self):
        print("\n  Cancel Appointment")
        aid = input("  Appointment ID: ").strip().upper()
        appt = self._recursive_find(self._appointments, aid)
        if not appt:
            print("  ✘ Appointment not found.")
            return
        appt.cancel()
        save_appointment_to_file(appt)      
    @log_action
    def reschedule_appointment(self):
        print("\n  Reschedule Appointment")
        aid = input("  Appointment ID        : ").strip().upper()
        appt = self._recursive_find(self._appointments, aid)
        if not appt:
            print("  ✘ Appointment not found.")
            return
        new_dt = input("  New DateTime (YYYY-MM-DD HH:MM): ").strip()
        appt.reschedule(new_dt)
        save_appointment_to_file(appt)       
    def view_appointments(self):
        print("\n View Appointments")
        print("  1. All Appointments")
        print("  2. By Patient ID")
        print("  3. By Doctor ID")
        print("  4. Booked Only")
        ch = input("  Choice: ").strip()
        if ch == "1":
            appts = self._appointments
        elif ch == "2":
            pid = input("  Patient ID: ").strip().upper()
            appts = [a for a in self._appointments if a.patient_id == pid]
        elif ch == "3":
            did = input("  Doctor ID: ").strip().upper()
            appts = [a for a in self._appointments if a.doctor_id == did]
        elif ch == "4":
            appts = [a for a in self._appointments
                     if a.status == Appointment.STATUS_BOOKED]
        else:
            print(" Invalid choice.")
            return
        if not appts:
            print("  No appointments found.")
            return
        for a in appts:
            print(f"  {a}")

# MEDICAL RECORD

    @log_action
    def add_medical_record(self):
        print("\n  Create Medical Record")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  Patient not found.")
            return
        did = input("  Doctor ID : ").strip().upper()
        doctor = self._recursive_find(self._doctors, did)
        if not doctor:
            print("  Doctor not found.")
            return
        mr = MedicalRecord(pid, did)
        print("  Enter diagnoses (blank to stop):")
        while True:
            diag = input("    Diagnosis: ").strip()
            if not diag:
                break
            mr.add_diagnosis(diag)
            patient.add_history(diag)
        print("  Enter prescriptions (blank medicine name to stop):")
        while True:
            med = input("    Medicine  : ").strip()
            if not med:
                break
            try:
                dosage = input("    Dosage    : ").strip()
                days   = int(input("    Days      : ").strip())
                mr.add_prescription(med, dosage, days)
            except ValueError:
                print("    ✘ Invalid days value.")
        notes = input("  Additional Notes: ").strip()
        if notes:
            mr.add_notes(notes)
        self._records.append(mr)
        save_record_to_file(mr)  
        print(f"\n  Medical record created. ID: {mr.id}")

    def view_medical_records(self):
        print("\n  View Medical Records")
        pid = input("  Patient ID: ").strip().upper()
        records = [r for r in self._records if r.patient_id == pid]
        if not records:
            print("  No records found for this patient.")
            return
        for r in records:
            print(f"\n  {r}")
            print(f"    Notes: {r._notes or 'None'}")
            for d in r.diagnoses:
                print(f"    ✦ Diagnosis: {d}")
            for pr in r.prescriptions:
                print(f"    Rx: {pr['medicine']} | {pr['dosage']} | {pr['days']} days")

    # LABORATORY MANAGEMENT

    @log_action
    def create_lab_report(self):
        print("\n  Create Lab Report")
        pid = input("  Patient ID  : ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  Patient not found.")
            return
        test_name  = input("  Test Name   : ").strip()
        technician = input("  Technician  : ").strip() or "Lab Technician"
        lr = LabReport(pid, test_name, technician)
        add_result = input("  Add result now? (y/n): ").strip().lower()
        if add_result == "y":
            try:
                result  = input("  Result      : ").strip()
                remarks = input("  Remarks     : ").strip()
                cost    = float(input("  Cost (₹)    : "))
                lr.set_result(result, remarks, cost)
            except ValueError as e:
                print(f"  Error: {e}")
        self._lab_reports.append(lr)
        save_lab_report_to_file(lr)  
        print(f"\n  Lab report created. ID: {lr.id}")

    def view_lab_reports(self):
        print("\n  View Lab Reports")
        pid = input("  Patient ID: ").strip().upper()
        reports = [r for r in self._lab_reports if r.patient_id == pid]
        if not reports:
            print("  No lab reports found.")
            return
        for r in reports:
            print(f"  {r}")

    # PHARMACY MANAGEMENT

    @log_action
    def add_medicine(self):
        print("\n Add Medicine")
        try:
            name     = input("  Name         : ").strip()
            category = input("  Category     : ").strip()
            price    = float(input("  Price (₹)    : "))
            stock    = int(input("  Stock (units): "))
            expiry   = input("  Expiry Date (YYYY-MM-DD): ").strip()
            mfr      = input("  Manufacturer : ").strip() or "Unknown"
            m = Medicine(name, category, price, stock, expiry, mfr)
            self._medicines.append(m)
            save_medicine_to_file(m)      
            print(f"\n  Medicine added. ID: {m.id}")
            print(f"  {m}")
        except ValueError as e:
            print(f"  Error: {e}")

    def update_medicine_stock(self):
        print("\n Update Medicine Stock")
        mid = input("  Medicine ID    : ").strip().upper()
        med = self._recursive_find(self._medicines, mid)
        if not med:
            print(" Medicine not found.")
            return
        print(f"  Current Stock: {med.stock}")
        try:
            qty = int(input("  Quantity to Add (+) or Remove (-): "))
            med.update_stock(qty)
            save_medicine_to_file(med)     
        except ValueError as e:
            print(f" Error: {e}")

    def check_medicine_availability(self):
        print("\n Check Medicine Availability")
        name = input("  Medicine Name (partial): ").strip().lower()
        # List comprehension
        results = [m for m in self._medicines if name in m.name.lower()]
        if not results:
            print("  No medicines found.")
            return
        for m in results:
            status = "Available" if m.is_available() else ("Expired" if m.is_expired() else "Out of Stock")
            print(f"  {m.name} | Stock={m.stock} | Price=₹{m.price:.2f} | {status}")

    def check_expiry(self):
        print("\n Medicines Expiry Check")
        # Lambda + list comprehension to get expired medicines
        expired = list(filter(lambda m: m.is_expired(), self._medicines))
        if expired:
            print(f"  EXPIRED Medicines ({len(expired)}):")
            for m in expired:
                print(f"  {m.name} | Expiry: {m.expiry_date}")
        else:
            print("  No expired medicines.")

        # Near-expiry (within 30 days)
        near = []
        for m in self._medicines:
            if not m.is_expired():
                try:
                    exp = datetime.strptime(m.expiry_date, "%Y-%m-%d").date()
                    delta = (exp - date.today()).days
                    if 0 <= delta <= 30:
                        near.append((m, delta))
                except ValueError:
                    pass
        if near:
            print(f"\n  Near-Expiry (within 30 days) ({len(near)}):")
            for m, d in near:
                print(f"  {m.name} | Expiry: {m.expiry_date} ({d} days left)")

    def list_all_medicines(self):
        if not self._medicines:
            print("  No medicines in pharmacy.")
            return
        print(f"\n  All Medicines ({len(self._medicines)})")
        for m in self._medicines:
            print(f"  {m}")

    #BILLING MANAGEMENT

    @log_action
    def create_bill(self):
        print("\n  Create Bill")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print(" Patient not found.")
            return
        bill = Bill(pid)

        # Consultation charge
        add_cons = input("  Add consultation charge? (y/n): ").strip().lower()
        if add_cons == "y":
            try:
                did = input("  Doctor ID: ").strip().upper()
                doc = self._recursive_find(self._doctors, did)
                if doc:
                    bill.add_consultation(doc.consultation_fee, doc.name)
                    print(f"  Consultation fee ₹{doc.consultation_fee:.2f} added.")
                else:
                    amt = float(input("  Manual consultation amount: ₹"))
                    bill.add_consultation(amt)
            except ValueError as e:
                print(f" Error: {e}")

        # Medicine charges
        add_med = input("  Add medicine charges? (y/n): ").strip().lower()
        while add_med == "y":
            try:
                mid = input("  Medicine ID: ").strip().upper()
                med = self._recursive_find(self._medicines, mid)
                if not med:
                    print("  Medicine not found.")
                    break
                qty = int(input(f"  Quantity (Stock={med.stock}): "))
                med.update_stock(-qty)
                total_cost = med.price * qty
                bill.add_medicine_charge(total_cost, med.name)
                print(f"  ₹{total_cost:.2f} added for {med.name} x{qty}.")
            except ValueError as e:
                print(f" Error: {e}")
            add_med = input("  Add another medicine? (y/n): ").strip().lower()

        # Lab charges
        add_lab = input("  Add lab charges? (y/n): ").strip().lower()
        while add_lab == "y":
            try:
                lid = input("  Lab Report ID: ").strip().upper()
                lr  = self._recursive_find(self._lab_reports, lid)
                if lr:
                    bill.add_lab_charge(lr.cost, lr.test_name)
                    print(f"  Lab charge ₹{lr.cost:.2f} for '{lr.test_name}' added.")
                else:
                    print("  Lab report not found.")
            except ValueError as e:
                print(f" Error: {e}")
            add_lab = input("  Add another lab charge? (y/n): ").strip().lower()

        # Other charges
        add_other = input("  Add other charges? (y/n): ").strip().lower()
        if add_other == "y":
            try:
                desc = input("  Description: ").strip()
                amt  = float(input("  Amount (₹) : "))
                bill.add_other_charge(amt, desc)
            except ValueError as e:
                print(f" Error: {e}")

        # Discount
        disc_s = input("  Discount (₹, 0 for none): ").strip()
        try:
            disc = float(disc_s) if disc_s else 0.0
            bill.set_discount(disc)
        except ValueError:
            disc = 0.0

        self._bills.append(bill)
        save_bill_to_file(bill, patient.name)
        print(f"\n Bill created. ID: {bill.id}")
        print(f"  Total: ₹{bill.calculate_total():.2f}")

        pay_now = input("  Mark as paid now? (y/n): ").strip().lower()
        if pay_now == "y":
            bill.mark_paid()
            save_bill_to_file(bill, patient.name) 

    def view_bill(self):
        print("\n  View Bill")
        bid = input("  Bill ID: ").strip().upper()
        bill = self._recursive_find(self._bills, bid)
        if not bill:
            print("  Bill not found.")
            return
        patient = self._recursive_find(self._patients, bill.patient_id)
        pname   = patient.name if patient else "Unknown"
        print(bill.generate_receipt(pname))

    def generate_receipt(self):
        print("\n Generate Receipt")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print(" Patient not found.")
            return
        bills = [b for b in self._bills if b.patient_id == pid]
        if not bills:
            print("  No bills found for this patient.")
            return
        print(f"\n  Bills for {patient.name} ({len(bills)} total):")
        for i, b in enumerate(bills, 1):
            print(f"  {i}. {b}")
        try:
            sc = int(input("  Select bill #: ")) - 1
            if 0 <= sc < len(bills):
                print(bills[sc].generate_receipt(patient.name))
            else:
                print("  Invalid selection.")
        except ValueError:
            print(" Invalid input.")

    # GENERATOR: Hospital Summary Report
    
    def _report_generator(self):
        """
        Generator function: yields one section of the hospital report at a time.
        Demonstrates the use of Python generators.
        """
        yield f"\n{'='*60}"
        yield f"  SMART HOSPITAL MANAGEMENT SYSTEM — SUMMARY REPORT"
        yield f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        yield f"{'='*60}"
        yield f"\n  PATIENTS   : {len(self._patients)}"
        yield f"  DOCTORS    : {len(self._doctors)}"
        yield f"  NURSES     : {len(self._nurses)}"
        yield f"  APPOINTMENTS: {len(self._appointments)}"
        yield f"  MED RECORDS: {len(self._records)}"
        yield f"  LAB REPORTS: {len(self._lab_reports)}"
        yield f"  MEDICINES  : {len(self._medicines)}"
        yield f"  BILLS      : {len(self._bills)}"

        booked = [a for a in self._appointments if a.status == Appointment.STATUS_BOOKED]
        cancelled = [a for a in self._appointments if a.status == Appointment.STATUS_CANCELLED]
        yield f"\n  Booked Appointments  : {len(booked)}"
        yield f"  Cancelled Appointments: {len(cancelled)}"

        total_revenue = sum(b.calculate_total() for b in self._bills if b.is_paid)
        yield f"\n  Total Revenue (Paid Bills): ₹{total_revenue:.2f}"

        expired = [m for m in self._medicines if m.is_expired()]
        yield f"  Expired Medicines    : {len(expired)}"

        yield f"\n  TOP DOCTORS BY FEE:"
        # Lambda sort
        top_docs = sorted(self._doctors, key=lambda d: d.consultation_fee, reverse=True)[:5]
        for doc in top_docs:
            yield f"    Dr. {doc.name:<20} | ₹{doc.consultation_fee:.2f}"

        yield f"\n{'='*60}"

    def generate_report(self):
        """Use the generator to print the hospital report."""
        print("\n  Generating Hospital Report...")
        for line in self._report_generator():
            print(line)

    # SAVE & LOAD ALL DATA
    
    def save_all_data(self):
        print("\n  Saving All Data")
        save_data(PATIENTS_FILE,     [p.to_dict() for p in self._patients])
        save_data(DOCTORS_FILE,      [d.to_dict() for d in self._doctors])
        save_data(APPOINTMENTS_FILE, [a.to_dict() for a in self._appointments])
        save_data(MEDICINES_FILE,    [m.to_dict() for m in self._medicines])
        save_data(RECORDS_FILE,      [r.to_dict() for r in self._records])
        save_data(BILLS_FILE,        [b.to_dict() for b in self._bills])
        # Nurses are kept in doctors file group for simplicity; save separately
        save_data("nurses.json",     [n.to_dict() for n in self._nurses])
        save_data("lab_reports.json",[l.to_dict() for l in self._lab_reports])
        print("  ✔ All data saved.")

    def load_all_data(self):
        print("\n Loading All Data")
        self._patients.clear()
        self._patients.extend(Patient.from_dict(d) for d in load_data(PATIENTS_FILE))

        self._doctors.clear()
        self._doctors.extend(Doctor.from_dict(d) for d in load_data(DOCTORS_FILE))

        self._appointments.clear()
        self._appointments.extend(
            Appointment.from_dict(d) for d in load_data(APPOINTMENTS_FILE))

        self._medicines.clear()
        self._medicines.extend(Medicine.from_dict(d) for d in load_data(MEDICINES_FILE))

        self._records.clear()
        self._records.extend(
            MedicalRecord.from_dict(d) for d in load_data(RECORDS_FILE))

        self._bills.clear()
        self._bills.extend(Bill.from_dict(d) for d in load_data(BILLS_FILE))

        self._nurses.clear()
        self._nurses.extend(Nurse.from_dict(d) for d in load_data("nurses.json"))

        self._lab_reports.clear()
        self._lab_reports.extend(
            LabReport.from_dict(d) for d in load_data("lab_reports.json"))

        print(f" Loaded: {len(self._patients)} patients, {len(self._doctors)} doctors, "
              f"{len(self._nurses)} nurses, {len(self._appointments)} appointments.")

# MENU DRIVER

def display_main_menu():
    print("\n" + "=" * 55)
    print("       SMART HOSPITAL MANAGEMENT SYSTEM")
    print("=" * 55)
    print("  1.  Patient Management")
    print("  2.  Doctor Management")
    print("  3.  Nurse Management")
    print("  4.  Appointment Management")
    print("  5.  Medical Records")
    print("  6.  Laboratory Reports")
    print("  7.  Pharmacy Management")
    print("  8.  Billing Management")
    print("  9.  Generate Reports")
    print("  10. Save Data")
    print("  11. Load Data")
    print("  0.  Exit")
    print("=" * 55)

def patient_menu(hospital: Hospital):
    while True:
        print("\n Patient Management")
        print("  1. Register Patient")
        print("  2. Update Patient")
        print("  3. Search Patient")
        print("  4. View Patient History")
        print("  5. List All Patients")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.register_patient()
        elif ch == "2": hospital.update_patient()
        elif ch == "3": hospital.search_patient()
        elif ch == "4": hospital.view_patient_history()
        elif ch == "5": hospital.list_all_patients()
        elif ch == "0": break
        else: print("  Invalid choice.")


def doctor_menu(hospital: Hospital):
    while True:
        print("\nDoctor Management")
        print("  1. Add Doctor")
        print("  2. Update Doctor")
        print("  3. Manage Available Slots")
        print("  4. List All Doctors")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.add_doctor()
        elif ch == "2": hospital.update_doctor()
        elif ch == "3": hospital.manage_doctor_slots()
        elif ch == "4": hospital.list_all_doctors()
        elif ch == "0": break
        else: print("  ✘ Invalid choice.")

def nurse_menu(hospital: Hospital):
    while True:
        print("\n  ── Nurse Management ──")
        print("  1. Add Nurse")
        print("  2. Assign Department")
        print("  3. Manage Shift")
        print("  4. List All Nurses")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.add_nurse()
        elif ch == "2": hospital.assign_nurse_department()
        elif ch == "3": hospital.manage_nurse_shift()
        elif ch == "4": hospital.list_all_nurses()
        elif ch == "0": break
        else: print("  Invalid choice.")

def appointment_menu(hospital: Hospital):
    while True:
        print("\n Appointment Management")
        print("  1. Book Appointment")
        print("  2. Cancel Appointment")
        print("  3. Reschedule Appointment")
        print("  4. View Appointments")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.book_appointment()
        elif ch == "2": hospital.cancel_appointment()
        elif ch == "3": hospital.reschedule_appointment()
        elif ch == "4": hospital.view_appointments()
        elif ch == "0": break
        else: print(" Invalid choice.")

def medical_records_menu(hospital: Hospital):
    while True:
        print("\n Medical Records")
        print("  1. Add Diagnosis & Prescription")
        print("  2. View Records")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.add_medical_record()
        elif ch == "2": hospital.view_medical_records()
        elif ch == "0": break
        else: print(" Invalid choice.")

def lab_menu(hospital: Hospital):
    while True:
        print("\n  Laboratory Managemen")
        print("  1. Create Lab Report")
        print("  2. View Lab Reports")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.create_lab_report()
        elif ch == "2": hospital.view_lab_reports()
        elif ch == "0": break
        else: print("  Invalid choice.")

def pharmacy_menu(hospital: Hospital):
    while True:
        print("\nPharmacy Management")
        print("  1. Add Medicine")
        print("  2. Update Stock")
        print("  3. Check Availability")
        print("  4. Check Expiry Dates")
        print("  5. List All Medicines")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.add_medicine()
        elif ch == "2": hospital.update_medicine_stock()
        elif ch == "3": hospital.check_medicine_availability()
        elif ch == "4": hospital.check_expiry()
        elif ch == "5": hospital.list_all_medicines()
        elif ch == "0": break
        else: print("  Invalid choice.")

def billing_menu(hospital: Hospital):
    while True:
        print("\n Billing Management")
        print("  1. Create Bill")
        print("  2. View Bill by Bill ID")
        print("  3. Generate Receipt for Patient")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if   ch == "1": hospital.create_bill()
        elif ch == "2": hospital.view_bill()
        elif ch == "3": hospital.generate_receipt()
        elif ch == "0": break
        else: print(" Invalid choice.")

#ENTRY POINT

def main():
    hospital = Hospital("Smart City Hospital")
    print("\n  Welcome to SMART HOSPITAL MANAGEMENT SYSTEM")
    print(f"  Hospital: {hospital._name}")

    # Auto-load data if files exist
    hospital.load_all_data()

    while True:
        display_main_menu()
        choice = input("\n  Enter your choice: ").strip()
        try:
            if   choice == "1":  patient_menu(hospital)
            elif choice == "2":  doctor_menu(hospital)
            elif choice == "3":  nurse_menu(hospital)
            elif choice == "4":  appointment_menu(hospital)
            elif choice == "5":  medical_records_menu(hospital)
            elif choice == "6":  lab_menu(hospital)
            elif choice == "7":  pharmacy_menu(hospital)
            elif choice == "8":  billing_menu(hospital)
            elif choice == "9":  hospital.generate_report()
            elif choice == "10": hospital.save_all_data()
            elif choice == "11": hospital.load_all_data()
            elif choice == "0":
                save_choice = input("\n  Save data before exiting? (y/n): ").strip().lower()
                if save_choice == "y":
                    hospital.save_all_data()
                print("\n  Thank you for using Smart Hospital Management System!")
                print("  Goodbye!\n")
                break
            else:
                print(" Invalid choice. Please enter 0-11.")
        except KeyboardInterrupt:
            print("\n\n  Interrupted. Returning to main menu.")
        except Exception as e:
            print(f"\n  Unexpected error: {e}")


if __name__ == "__main__":
    main()