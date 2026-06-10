# =============================================================================
# models/medicine.py — Medicine class
# =============================================================================

import uuid
from datetime import datetime, date


class Medicine:
    """Represents a medicine in the hospital pharmacy."""

    def __init__(self, name: str, category: str, price: float,
                 stock: int, expiry_date: str, manufacturer: str = "Unknown"):
        self._id           = str(uuid.uuid4())[:8].upper()
        self._name         = name
        self._category     = category
        self._price        = float(price)
        self._stock        = int(stock)
        self._expiry_date  = expiry_date    # "YYYY-MM-DD"
        self._manufacturer = manufacturer

    @property
    def id(self):            return self._id
    @property
    def name(self):          return self._name
    @property
    def category(self):      return self._category
    @property
    def price(self):         return self._price
    @property
    def stock(self):         return self._stock
    @property
    def expiry_date(self):   return self._expiry_date
    @property
    def manufacturer(self):  return self._manufacturer

    def update_stock(self, quantity: int):
        """Add or subtract stock. Pass a negative value to reduce."""
        if self._stock + quantity < 0:
            raise ValueError(f"Insufficient stock. Available: {self._stock}")
        self._stock += quantity
        print(f"  Stock for '{self._name}' updated to {self._stock}.")

    def is_expired(self) -> bool:
        try:
            exp = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
            return exp < date.today()
        except ValueError:
            return False

    def is_available(self) -> bool:
        return self._stock > 0 and not self.is_expired()

    def __str__(self):
        status = ("EXPIRED" if self.is_expired()
                  else ("Available" if self._stock > 0 else "Out of Stock"))
        return (f"Medicine ID={self._id} | Name={self._name} | "
                f"Category={self._category} | Price=₹{self._price:.2f} | "
                f"Stock={self._stock} | Expiry={self._expiry_date} | Status={status}")

    def to_dict(self) -> dict:
        return {
            "id":           self._id,
            "name":         self._name,
            "category":     self._category,
            "price":        self._price,
            "stock":        self._stock,
            "expiry_date":  self._expiry_date,
            "manufacturer": self._manufacturer,
        }

    @staticmethod
    def from_dict(data: dict) -> "Medicine":
        m = Medicine(data["name"], data["category"], data["price"],
                     data["stock"], data["expiry_date"],
                     data.get("manufacturer", "Unknown"))
        m._id = data["id"]
        return m
