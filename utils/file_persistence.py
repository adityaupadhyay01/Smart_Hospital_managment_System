import os
from datetime import datetime
from config import DATA_ROOT


def _ensure_dir(subfolder: str) -> str:
    """Create DATA_ROOT/<subfolder> if it does not exist. Returns the path."""
    path = os.path.join(DATA_ROOT, subfolder)
    os.makedirs(path, exist_ok=True)
    return path


def _write_file(filepath: str, content: str) -> None:
    """Write content to filepath, overwriting any previous version."""
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
    diag_txt  = "\n".join(f"    • {d}" for d in record.diagnoses) or "    None"
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
    folder    = _ensure_dir("bills")
    filepath  = os.path.join(folder, f"bill_{bill.id}.txt")
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
