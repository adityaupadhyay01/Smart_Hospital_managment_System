# =============================================================================
# hospital/hospital.py — Hospital class (Composition hub)
# Owns all entity lists and exposes every management operation.
# =============================================================================

from datetime import datetime, date

from config import (PATIENTS_FILE, DOCTORS_FILE, APPOINTMENTS_FILE,
                    MEDICINES_FILE, RECORDS_FILE, BILLS_FILE,
                    NURSES_FILE, LAB_REPORTS_FILE)

from models.patient       import Patient
from models.doctor        import Doctor
from models.nurse         import Nurse
from models.appointment   import Appointment
from models.medical_record import MedicalRecord
from models.medicine      import Medicine
from models.lab_report    import LabReport
from models.bill          import Bill

from utils.file_io          import save_data, load_data
from utils.decorators       import log_action
from utils.file_persistence import (
    save_patient_to_file, save_doctor_to_file, save_nurse_to_file,
    save_appointment_to_file, save_record_to_file, save_medicine_to_file,
    save_bill_to_file, save_lab_report_to_file,
)


class Hospital:
    """
    Central class for the Smart Hospital Management System.
    Uses Composition to manage all entity collections.
    """

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

    # -------------------------------------------------------------------------
    # HELPER: recursive search by id
    # -------------------------------------------------------------------------

    def _recursive_find(self, collection: list, target_id: str, index: int = 0):
        """
        Recursion: traverse a list to find an item by its .id attribute.
        Returns the item or None.
        """
        if index >= len(collection):
            return None
        if collection[index].id == target_id:
            return collection[index]
        return self._recursive_find(collection, target_id, index + 1)

    # =========================================================================
    # PATIENT MANAGEMENT
    # =========================================================================

    @log_action
    def register_patient(self):
        print("\n  ─── Register New Patient ───")
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
            print(f"\n  ✔ Patient registered successfully! ID: {p.id}")
            print(f"  {p}")
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    @log_action
    def update_patient(self):
        print("\n  ─── Update Patient ───")
        pid = input("  Enter Patient ID: ").strip().upper()
        p = self._recursive_find(self._patients, pid)
        if not p:
            print("  ✘ Patient not found.")
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
            save_patient_to_file(p)
            print("  ✔ Patient updated successfully.")
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    def search_patient(self):
        print("\n  ─── Search Patient ───")
        print("  1. Search by ID")
        print("  2. Search by Name")
        choice = input("  Choice: ").strip()
        if choice == "1":
            pid = input("  Patient ID: ").strip().upper()
            p = self._recursive_find(self._patients, pid)
            if p:
                print(f"\n  {p}")
                print(f"  Blood Group: {p.blood_group} | Registered: {p.registration_date}")
                history = ', '.join(p.medical_history) if p.medical_history else 'None'
                print(f"  Medical History: {history}")
            else:
                print("  ✘ Patient not found.")
        elif choice == "2":
            name = input("  Patient Name (partial): ").strip().lower()
            # List comprehension
            results = [p for p in self._patients if name in p.name.lower()]
            if results:
                for p in results:
                    print(f"  {p}")
            else:
                print("  ✘ No patients found with that name.")
        else:
            print("  ✘ Invalid choice.")

    def view_patient_history(self):
        print("\n  ─── Patient History ───")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  ✘ Patient not found.")
            return
        print(f"\n  Patient: {patient.name} | ID: {patient.id}")
        print(f"  Blood Group: {patient.blood_group}")

        records = [r for r in self._records if r.patient_id == pid]
        print(f"\n  Medical Records ({len(records)}):")
        for r in records:
            print(f"    {r}")
            for d in r.diagnoses:
                print(f"      Diagnosis: {d}")
            for pr in r.prescriptions:
                print(f"      Rx: {pr['medicine']} | Dosage: {pr['dosage']} | {pr['days']} days")

        labs = [l for l in self._lab_reports if l.patient_id == pid]
        print(f"\n  Lab Reports ({len(labs)}):")
        for l in labs:
            print(f"    {l}")

        bills = [b for b in self._bills if b.patient_id == pid]
        print(f"\n  Bills ({len(bills)}):")
        for b in bills:
            print(f"    {b}")

    def list_all_patients(self):
        if not self._patients:
            print("  No patients registered.")
            return
        print(f"\n  ─── All Patients ({len(self._patients)}) ───")
        for p in self._patients:
            print(f"  {p}")

    # =========================================================================
    # DOCTOR MANAGEMENT
    # =========================================================================

    @log_action
    def add_doctor(self):
        print("\n  ─── Add New Doctor ───")
        try:
            name    = input("  Full Name        : ").strip()
            age     = int(input("  Age              : "))
            gender  = input("  Gender (M/F/O)   : ").strip()
            phone   = input("  Phone            : ").strip()
            address = input("  Address          : ").strip()
            spec    = input("  Specialization   : ").strip()
            fee     = float(input("  Consultation Fee : ₹"))
            d = Doctor(name, age, gender, phone, address, spec, fee)
            self._doctors.append(d)
            save_doctor_to_file(d)
            print(f"\n  ✔ Doctor added! ID: {d.id}")
            print(f"  {d}")
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    @log_action
    def update_doctor(self):
        print("\n  ─── Update Doctor ───")
        did = input("  Doctor ID: ").strip().upper()
        d = self._recursive_find(self._doctors, did)
        if not d:
            print("  ✘ Doctor not found.")
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
            print("  ✔ Doctor updated.")
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    def manage_doctor_slots(self):
        print("\n  ─── Manage Doctor Slots ───")
        did = input("  Doctor ID: ").strip().upper()
        d = self._recursive_find(self._doctors, did)
        if not d:
            print("  ✘ Doctor not found.")
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
            print("  ✘ Invalid choice.")

    def list_all_doctors(self):
        if not self._doctors:
            print("  No doctors registered.")
            return
        # Lambda: sort by consultation fee
        sorted_docs = sorted(self._doctors, key=lambda d: d.consultation_fee)
        print(f"\n  ─── All Doctors (sorted by fee, {len(sorted_docs)}) ───")
        for d in sorted_docs:
            print(f"  {d} | Spec={d.specialization} | Fee=₹{d.consultation_fee:.2f}")

    # =========================================================================
    # NURSE MANAGEMENT
    # =========================================================================

    @log_action
    def add_nurse(self):
        print("\n  ─── Add New Nurse ───")
        try:
            name    = input("  Full Name   : ").strip()
            age     = int(input("  Age         : "))
            gender  = input("  Gender      : ").strip()
            phone   = input("  Phone       : ").strip()
            address = input("  Address     : ").strip()
            dept    = input("  Department  : ").strip()
            print("  Shifts:")
            for i, s in enumerate(Nurse.SHIFTS, 1):
                print(f"    {i}. {s}")
            sc    = int(input("  Choose Shift (1-3): ").strip()) - 1
            shift = Nurse.SHIFTS[sc] if 0 <= sc < len(Nurse.SHIFTS) else Nurse.SHIFTS[0]
            n = Nurse(name, age, gender, phone, address, dept, shift)
            self._nurses.append(n)
            save_nurse_to_file(n)
            print(f"\n  ✔ Nurse added! ID: {n.id}")
        except (ValueError, IndexError) as e:
            print(f"  ✘ Error: {e}")

    def assign_nurse_department(self):
        print("\n  ─── Assign Nurse Department ───")
        nid = input("  Nurse ID  : ").strip().upper()
        n = self._recursive_find(self._nurses, nid)
        if not n:
            print("  ✘ Nurse not found.")
            return
        dept = input("  Department: ").strip()
        n.assign_department(dept)
        save_nurse_to_file(n)

    def manage_nurse_shift(self):
        print("\n  ─── Manage Nurse Shift ───")
        nid = input("  Nurse ID: ").strip().upper()
        n = self._recursive_find(self._nurses, nid)
        if not n:
            print("  ✘ Nurse not found.")
            return
        print(f"  Current Shift: {n.shift}")
        for i, s in enumerate(Nurse.SHIFTS, 1):
            print(f"  {i}. {s}")
        try:
            sc = int(input("  New Shift (1-3): ").strip()) - 1
            n.change_shift(Nurse.SHIFTS[sc])
            save_nurse_to_file(n)
        except (ValueError, IndexError):
            print("  ✘ Invalid selection.")

    def list_all_nurses(self):
        if not self._nurses:
            print("  No nurses registered.")
            return
        print(f"\n  ─── All Nurses ({len(self._nurses)}) ───")
        for n in self._nurses:
            print(f"  {n} | Dept={n.department} | Shift={n.shift}")

    # =========================================================================
    # APPOINTMENT MANAGEMENT
    # =========================================================================

    @log_action
    def book_appointment(self):
        print("\n  ─── Book Appointment ───")
        try:
            pid = input("  Patient ID : ").strip().upper()
            patient = self._recursive_find(self._patients, pid)
            if not patient:
                print("  ✘ Patient not found.")
                return
            did = input("  Doctor ID  : ").strip().upper()
            doctor = self._recursive_find(self._doctors, did)
            if not doctor:
                print("  ✘ Doctor not found.")
                return
            print(f"  Available slots for Dr. {doctor.name}:")
            if not doctor.available_slots:
                print("  No slots available. Please add slots first.")
                return
            for i, s in enumerate(doctor.available_slots, 1):
                print(f"    {i}. {s}")
            sc = int(input("  Select Slot #: ").strip()) - 1
            if not (0 <= sc < len(doctor.available_slots)):
                print("  ✘ Invalid slot selection.")
                return
            slot   = doctor.available_slots[sc]
            reason = input("  Reason      : ").strip() or "General Checkup"
            appt   = Appointment(pid, did, slot, reason)
            doctor.remove_slot(slot)
            self._appointments.append(appt)
            save_appointment_to_file(appt)
            print(f"\n  ✔ Appointment booked! ID: {appt.id}")
            print(f"  {appt}")
        except (ValueError, IndexError) as e:
            print(f"  ✘ Error: {e}")

    @log_action
    def cancel_appointment(self):
        print("\n  ─── Cancel Appointment ───")
        aid = input("  Appointment ID: ").strip().upper()
        appt = self._recursive_find(self._appointments, aid)
        if not appt:
            print("  ✘ Appointment not found.")
            return
        appt.cancel()
        save_appointment_to_file(appt)

    @log_action
    def reschedule_appointment(self):
        print("\n  ─── Reschedule Appointment ───")
        aid = input("  Appointment ID        : ").strip().upper()
        appt = self._recursive_find(self._appointments, aid)
        if not appt:
            print("  ✘ Appointment not found.")
            return
        new_dt = input("  New DateTime (YYYY-MM-DD HH:MM): ").strip()
        appt.reschedule(new_dt)
        save_appointment_to_file(appt)

    def view_appointments(self):
        print("\n  ─── View Appointments ───")
        print("  1. All Appointments")
        print("  2. By Patient ID")
        print("  3. By Doctor ID")
        print("  4. Booked Only")
        ch = input("  Choice: ").strip()
        if ch == "1":
            appts = self._appointments
        elif ch == "2":
            pid   = input("  Patient ID: ").strip().upper()
            appts = [a for a in self._appointments if a.patient_id == pid]
        elif ch == "3":
            did   = input("  Doctor ID: ").strip().upper()
            appts = [a for a in self._appointments if a.doctor_id == did]
        elif ch == "4":
            appts = [a for a in self._appointments
                     if a.status == Appointment.STATUS_BOOKED]
        else:
            print("  ✘ Invalid choice.")
            return
        if not appts:
            print("  No appointments found.")
            return
        for a in appts:
            print(f"  {a}")

    # =========================================================================
    # MEDICAL RECORDS
    # =========================================================================

    @log_action
    def add_medical_record(self):
        print("\n  ─── Create Medical Record ───")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  ✘ Patient not found.")
            return
        did = input("  Doctor ID : ").strip().upper()
        doctor = self._recursive_find(self._doctors, did)
        if not doctor:
            print("  ✘ Doctor not found.")
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
        print(f"\n  ✔ Medical record created. ID: {mr.id}")

    def view_medical_records(self):
        print("\n  ─── View Medical Records ───")
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

    # =========================================================================
    # LABORATORY MANAGEMENT
    # =========================================================================

    @log_action
    def create_lab_report(self):
        print("\n  ─── Create Lab Report ───")
        pid = input("  Patient ID  : ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  ✘ Patient not found.")
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
                print(f"  ✘ Error: {e}")
        self._lab_reports.append(lr)
        save_lab_report_to_file(lr)
        print(f"\n  ✔ Lab report created. ID: {lr.id}")

    def view_lab_reports(self):
        print("\n  ─── View Lab Reports ───")
        pid = input("  Patient ID: ").strip().upper()
        reports = [r for r in self._lab_reports if r.patient_id == pid]
        if not reports:
            print("  No lab reports found.")
            return
        for r in reports:
            print(f"  {r}")

    # =========================================================================
    # PHARMACY MANAGEMENT
    # =========================================================================

    @log_action
    def add_medicine(self):
        print("\n  ─── Add Medicine ───")
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
            print(f"\n  ✔ Medicine added. ID: {m.id}")
            print(f"  {m}")
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    def update_medicine_stock(self):
        print("\n  ─── Update Medicine Stock ───")
        mid = input("  Medicine ID    : ").strip().upper()
        med = self._recursive_find(self._medicines, mid)
        if not med:
            print("  ✘ Medicine not found.")
            return
        print(f"  Current Stock: {med.stock}")
        try:
            qty = int(input("  Quantity to Add (+) or Remove (-): "))
            med.update_stock(qty)
            save_medicine_to_file(med)
        except ValueError as e:
            print(f"  ✘ Error: {e}")

    def check_medicine_availability(self):
        print("\n  ─── Check Medicine Availability ───")
        name    = input("  Medicine Name (partial): ").strip().lower()
        results = [m for m in self._medicines if name in m.name.lower()]
        if not results:
            print("  No medicines found.")
            return
        for m in results:
            status = "✔ Available" if m.is_available() else (
                "✘ Expired" if m.is_expired() else "✘ Out of Stock")
            print(f"  {m.name} | Stock={m.stock} | Price=₹{m.price:.2f} | {status}")

    def check_expiry(self):
        print("\n  ─── Medicines Expiry Check ───")
        # Lambda filter
        expired = list(filter(lambda m: m.is_expired(), self._medicines))
        if expired:
            print(f"  EXPIRED Medicines ({len(expired)}):")
            for m in expired:
                print(f"  ⚠  {m.name} | Expiry: {m.expiry_date}")
        else:
            print("  ✔ No expired medicines.")

        near = []
        for m in self._medicines:
            if not m.is_expired():
                try:
                    exp   = datetime.strptime(m.expiry_date, "%Y-%m-%d").date()
                    delta = (exp - date.today()).days
                    if 0 <= delta <= 30:
                        near.append((m, delta))
                except ValueError:
                    pass
        if near:
            print(f"\n  Near-Expiry (within 30 days) ({len(near)}):")
            for m, d in near:
                print(f"  ⚠  {m.name} | Expiry: {m.expiry_date} ({d} days left)")

    def list_all_medicines(self):
        if not self._medicines:
            print("  No medicines in pharmacy.")
            return
        print(f"\n  ─── All Medicines ({len(self._medicines)}) ───")
        for m in self._medicines:
            print(f"  {m}")

    # =========================================================================
    # BILLING MANAGEMENT
    # =========================================================================

    @log_action
    def create_bill(self):
        print("\n  ─── Create Bill ───")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  ✘ Patient not found.")
            return
        bill = Bill(pid)

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
                print(f"  ✘ Error: {e}")

        add_med = input("  Add medicine charges? (y/n): ").strip().lower()
        while add_med == "y":
            try:
                mid = input("  Medicine ID: ").strip().upper()
                med = self._recursive_find(self._medicines, mid)
                if not med:
                    print("  Medicine not found.")
                    break
                qty        = int(input(f"  Quantity (Stock={med.stock}): "))
                med.update_stock(-qty)
                total_cost = med.price * qty
                bill.add_medicine_charge(total_cost, med.name)
                print(f"  ₹{total_cost:.2f} added for {med.name} x{qty}.")
            except ValueError as e:
                print(f"  ✘ Error: {e}")
            add_med = input("  Add another medicine? (y/n): ").strip().lower()

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
                print(f"  ✘ Error: {e}")
            add_lab = input("  Add another lab charge? (y/n): ").strip().lower()

        add_other = input("  Add other charges? (y/n): ").strip().lower()
        if add_other == "y":
            try:
                desc = input("  Description: ").strip()
                amt  = float(input("  Amount (₹) : "))
                bill.add_other_charge(amt, desc)
            except ValueError as e:
                print(f"  ✘ Error: {e}")

        disc_s = input("  Discount (₹, 0 for none): ").strip()
        try:
            disc = float(disc_s) if disc_s else 0.0
            bill.set_discount(disc)
        except ValueError:
            disc = 0.0

        self._bills.append(bill)
        save_bill_to_file(bill, patient.name)
        print(f"\n  ✔ Bill created. ID: {bill.id}")
        print(f"  Total: ₹{bill.calculate_total():.2f}")

        pay_now = input("  Mark as paid now? (y/n): ").strip().lower()
        if pay_now == "y":
            bill.mark_paid()
            save_bill_to_file(bill, patient.name)

    def view_bill(self):
        print("\n  ─── View Bill ───")
        bid  = input("  Bill ID: ").strip().upper()
        bill = self._recursive_find(self._bills, bid)
        if not bill:
            print("  ✘ Bill not found.")
            return
        patient = self._recursive_find(self._patients, bill.patient_id)
        pname   = patient.name if patient else "Unknown"
        print(bill.generate_receipt(pname))

    def generate_receipt(self):
        print("\n  ─── Generate Receipt ───")
        pid = input("  Patient ID: ").strip().upper()
        patient = self._recursive_find(self._patients, pid)
        if not patient:
            print("  ✘ Patient not found.")
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
                print("  ✘ Invalid selection.")
        except ValueError:
            print("  ✘ Invalid input.")

    # =========================================================================
    # GENERATOR: Hospital Summary Report
    # =========================================================================

    def _report_generator(self):
        """
        Generator function: yields one section of the report at a time.
        """
        yield f"\n{'='*60}"
        yield  "  SMART HOSPITAL MANAGEMENT SYSTEM — SUMMARY REPORT"
        yield f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        yield f"{'='*60}"
        yield f"\n  PATIENTS    : {len(self._patients)}"
        yield f"  DOCTORS     : {len(self._doctors)}"
        yield f"  NURSES      : {len(self._nurses)}"
        yield f"  APPOINTMENTS: {len(self._appointments)}"
        yield f"  MED RECORDS : {len(self._records)}"
        yield f"  LAB REPORTS : {len(self._lab_reports)}"
        yield f"  MEDICINES   : {len(self._medicines)}"
        yield f"  BILLS       : {len(self._bills)}"

        booked    = [a for a in self._appointments if a.status == Appointment.STATUS_BOOKED]
        cancelled = [a for a in self._appointments if a.status == Appointment.STATUS_CANCELLED]
        yield f"\n  Booked Appointments   : {len(booked)}"
        yield f"  Cancelled Appointments: {len(cancelled)}"

        total_revenue = sum(b.calculate_total() for b in self._bills if b.is_paid)
        yield f"\n  Total Revenue (Paid)  : ₹{total_revenue:.2f}"

        expired = [m for m in self._medicines if m.is_expired()]
        yield f"  Expired Medicines     : {len(expired)}"

        yield "\n  TOP DOCTORS BY FEE:"
        top_docs = sorted(self._doctors, key=lambda d: d.consultation_fee, reverse=True)[:5]
        for doc in top_docs:
            yield f"    Dr. {doc.name:<20} | ₹{doc.consultation_fee:.2f}"

        yield f"\n{'='*60}"

    def generate_report(self):
        """Print the hospital summary report via generator."""
        print("\n  Generating Hospital Report...")
        for line in self._report_generator():
            print(line)

    # =========================================================================
    # SAVE & LOAD ALL DATA
    # =========================================================================

    def save_all_data(self):
        print("\n  ─── Saving All Data ───")
        save_data(PATIENTS_FILE,      [p.to_dict() for p in self._patients])
        save_data(DOCTORS_FILE,       [d.to_dict() for d in self._doctors])
        save_data(APPOINTMENTS_FILE,  [a.to_dict() for a in self._appointments])
        save_data(MEDICINES_FILE,     [m.to_dict() for m in self._medicines])
        save_data(RECORDS_FILE,       [r.to_dict() for r in self._records])
        save_data(BILLS_FILE,         [b.to_dict() for b in self._bills])
        save_data(NURSES_FILE,        [n.to_dict() for n in self._nurses])
        save_data(LAB_REPORTS_FILE,   [l.to_dict() for l in self._lab_reports])
        print("  ✔ All data saved.")

    def load_all_data(self):
        print("\n  ─── Loading All Data ───")
        # Use clear() + extend() to preserve list object identity (bug fix).
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
        self._nurses.extend(Nurse.from_dict(d) for d in load_data(NURSES_FILE))

        self._lab_reports.clear()
        self._lab_reports.extend(
            LabReport.from_dict(d) for d in load_data(LAB_REPORTS_FILE))

        print(f"  ✔ Loaded: {len(self._patients)} patients, "
              f"{len(self._doctors)} doctors, {len(self._nurses)} nurses, "
              f"{len(self._appointments)} appointments.")
