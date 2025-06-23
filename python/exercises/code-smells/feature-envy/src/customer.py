from dataclasses import dataclass


@dataclass
class Customer:
    id: str
    name: str
    email: str
    type: str
    loyalty_years: int
    address: str = ""
    phone_number: str = ""

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_email(self) -> str:
        return self.email

    def get_type(self) -> str:
        return self.type

    def get_loyalty_years(self) -> int:
        return self.loyalty_years

    def get_address(self) -> str:
        return self.address

    def get_phone_number(self) -> str:
        return self.phone_number
