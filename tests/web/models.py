from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    name: str
    email: str
    firstname: Optional[str] = None
    secondname: Optional[str] = None
    address: Optional[dict] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[dict] = None


class GetUser(CreateUser):
    id: int
