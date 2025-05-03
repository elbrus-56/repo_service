import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import AliasChoices, BaseModel, Field


class Order(BaseModel):
    order_id: UUID
    user_id: int
    order_date: datetime.datetime
    status: str
    product_code: str
    quantity: int
    amount: Decimal
    shipping_address_city: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.city",
            "shipping_address_city",
        )
    )
    shipping_address_street: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.street",
            "shipping_address_street",
        )
    )
    shipping_address_postal_code: list[str] = Field(
        validation_alias=AliasChoices(
            "shipping_address.postal_code",
            "shipping_address_postal_code",
        )
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime
