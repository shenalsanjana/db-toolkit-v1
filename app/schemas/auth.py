from datetime import datetime
from typing import Optional
from ninja import Schema


class RegisterIn(Schema):
    name: str
    email: str
    password: str
    mobile_no: Optional[str] = None


class LoginIn(Schema):
    email: str
    password: str


class AuthOut(Schema):
    access_token: str
    token_type: str = "bearer"
    customer_id: int
    name: str
    email: str


class CustomerProfileOut(Schema):
    id: int
    name: str
    email: Optional[str] = None
    mobile_no: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
