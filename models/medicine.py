import uuid
from datetime import datetime, date

class Medicine:
    def __init__(self, name, category, price, stock, expiry_date, manufacturer="Unknown"):
        self._id           = str(uuid.uuid4())[:8].upper()
        self._name         = name
        self._category     = category
        self._price        = float(price)
        self._stock        = int(stock)
        self._expiry_date  = expiry_date
        self._manufacturer = manufacturer

    @property
    def id(self):           return self._id
    @property
    def name(self):         return self._name
    @property
    def category(self):     return self._category
    @property
    def price(self):        return self._price
    @property
    def stock(self):        return self._stock
    @property
    def expiry_date(self):  return self._expiry_date
    @property
    def manufacturer(self): return self._manufacturer

    def update_stock(self, qty):
        if self._stock + qty < 0: raise ValueError(f"Insufficient stock ({self._stock}).")
        self._stock += qty; print(f"  Stock → {self._stock}")

    def is_expired(self):
        try: return datetime.strptime(self._expiry_date, "%Y-%m-%d").date() < date.today()
        except ValueError: return False

    def is_available(self): return self._stock > 0 and not self.is_expired()

    def __str__(self):
        s = "EXPIRED" if self.is_expired() else ("Available" if self._stock > 0 else "Out of Stock")
        return f"Med {self._id} | {self._name} | ₹{self._price:.2f} | Stock:{self._stock} | {self._expiry_date} | {s}"

    def to_dict(self):
        return dict(id=self._id, name=self._name, category=self._category,
                    price=self._price, stock=self._stock,
                    expiry_date=self._expiry_date, manufacturer=self._manufacturer)

    @staticmethod
    def from_dict(data):
        m = Medicine(data["name"], data["category"], data["price"], data["stock"],
                     data["expiry_date"], data.get("manufacturer","Unknown"))
        m._id = data["id"]; return m
