import os
from datetime import datetime
from config import DATA_ROOT

def _dir(sub):
    p = os.path.join(DATA_ROOT, sub); os.makedirs(p, exist_ok=True); return p

def _write(path, text):
    try:
        open(path, "w", encoding="utf-8").write(text)
        print(f"  [FILE] → {path}")
    except IOError as e:
        print(f"  [FILE ✘] {path}: {e}")

S = "=" * 45
D = "-" * 45
TS = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_patient_to_file(p):
    hist = "\n".join(f"  • {h}" for h in p.medical_history) or "  None"
    _write(os.path.join(_dir("patients"), f"patient_{p.id}.txt"),
        f"{S}\n  PATIENT DETAILS\n{S}\n"
        f"  ID        : {p.id}\n  Name      : {p.name}\n  Age       : {p.age}\n"
        f"  Gender    : {p.gender}\n  Phone     : {p.phone}\n  Address   : {p.address}\n"
        f"  Blood Grp : {p.blood_group}\n  Registered: {p.registration_date}\n{D}\n"
        f"  History:\n{hist}\n{S}\n  Updated: {TS()}\n{S}\n")

def save_doctor_to_file(d):
    slots = "\n".join(f"  • {s}" for s in d.available_slots) or "  None"
    _write(os.path.join(_dir("doctors"), f"doctor_{d.id}.txt"),
        f"{S}\n  DOCTOR DETAILS\n{S}\n"
        f"  ID     : {d.id}\n  Name   : {d.name}\n  Age    : {d.age}\n"
        f"  Gender : {d.gender}\n  Phone  : {d.phone}\n  Spec   : {d.specialization}\n"
        f"  Dept   : {d.department}\n  Fee    : ₹{d.consultation_fee:.2f}\n{D}\n"
        f"  Slots:\n{slots}\n{S}\n  Updated: {TS()}\n{S}\n")

def save_nurse_to_file(n):
    _write(os.path.join(_dir("nurses"), f"nurse_{n.id}.txt"),
        f"{S}\n  NURSE DETAILS\n{S}\n"
        f"  ID   : {n.id}\n  Name : {n.name}\n  Age  : {n.age}\n"
        f"  Phone: {n.phone}\n  Dept : {n.department}\n  Shift: {n.shift}\n"
        f"{S}\n  Updated: {TS()}\n{S}\n")

def save_appointment_to_file(a):
    _write(os.path.join(_dir("appointments"), f"appointment_{a.id}.txt"),
        f"{S}\n  APPOINTMENT DETAILS\n{S}\n"
        f"  ID       : {a.id}\n  Patient  : {a.patient_id}\n  Doctor   : {a.doctor_id}\n"
        f"  DateTime : {a.date_time}\n  Reason   : {a.reason}\n  Status   : {a.status}\n"
        f"{S}\n  Updated: {TS()}\n{S}\n")

def save_record_to_file(r):
    diag  = "\n".join(f"  • {d}" for d in r.diagnoses) or "  None"
    presc = "\n".join(f"  • {p['medicine']} {p['dosage']} {p['days']}d" for p in r.prescriptions) or "  None"
    _write(os.path.join(_dir("records"), f"record_{r.id}.txt"),
        f"{S}\n  MEDICAL RECORD\n{S}\n"
        f"  ID      : {r.id}\n  Patient : {r.patient_id}\n  Doctor  : {r.doctor_id}\n  Date: {r.date}\n{D}\n"
        f"  Diagnoses:\n{diag}\n{D}\n  Prescriptions:\n{presc}\n{D}\n"
        f"  Notes: {r._notes or 'None'}\n{S}\n  Updated: {TS()}\n{S}\n")

def save_medicine_to_file(m):
    status = "EXPIRED" if m.is_expired() else ("Available" if m.stock > 0 else "Out of Stock")
    _write(os.path.join(_dir("medicines"), f"medicine_{m.id}.txt"),
        f"{S}\n  MEDICINE DETAILS\n{S}\n"
        f"  ID     : {m.id}\n  Name   : {m.name}\n  Cat    : {m.category}\n"
        f"  Price  : ₹{m.price:.2f}\n  Stock  : {m.stock}\n  Expiry : {m.expiry_date}\n"
        f"  Status : {status}\n{S}\n  Updated: {TS()}\n{S}\n")

def save_bill_to_file(bill, pname=""):
    items = "\n".join(f"  {i['description']:<30} ₹{i['amount']:>8.2f}" for i in bill._items) or "  (none)"
    gross = bill._consultation_charges + bill._medicine_charges + bill._lab_charges + bill._other_charges
    _write(os.path.join(_dir("bills"), f"bill_{bill.id}.txt"),
        f"{S}\n  BILL / RECEIPT\n{S}\n"
        f"  ID      : {bill.id}\n  Patient : {bill.patient_id} ({pname})\n  Date: {bill._date}\n{D}\n"
        f"{items}\n{D}\n"
        f"  Subtotal: ₹{gross:.2f}\n  Discount: ₹{bill._discount:.2f}\n"
        f"  TOTAL   : ₹{bill.calculate_total():.2f}\n"
        f"  Status  : {'✔ PAID' if bill.is_paid else '✘ UNPAID'}\n{S}\n  Updated: {TS()}\n{S}\n")

def save_lab_report_to_file(lr):
    _write(os.path.join(_dir("lab_reports"), f"labreport_{lr.id}.txt"),
        f"{S}\n  LAB REPORT\n{S}\n"
        f"  ID    : {lr.id}\n  Patient: {lr.patient_id}\n  Test  : {lr.test_name}\n"
        f"  Tech  : {lr._technician}\n  Date  : {lr.date}\n{D}\n"
        f"  Result : {lr.result}\n  Remarks: {lr._remarks or 'None'}\n"
        f"  Cost   : ₹{lr.cost:.2f}\n  Status : {lr.status}\n{S}\n  Updated: {TS()}\n{S}\n")
