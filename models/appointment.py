# models/appointment.py — Appointment class
import uuid
from datetime import datetime


class Appointment:
    """Represents a scheduled appointment between a patient and a doctor."""

    STATUS_BOOKED      = "Booked"
    STATUS_CANCELLED   = "Cancelled"
    STATUS_COMPLETED   = "Completed"
    STATUS_RESCHEDULED = "Rescheduled"

    def __init__(self, patient_id: str, doctor_id: str,
                 date_time: str, reason: str = "General Checkup"):
        self._id         = str(uuid.uuid4())[:8].upper()
        self._patient_id = patient_id
        self._doctor_id  = doctor_id
        self._date_time  = date_time      # "YYYY-MM-DD HH:MM"
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