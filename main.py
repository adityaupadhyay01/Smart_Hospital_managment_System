from hospital.hospital import Hospital
from menus.menus import (
    display_main_menu,
    patient_menu, doctor_menu, nurse_menu,
    appointment_menu, medical_records_menu,
    lab_menu, pharmacy_menu, billing_menu,
)

def main():
    hospital = Hospital("Smart City Hospital")
    print("\n  Welcome to SMART HOSPITAL MANAGEMENT SYSTEM")
    print(f"  Hospital: {hospital._name}")

    # Auto-load persisted data on startup
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
                print("  Invalid choice. Please enter 0-11.")
        except KeyboardInterrupt:
            print("\n\n  Interrupted. Returning to main menu.")
        except Exception as e:
            print(f"\n  Unexpected error: {e}")


if __name__ == "__main__":
    main()