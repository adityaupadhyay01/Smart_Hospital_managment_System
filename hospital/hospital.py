from datetime import datetime, date
from config import *
from models.patient        import Patient
from models.doctor         import Doctor
from models.nurse          import Nurse
from models.appointment    import Appointment
from models.medical_record import MedicalRecord
from models.medicine       import Medicine
from models.lab_report     import LabReport
from models.bill           import Bill
from utils.file_io         import save_data, load_data
from utils.decorators      import log_action
from utils.file_persistence import (save_patient_to_file, save_doctor_to_file,
    save_nurse_to_file, save_appointment_to_file, save_record_to_file,
    save_medicine_to_file, save_bill_to_file, save_lab_report_to_file)

def _inp(prompt): return input(f"  {prompt}").strip()

class Hospital:
    def __init__(self, name="Smart Hospital"):
        self._name = name
        self._patients, self._doctors, self._nurses = [], [], []
        self._appointments, self._records, self._lab_reports = [], [], []
        self._medicines, self._bills = [], []

    def _find(self, col, tid, i=0):
        if i >= len(col): return None
        return col[i] if col[i].id == tid else self._find(col, tid, i+1)

    # ── PATIENTS ─────────────────────────────────────────────────────────────
    @log_action
    def register_patient(self):
        try:
            p = Patient(_inp("Name      : "), int(_inp("Age       : ")),
                        _inp("Gender    : "), _inp("Phone     : "),
                        _inp("Address   : "), _inp("BloodGroup: "))
            self._patients.append(p); save_patient_to_file(p)
            print(f"  ✔ Patient registered. ID: {p.id}")
        except ValueError as e: print(f"  ✘ {e}")

    @log_action
    def update_patient(self):
        p = self._find(self._patients, _inp("Patient ID: ").upper())
        if not p: print("  ✘ Not found."); return
        try:
            n,a,ph,ad,bg = (_inp(f) or None for f in ["New Name: ","New Age : ","New Phone: ","New Addr : ","New BG   : "])
            p.update(n, int(a) if a else None, ph, ad, bg)
            save_patient_to_file(p); print("  ✔ Updated.")
        except ValueError as e: print(f"  ✘ {e}")

    def search_patient(self):
        ch = _inp("1=ID  2=Name: ")
        if ch == "1":
            p = self._find(self._patients, _inp("ID: ").upper())
            if p: print(f"  {p}\n  BG:{p.blood_group} Reg:{p.registration_date}")
            else: print("  ✘ Not found.")
        elif ch == "2":
            q = _inp("Name: ").lower()
            res = [p for p in self._patients if q in p.name.lower()]
            [print(f"  {p}") for p in res] if res else print("  ✘ None found.")

    def view_patient_history(self):
        pid = _inp("Patient ID: ").upper()
        p = self._find(self._patients, pid)
        if not p: print("  ✘ Not found."); return
        print(f"\n  {p} | BG:{p.blood_group}")
        recs = [r for r in self._records if r.patient_id == pid]
        print(f"  Records({len(recs)}):"); [print(f"    {r}") for r in recs]
        labs = [l for l in self._lab_reports if l.patient_id == pid]
        print(f"  Labs({len(labs)}):"); [print(f"    {l}") for l in labs]
        bills = [b for b in self._bills if b.patient_id == pid]
        print(f"  Bills({len(bills)}):"); [print(f"    {b}") for b in bills]

    def list_all_patients(self):
        if not self._patients: print("  No patients."); return
        [print(f"  {p}") for p in self._patients]

    # ── DOCTORS ───────────────────────────────────────────────────────────────
    @log_action
    def add_doctor(self):
        try:
            d = Doctor(_inp("Name : "), int(_inp("Age  : ")), _inp("Gender: "),
                       _inp("Phone: "), _inp("Addr : "), _inp("Spec : "),
                       float(_inp("Fee  : ₹")))
            self._doctors.append(d); save_doctor_to_file(d)
            print(f"  ✔ Doctor added. ID: {d.id}")
        except ValueError as e: print(f"  ✘ {e}")

    @log_action
    def update_doctor(self):
        d = self._find(self._doctors, _inp("Doctor ID: ").upper())
        if not d: print("  ✘ Not found."); return
        try:
            n,ph,ad,sp,fs = (_inp(f) or None for f in ["New Name: ","New Phone: ","New Addr: ","New Spec: ","New Fee : "])
            d.update(n, ph, ad, sp, float(fs) if fs else None)
            save_doctor_to_file(d); print("  ✔ Updated.")
        except ValueError as e: print(f"  ✘ {e}")

    def manage_doctor_slots(self):
        d = self._find(self._doctors, _inp("Doctor ID: ").upper())
        if not d: print("  ✘ Not found."); return
        ch = _inp("1=Add 2=Remove 3=View: ")
        if ch == "1": d.add_slot(_inp("Slot (YYYY-MM-DD HH:MM): "))
        elif ch == "2": d.remove_slot(_inp("Slot to remove: "))
        elif ch == "3": [print(f"  - {s}") for s in d.available_slots] or print("  None.")

    def list_all_doctors(self):
        if not self._doctors: print("  No doctors."); return
        [print(f"  {d} | ₹{d.consultation_fee:.2f}")
         for d in sorted(self._doctors, key=lambda d: d.consultation_fee)]

    # ── NURSES ────────────────────────────────────────────────────────────────
    @log_action
    def add_nurse(self):
        try:
            [print(f"  {i+1}. {s}") for i,s in enumerate(Nurse.SHIFTS)]
            sc = int(_inp("Shift (1-3): ")) - 1
            n = Nurse(_inp("Name : "), int(_inp("Age  : ")), _inp("Gender: "),
                      _inp("Phone: "), _inp("Addr : "), _inp("Dept : "),
                      Nurse.SHIFTS[sc] if 0 <= sc < 3 else Nurse.SHIFTS[0])
            self._nurses.append(n); save_nurse_to_file(n)
            print(f"  ✔ Nurse added. ID: {n.id}")
        except (ValueError, IndexError) as e: print(f"  ✘ {e}")

    def assign_nurse_department(self):
        n = self._find(self._nurses, _inp("Nurse ID: ").upper())
        if not n: print("  ✘ Not found."); return
        n.assign_department(_inp("Dept: ")); save_nurse_to_file(n)

    def manage_nurse_shift(self):
        n = self._find(self._nurses, _inp("Nurse ID: ").upper())
        if not n: print("  ✘ Not found."); return
        [print(f"  {i+1}. {s}") for i,s in enumerate(Nurse.SHIFTS)]
        try:
            sc = int(_inp("New shift (1-3): ")) - 1
            n.change_shift(Nurse.SHIFTS[sc]); save_nurse_to_file(n)
        except (ValueError, IndexError): print("  ✘ Invalid.")

    def list_all_nurses(self):
        if not self._nurses: print("  No nurses registered."); return
        [print(f"  {n} | {n.department} | {n.shift}") for n in self._nurses]

    # ── APPOINTMENTS ──────────────────────────────────────────────────────────
    @log_action
    def book_appointment(self):
        try:
            p = self._find(self._patients, _inp("Patient ID: ").upper())
            if not p: print("  ✘ Patient not found."); return
            d = self._find(self._doctors, _inp("Doctor ID : ").upper())
            if not d: print("  ✘ Doctor not found."); return
            if not d.available_slots: print("  No slots."); return
            [print(f"  {i+1}. {s}") for i,s in enumerate(d.available_slots)]
            sc = int(_inp("Slot #: ")) - 1
            if not (0 <= sc < len(d.available_slots)): print("  ✘ Invalid."); return
            slot = d.available_slots[sc]; d.remove_slot(slot)
            a = Appointment(p.id, d.id, slot, _inp("Reason: ") or "General Checkup")
            self._appointments.append(a); save_appointment_to_file(a)
            print(f"  ✔ Booked. ID: {a.id}")
        except (ValueError, IndexError) as e: print(f"  ✘ {e}")

    @log_action
    def cancel_appointment(self):
        a = self._find(self._appointments, _inp("Appt ID: ").upper())
        if not a: print("  ✘ Not found."); return
        a.cancel(); save_appointment_to_file(a)

    @log_action
    def reschedule_appointment(self):
        a = self._find(self._appointments, _inp("Appt ID: ").upper())
        if not a: print("  ✘ Not found."); return
        a.reschedule(_inp("New DateTime (YYYY-MM-DD HH:MM): "))
        save_appointment_to_file(a)

    def view_appointments(self):
        ch = _inp("1=All 2=ByPatient 3=ByDoctor 4=Booked: ")
        if   ch == "1": appts = self._appointments
        elif ch == "2": appts = [a for a in self._appointments if a.patient_id == _inp("Patient ID: ").upper()]
        elif ch == "3": appts = [a for a in self._appointments if a.doctor_id  == _inp("Doctor ID : ").upper()]
        elif ch == "4": appts = [a for a in self._appointments if a.status == Appointment.BOOKED]
        else: return
        [print(f"  {a}") for a in appts] if appts else print("  None found.")

    # ── MEDICAL RECORDS ───────────────────────────────────────────────────────
    @log_action
    def add_medical_record(self):
        p = self._find(self._patients, _inp("Patient ID: ").upper())
        if not p: print("  ✘ Not found."); return
        d = self._find(self._doctors, _inp("Doctor ID : ").upper())
        if not d: print("  ✘ Not found."); return
        mr = MedicalRecord(p.id, d.id)
        while (dx := _inp("Diagnosis (blank=stop): ")):
            mr.add_diagnosis(dx); p.add_history(dx)
        while (med := _inp("Medicine (blank=stop): ")):
            try: mr.add_prescription(med, _inp("Dosage: "), int(_inp("Days: ")))
            except ValueError: print("  ✘ Invalid days.")
        if n := _inp("Notes: "): mr.add_notes(n)
        self._records.append(mr); save_record_to_file(mr)
        print(f"  ✔ Record created. ID: {mr.id}")

    def view_medical_records(self):
        pid = _inp("Patient ID: ").upper()
        recs = [r for r in self._records if r.patient_id == pid]
        if not recs: print("  None found."); return
        for r in recs:
            print(f"  {r}")
            [print(f"    Dx: {d}") for d in r.diagnoses]
            [print(f"    Rx: {p['medicine']} {p['dosage']} {p['days']}d") for p in r.prescriptions]

    # ── LAB REPORTS ───────────────────────────────────────────────────────────
    @log_action
    def create_lab_report(self):
        p = self._find(self._patients, _inp("Patient ID: ").upper())
        if not p: print("  ✘ Not found."); return
        lr = LabReport(p.id, _inp("Test Name : "), _inp("Technician: ") or "Lab Tech")
        if _inp("Add result now? y/n: ").lower() == "y":
            try: lr.set_result(_inp("Result : "), _inp("Remarks: "), float(_inp("Cost ₹ : ")))
            except ValueError as e: print(f"  ✘ {e}")
        self._lab_reports.append(lr); save_lab_report_to_file(lr)
        print(f"  ✔ Lab report created. ID: {lr.id}")

    def view_lab_reports(self):
        pid = _inp("Patient ID: ").upper()
        reps = [r for r in self._lab_reports if r.patient_id == pid]
        [print(f"  {r}") for r in reps] if reps else print("  None found.")

    # ── PHARMACY ──────────────────────────────────────────────────────────────
    @log_action
    def add_medicine(self):
        try:
            m = Medicine(_inp("Name    : "), _inp("Category: "),
                         float(_inp("Price ₹ : ")), int(_inp("Stock   : ")),
                         _inp("Expiry (YYYY-MM-DD): "), _inp("Mfr     : ") or "Unknown")
            self._medicines.append(m); save_medicine_to_file(m)
            print(f"  ✔ Medicine added. ID: {m.id}")
        except ValueError as e: print(f"  ✘ {e}")

    def update_medicine_stock(self):
        m = self._find(self._medicines, _inp("Medicine ID: ").upper())
        if not m: print("  ✘ Not found."); return
        try: m.update_stock(int(_inp("Qty (+add/-remove): "))); save_medicine_to_file(m)
        except ValueError as e: print(f"  ✘ {e}")

    def check_medicine_availability(self):
        q = _inp("Name (partial): ").lower()
        res = [m for m in self._medicines if q in m.name.lower()]
        [print(f"  {m}") for m in res] if res else print("  None found.")

    def check_expiry(self):
        exp = [m for m in self._medicines if m.is_expired()]
        print(f"  Expired ({len(exp)}):"); [print(f"  ⚠ {m.name} | {m.expiry_date}") for m in exp]
        near = [(m,(datetime.strptime(m.expiry_date,"%Y-%m-%d").date()-date.today()).days)
                for m in self._medicines if not m.is_expired()
                and 0 <= (datetime.strptime(m.expiry_date,"%Y-%m-%d").date()-date.today()).days <= 30]
        if near: print(f"  Near-expiry:"); [print(f"  ⚠ {m.name} | {d}d left") for m,d in near]

    def list_all_medicines(self):
        if not self._medicines: print("  No medicines."); return
        [print(f"  {m}") for m in self._medicines]

    # ── BILLING ───────────────────────────────────────────────────────────────
    @log_action
    def create_bill(self):
        p = self._find(self._patients, _inp("Patient ID: ").upper())
        if not p: print("  ✘ Not found."); return
        bill = Bill(p.id)
        if _inp("Add consultation? y/n: ").lower() == "y":
            try:
                d = self._find(self._doctors, _inp("Doctor ID: ").upper())
                if d: bill.add_consultation(d.consultation_fee, d.name)
                else: bill.add_consultation(float(_inp("Manual amount ₹: ")))
            except ValueError as e: print(f"  ✘ {e}")
        while _inp("Add medicine charge? y/n: ").lower() == "y":
            try:
                m = self._find(self._medicines, _inp("Medicine ID: ").upper())
                if not m: print("  ✘ Not found."); break
                qty = int(_inp(f"Qty (stock={m.stock}): "))
                m.update_stock(-qty); bill.add_medicine_charge(m.price*qty, m.name)
            except ValueError as e: print(f"  ✘ {e}")
        while _inp("Add lab charge? y/n: ").lower() == "y":
            lr = self._find(self._lab_reports, _inp("Lab Report ID: ").upper())
            if lr: bill.add_lab_charge(lr.cost, lr.test_name)
            else: print("  ✘ Not found.")
        if _inp("Add other charge? y/n: ").lower() == "y":
            try: bill.add_other_charge(float(_inp("Amount ₹: ")), _inp("Desc: "))
            except ValueError as e: print(f"  ✘ {e}")
        try: bill.set_discount(float(_inp("Discount ₹ (0=none): ") or "0"))
        except ValueError: pass
        self._bills.append(bill); save_bill_to_file(bill, p.name)
        print(f"  ✔ Bill {bill.id} created. Total ₹{bill.calculate_total():.2f}")
        if _inp("Mark paid? y/n: ").lower() == "y":
            bill.mark_paid(); save_bill_to_file(bill, p.name)

    def view_bill(self):
        b = self._find(self._bills, _inp("Bill ID: ").upper())
        if not b: print("  ✘ Not found."); return
        pname = (self._find(self._patients, b.patient_id) or type("x", (), {"name":""})()).name
        print(b.generate_receipt(pname))

    def generate_receipt(self):
        p = self._find(self._patients, _inp("Patient ID: ").upper())
        if not p: print("  ✘ Not found."); return
        bills = [b for b in self._bills if b.patient_id == p.id]
        if not bills: print("  No bills."); return
        [print(f"  {i+1}. {b}") for i,b in enumerate(bills)]
        try:
            sc = int(_inp("Select #: ")) - 1
            if 0 <= sc < len(bills): print(bills[sc].generate_receipt(p.name))
        except ValueError: print("  ✘ Invalid.")

    # ── REPORTS ───────────────────────────────────────────────────────────────
    def _report_generator(self):
        yield f"\n{'='*55}\n  HOSPITAL SUMMARY — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*55}"
        yield (f"  Patients:{len(self._patients)} Doctors:{len(self._doctors)} "
               f"Nurses:{len(self._nurses)} Appts:{len(self._appointments)}")
        yield (f"  Records:{len(self._records)} Labs:{len(self._lab_reports)} "
               f"Meds:{len(self._medicines)} Bills:{len(self._bills)}")
        yield f"  Revenue (paid): ₹{sum(b.calculate_total() for b in self._bills if b.is_paid):.2f}"
        yield f"  Expired meds  : {sum(1 for m in self._medicines if m.is_expired())}"
        yield "  Top doctors by fee:"
        for d in sorted(self._doctors, key=lambda d: d.consultation_fee, reverse=True)[:5]:
            yield f"    Dr.{d.name} — ₹{d.consultation_fee:.2f}"
        yield "=" * 55

    def generate_report(self):
        for line in self._report_generator(): print(line)

    # ── SAVE / LOAD ───────────────────────────────────────────────────────────
    def save_all_data(self):
        save_data(PATIENTS_FILE,     [p.to_dict() for p in self._patients])
        save_data(DOCTORS_FILE,      [d.to_dict() for d in self._doctors])
        save_data(APPOINTMENTS_FILE, [a.to_dict() for a in self._appointments])
        save_data(MEDICINES_FILE,    [m.to_dict() for m in self._medicines])
        save_data(RECORDS_FILE,      [r.to_dict() for r in self._records])
        save_data(BILLS_FILE,        [b.to_dict() for b in self._bills])
        save_data(NURSES_FILE,       [n.to_dict() for n in self._nurses])
        save_data(LAB_REPORTS_FILE,  [l.to_dict() for l in self._lab_reports])
        print("  ✔ All data saved.")

    def load_all_data(self):
        def _load(col, cls, f): col.clear(); col.extend(cls.from_dict(d) for d in load_data(f))
        _load(self._patients,     Patient,       PATIENTS_FILE)
        _load(self._doctors,      Doctor,        DOCTORS_FILE)
        _load(self._appointments, Appointment,   APPOINTMENTS_FILE)
        _load(self._medicines,    Medicine,      MEDICINES_FILE)
        _load(self._records,      MedicalRecord, RECORDS_FILE)
        _load(self._bills,        Bill,          BILLS_FILE)
        _load(self._nurses,       Nurse,         NURSES_FILE)
        _load(self._lab_reports,  LabReport,     LAB_REPORTS_FILE)
        print(f"  ✔ Loaded: {len(self._patients)}P {len(self._doctors)}D "
              f"{len(self._nurses)}N {len(self._appointments)}A")
