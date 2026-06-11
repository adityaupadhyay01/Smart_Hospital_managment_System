import uuid
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name, age, gender, phone, address):
        self._id, self._name, self._age = str(uuid.uuid4())[:8].upper(), name, age
        self._gender, self._phone, self._address = gender, phone, address

    @property
    def id(self):      return self._id
    @property
    def name(self):    return self._name
    @property
    def age(self):     return self._age
    @property
    def gender(self):  return self._gender
    @property
    def phone(self):   return self._phone
    @property
    def address(self): return self._address

    @name.setter
    def name(self, v):
        if not v.strip(): raise ValueError("Name cannot be empty.")
        self._name = v
    @age.setter
    def age(self, v):
        if not (0 < v < 150): raise ValueError("Age must be 1-149.")
        self._age = v
    @phone.setter
    def phone(self, v):   self._phone = v
    @address.setter
    def address(self, v): self._address = v

    @abstractmethod
    def get_role(self): pass

    def __str__(self):
        return f"[{self.get_role()}] ID={self._id} | {self._name} | Age={self._age} | {self._gender} | {self._phone}"

    def to_dict(self):
        return dict(id=self._id, name=self._name, age=self._age,
                    gender=self._gender, phone=self._phone,
                    address=self._address, role=self.get_role())
