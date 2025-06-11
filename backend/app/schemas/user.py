from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

# 用户基础模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

# 用户创建模型
class UserCreate(UserBase):
    password: str

# 用户更新模型
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    password: Optional[str] = None

# 用户响应模型
class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# 登录请求模型
class UserLogin(BaseModel):
    username: str
    password: str

# Token模型
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

# 登录响应模型
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User 