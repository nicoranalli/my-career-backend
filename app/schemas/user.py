from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    
class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserOut(UserBase):
    id: int
    roles: List[str] = Field(default_factory=lambda: ["user"])

    class Config:
        from_attributes = True

