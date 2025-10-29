from enum import Enum
from datetime import datetime
from typing import TypedDict


class Role(str, Enum):
    reader = "reader"
    writer = "writer"
    admin = "admin"


# Raw DB shapes (what we persist)
class OrganizationDoc(TypedDict):
    id: str
    name: str
    created_at: datetime


class UserDoc(TypedDict):
    id: str
    org_id: str
    email: str
    role: str
    created_at: datetime


class NoteDoc(TypedDict):
    id: str
    org_id: str
    title: str
    content: str
    author_id: str
    created_at: datetime
