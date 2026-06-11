import uuid
from datetime import datetime

class Appointment:
    BOOKED = "Booked"; CANCELLED = "Cancelled"; COMPLETED = "Completed"; RESCHEDULED = "Rescheduled"

    def __init__(self, patient_id, doctor_id, date_time, reason="General Checkup"):
        self._id         = str(uuid.uuid4())[:8].upper()
        self._patient_id = patient_id
        self._doctor_id  = doctor_id
        self._date_time  = date_time
        self._reason     = reason
        self._status     = Appointment.BOOKED
        self._created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def id(self):         return self._id
    @property
    def patient_id(self): return self._patient_id
    @property
    def doctor_id(self):  return self._doctor_id
    @property
    def date_time(self):  return self._date_time
    @property
    def status(self):     return self._status
    @property
    def reason(self):     return self._reason

    def cancel(self):
        if self._status == Appointment.BOOKED: self._status = Appointment.CANCELLED; print(f"  {self._id} cancelled.")
        else: print(f"  Cannot cancel. Status: {self._status}")
    def reschedule(self, dt):
        if self._status in (Appointment.BOOKED, Appointment.RESCHEDULED):
            self._date_time = dt; self._status = Appointment.RESCHEDULED; print(f"  Rescheduled → {dt}")
        else: print(f"  Cannot reschedule. Status: {self._status}")
    def complete(self): self._status = Appointment.COMPLETED

    def __str__(self):
        return f"Appt {self._id} | P:{self._patient_id} D:{self._doctor_id} | {self._date_time} | {self._status}"

    def to_dict(self):
        return dict(id=self._id, patient_id=self._patient_id, doctor_id=self._doctor_id,
                    date_time=self._date_time, reason=self._reason,
                    status=self._status, created_at=self._created_at)

    @staticmethod
    def from_dict(data):
        a = Appointment(data["patient_id"], data["doctor_id"], data["date_time"], data.get("reason","General Checkup"))
        a._id = data["id"]; a._status = data.get("status", Appointment.BOOKED)
        a._created_at = data.get("created_at",""); return a
