# =============================================================================
# models/person.py — Abstract base class: Person
# =============================================================================

import uuid
from abc import ABC, abstractmethod


class Person(ABC):
    """
    Abstract base class representing a generic person.
    Enforces implementation of get_role() in all derived classes.
    Demonstrates: Abstraction, Encapsulation, Magic Methods.
    """

    def __init__(self, name: str, age: int, gender: str, phone: str, address: str):
        # Encapsulation: private attributes with underscore convention
        self._id      = str(uuid.uuid4())[:8].upper()
        self._name    = name
        self._age     = age
        self._gender  = gender
        self._phone   = phone
        self._address = address

    # --- Getters ---
    @property
    def id(self):       return self._id
    @property
    def name(self):     return self._name
    @property
    def age(self):      return self._age
    @property
    def gender(self):   return self._gender
    @property
    def phone(self):    return self._phone
    @property
    def address(self):  return self._address

    # --- Setters ---
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @age.setter
    def age(self, value):
        if not (0 < value < 150):
            raise ValueError("Age must be between 1 and 149.")
        self._age = value

    @phone.setter
    def phone(self, value):
        self._phone = value

    @address.setter
    def address(self, value):
        self._address = value

    # --- Abstract Method (Abstraction) ---
    @abstractmethod
    def get_role(self) -> str:
        """Every person must declare their role."""

    # --- Magic Method ---
    def __str__(self):
        return (f"[{self.get_role()}] ID={self._id} | Name={self._name} | "
                f"Age={self._age} | Gender={self._gender} | Phone={self._phone}")

    def to_dict(self) -> dict:
        """Serialize common person fields to a dictionary."""
        return {
            "id":      self._id,
            "name":    self._name,
            "age":     self._age,
            "gender":  self._gender,
            "phone":   self._phone,
            "address": self._address,
            "role":    self.get_role(),
        }

    @classmethod
    def from_dict_base(cls, data: dict):
        """Restore base fields from dictionary (used by subclasses)."""
        return data  # subclasses handle full restoration
