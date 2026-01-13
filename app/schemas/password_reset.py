from pydantic import BaseModel, EmailStr, Field

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    token: str
    new_password: str = Field(min_length=8)

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=8)
    new_password: str = Field(min_length=8)
    confirm_new_password: str = Field(min_length=8)
