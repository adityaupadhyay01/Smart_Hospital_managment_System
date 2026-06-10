# All menu functions for the Hospital Management System

from hospital.hospital import Hospital

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
        print("\n  ── Patient Management ──")
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
        else: print(" Invalid choice.")

def doctor_menu(hospital: Hospital):
    while True:
        print("\n Doctor Management")
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
        else: print("  Invalid choice.")

def nurse_menu(hospital: Hospital):
    while True:
        print("\n  Nurse Management")
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
        print("\n  Appointment Management")
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
        else: print("  Invalid choice.")

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
        else: print("  Invalid choice.")

def lab_menu(hospital: Hospital):
    while True:
        print("\n  Laboratory Management")
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
        print("\n Pharmacy Management")
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
        else: print("  Invalid choice.")