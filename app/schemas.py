from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Literal
from app.models import Role


# --- Organizations
class OrgCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)


class OrgOut(BaseModel):
    id: str
    name: str
    created_at: datetime


# --- Users
class UserCreate(BaseModel):
    email: EmailStr
    role: Literal["reader", "writer", "admin"]


class UserOut(BaseModel):
    id: str
    org_id: str
    email: EmailStr
    role: Role
    created_at: datetime


# --- Notes
class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10_000)


class NoteOut(BaseModel):
    id: str
    org_id: str
    title: str
    content: str
    author_id: str
    created_at: datetime
