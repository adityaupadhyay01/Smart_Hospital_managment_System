from hospital.hospital import Hospital
from menus.menus import (display_main_menu, patient_menu, doctor_menu,
    nurse_menu, appointment_menu, medical_records_menu,
    lab_menu, pharmacy_menu, billing_menu)

def main():
    h = Hospital("Smart City Hospital")
    print(f"\n  Welcome — {h._name}")
    h.load_all_data()
    actions = {
        "1": patient_menu, "2": doctor_menu, "3": nurse_menu,
        "4": appointment_menu, "5": medical_records_menu, "6": lab_menu,
        "7": pharmacy_menu, "8": billing_menu,
        "9": lambda h: h.generate_report(),
        "10": lambda h: h.save_all_data(),
        "11": lambda h: h.load_all_data(),
    }
    while True:
        display_main_menu()
        ch = input("  Choice: ").strip()
        if ch == "0":
            if input("  Save before exit? y/n: ").strip().lower() == "y": h.save_all_data()
            print("  Goodbye!"); break
        try:
            if ch in actions: actions[ch](h)
            else: print("  ✘ Invalid choice.")
        except KeyboardInterrupt: print("\n  Back to menu.")
        except Exception as e: print(f"  ✘ Error: {e}")

if __name__ == "__main__":
    main()
