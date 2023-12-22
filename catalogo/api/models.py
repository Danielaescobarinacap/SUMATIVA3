from ninja import Schema
from typing import List


class MessageSchema(Schema):
    message: str

class ServiceInputSchema(Schema):
    name: str
    description: str
    provider: int
    valeu: int
    from_date: str
    thru_date: str

class ProviderOutputSchema(Schema):
    fantasy: str
    tax_name: str
    tax_id: str
    enable: bool

class AddressOutputSchema(Schema):
    provider: int
    type: str
    direction1: str
    direction2: str
    codepost: str
    city: str
    region: str
    country: str

class ContactOutputSchema(Schema):
    provider: int
    type: str
    first_name: str
    last_name: str
    email: str
    phone: str
    mobile: str

class ServiceOutputSchema(Schema):
    name: str
    description: str
    provider: ProviderOutputSchema
    valeu: int
    from_date: str
    thru_date: str
    contact: List[ContactOutputSchema]
    direction: AddressOutputSchema






