import json
import os
import uuid
import functools
from abc import ABC, abstractmethod
from datetime import datetime, date

# JSON file paths
PATIENTS_FILE     = "patients.json"
DOCTORS_FILE      = "doctors.json"
APPOINTMENTS_FILE = "appointments.json"
MEDICINES_FILE    = "medicines.json"
RECORDS_FILE      = "records.json"
BILLS_FILE        = "bills.json"
NURSES_FILE       = "nurses.json"
LAB_REPORTS_FILE  = "lab_reports.json"

# File system root for .txt record files 
DATA_ROOT = "hospital_data"