from hospital.hospital import Hospital

def _menu(title, options, hospital):
    while True:
        print(f"\n {title}")
        for i, (label, _) in enumerate(options, 1): print(f"  {i}. {label}")
        print("  0. Back")
        ch = input("  Choice: ").strip()
        if ch == "0": break
        try:
            idx = int(ch) - 1
            if 0 <= idx < len(options): options[idx][1](hospital)
            else: print("  Invalid.")
        except ValueError: print("  Invalid.")

def display_main_menu():
    print("     SMART HOSPITAL MANAGEMENT SYSTEM")
    print("-" * 50)
    for i, label in enumerate(["Patient Management","Doctor Management",
        "Nurse Management","Appointment Management","Medical Records",
        "Laboratory Reports","Pharmacy Management","Billing Management",
        "Generate Reports","Save Data","Load Data"], 1):
        print(f"  {i:>2}. {label}")
    print("   0. Exit\n" + "-" * 50)

def patient_menu(h):
    _menu("Patient Management", [
        ("Register Patient",    lambda h: h.register_patient()),
        ("Update Patient",      lambda h: h.update_patient()),
        ("Search Patient",      lambda h: h.search_patient()),
        ("View Patient History",lambda h: h.view_patient_history()),
        ("List All Patients",   lambda h: h.list_all_patients()),
    ], h)

def doctor_menu(h):
    _menu("Doctor Management", [
        ("Add Doctor",           lambda h: h.add_doctor()),
        ("Update Doctor",        lambda h: h.update_doctor()),
        ("Manage Slots",         lambda h: h.manage_doctor_slots()),
        ("List All Doctors",     lambda h: h.list_all_doctors()),
    ], h)

def nurse_menu(h):
    _menu("Nurse Management", [
        ("Add Nurse",            lambda h: h.add_nurse()),
        ("Assign Department",    lambda h: h.assign_nurse_department()),
        ("Manage Shift",         lambda h: h.manage_nurse_shift()),
        ("List All Nurses",      lambda h: h.list_all_nurses()),
    ], h)

def appointment_menu(h):
    _menu("Appointment Management", [
        ("Book Appointment",     lambda h: h.book_appointment()),
        ("Cancel Appointment",   lambda h: h.cancel_appointment()),
        ("Reschedule",           lambda h: h.reschedule_appointment()),
        ("View Appointments",    lambda h: h.view_appointments()),
    ], h)

def medical_records_menu(h):
    _menu("Medical Records", [
        ("Add Record",           lambda h: h.add_medical_record()),
        ("View Records",         lambda h: h.view_medical_records()),
    ], h)

def lab_menu(h):
    _menu("Laboratory", [
        ("Create Lab Report",    lambda h: h.create_lab_report()),
        ("View Lab Reports",     lambda h: h.view_lab_reports()),
    ], h)

def pharmacy_menu(h):
    _menu("Pharmacy", [
        ("Add Medicine",         lambda h: h.add_medicine()),
        ("Update Stock",         lambda h: h.update_medicine_stock()),
        ("Check Availability",   lambda h: h.check_medicine_availability()),
        ("Check Expiry",         lambda h: h.check_expiry()),
        ("List All Medicines",   lambda h: h.list_all_medicines()),
    ], h)

def billing_menu(h):
    _menu("Billing", [
        ("Create Bill",          lambda h: h.create_bill()),
        ("View Bill",            lambda h: h.view_bill()),
        ("Generate Receipt",     lambda h: h.generate_receipt()),
    ], h)