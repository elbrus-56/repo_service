import datetime
import random
import uuid

from pydantic import BaseModel, Field


class Order(BaseModel):
    order_id: uuid.UUID | str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: int = Field(default_factory=lambda: random.randrange(1000, 10000000))
    order_date: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    status: str = Field(
        default_factory=lambda: random.choice(
            ["shipped", "processing", "completed", "pending"]
        )
    )
    product_code: str = Field(
        default_factory=lambda: f"PROD-{random.randrange(1000, 10000000)}"
    )
    quantity: int = Field(default_factory=lambda: random.randrange(0, 100))
    amount: float = Field(default_factory=lambda: random.randrange(0, 5000))
    shipping_address_city: list[str] = Field(
        default_factory=lambda: [f"City {random.randrange(1, 1000)}"],
        serialization_alias="shipping_address.city",
    )
    shipping_address_street: list[str] = Field(
        default_factory=lambda: [f"Street {random.randrange(1, 1000)}"],
        serialization_alias="shipping_address.street",
    )
    shipping_address_postal_code: list[str] = Field(
        default_factory=lambda: [f"ZIP{random.randrange(10000, 100000)}"],
        serialization_alias="shipping_address.postal_code",
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now()
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now() + datetime.timedelta(days=1)
    )
