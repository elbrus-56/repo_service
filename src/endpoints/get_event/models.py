import datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class Order(BaseModel):
    order_id: UUID
    user_id: int
    order_date: datetime.datetime
    status: str
    product_code: str
    quantity: int
    amount: Decimal
    shipping_address_city: list[str] = Field(validation_alias="shipping_address.city")
    shipping_address_street: list[str] = Field(
        validation_alias="shipping_address.street"
    )
    shipping_address_postal_code: list[str] = Field(
        validation_alias="shipping_address.postal_code"
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime


class MongoOrder(Order):
    shipping_address_city: list[str]
    shipping_address_street: list[str]
    shipping_address_postal_code: list[str]
