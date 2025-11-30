from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
	"""註冊使用者時的輸入資料格式 (Request schema)。

	欄位: username, email(選填), password。
	"""
	username: str
	email: Optional[EmailStr] = None
	password: str


class UserOut(BaseModel):
	"""回傳給用戶端的使用者資料格式 (Response schema)。

	不包含 hashed_password，僅提供 id / username / email。
	"""
	id: int
	username: str
	email: Optional[EmailStr] = None

	class Config:
		orm_mode = True


class Token(BaseModel):
	"""JWT 存取權杖的回傳格式。

	access_token: 實際的 JWT 字串
	token_type: token 類型 (預設 bearer)
	"""
	access_token: str
	token_type: str = "bearer"


class TokenData(BaseModel):
	"""解析 token 後的資料結構 (內部使用) - 包含 username(sub)。"""
	username: Optional[str] = None

