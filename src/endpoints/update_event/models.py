import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, Field


class Order(BaseModel):
    order_id: UUID
    user_id: int
    order_date: datetime.datetime = Field(exclude=True)
    status: str
    product_code: str
    quantity: int
    amount: int
    shipping_address_city: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.city",
            "shipping_address_city",
        ),
        serialization_alias="shipping_address.city",
        exclude=True,
    )
    shipping_address_street: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.street",
            "shipping_address_street",
        ),
        serialization_alias="shipping_address.street",
        exclude=True,
    )
    shipping_address_postal_code: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.postal_code",
            "shipping_address_postal_code",
        ),
        serialization_alias="shipping_address.postal_code",
        exclude=True,
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime
