from pydantic import EmailStr, BaseModel


class UserSchema(BaseModel):
    name: str
    email: EmailStr
