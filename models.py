from pydantic import BaseModel, Field, field_validator
from datetime import datetime
import re


class Status():
    created = 'размещен'
    unpaid = 'ожидает оплаты'
    paid = 'оплачен'
    delivering = 'доставляется'
    completed = 'выполнен'
    cancelled = 'отменен'

class UserIn(BaseModel):
    name: str = Field(..., max_length=32)
    surname: str = Field(..., max_length=32)
    email: str = Field(..., max_length=128)
    password: str = Field(..., min_length=6, max_length=64)

    @field_validator("email")
    def check_email(cls, value):
        # use a regex to check that the email has a valid format
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Invalid email address")
        return value
        
class User(UserIn):
    id: int = Field(default=0, ge=0)


class ProductIn(BaseModel):
    name: str = Field(..., max_length=48)
    description: str = Field(..., max_length=150)
    cost: float = Field(..., gt=0)

class Product(ProductIn):
    id: int = Field(default=0, ge=0)

class OrderIn(BaseModel):
    user_id: int = Field(..., ge=0)
    product_id: int = Field(..., ge=0)
    date: datetime = Field(default_factory=datetime.now)
    status: str = Field(default=Status.created, max_length=16)

class Order(OrderIn):
    id: int = Field(..., ge=0)


