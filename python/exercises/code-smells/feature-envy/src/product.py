from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    price: float
    category: str
    weight: float
    fragile: bool = False
    manufacturer: str = ""

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_category(self) -> str:
        return self.category

    def get_weight(self) -> float:
        return self.weight

    def is_fragile(self) -> bool:
        return self.fragile

    def get_manufacturer(self) -> str:
        return self.manufacturer
