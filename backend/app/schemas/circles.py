from pydantic import BaseModel, EmailStr
from enum import Enum

class CircleStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"

class CircleInvite(BaseModel):
    guardian_email: EmailStr

class CircleMemberResponse(BaseModel):
    id: int
    user_id: int
    guardian_id: int
    status: str

    class Config:
        from_attributes = True