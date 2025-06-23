from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
from customer import Customer
from product import Product


@dataclass
class OrderItem:
    product: Product
    quantity: int


@dataclass
class Order:
    id: str
    customer: Customer
    items: List[OrderItem]
    shipping_address: str
    express: bool = False
    status: str = field(default='pending', init=False)
    order_date: str = field(default_factory=lambda: datetime.now().isoformat(), init=False)

    def get_id(self) -> str:
        return self.id

    def get_customer(self) -> Customer:
        return self.customer

    def get_items(self) -> List[OrderItem]:
        return self.items

    def get_status(self) -> str:
        return self.status

    def get_shipping_address(self) -> str:
        return self.shipping_address

    def get_order_date(self) -> str:
        return self.order_date

    def is_express(self) -> bool:
        return self.express

    def set_status(self, status: str) -> None:
        self.status = status

    def add_item(self, product: Product, quantity: int) -> None:
        self.items.append(OrderItem(product=product, quantity=quantity))