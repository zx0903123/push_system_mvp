from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
	"""使用者資料表 ORM 模型

	欄位：id, username, email, hashed_password。
	hashed_password 儲存已 hash 的密碼，不應直接暴露。
	"""

	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String(50), unique=True, index=True, nullable=False)
	email = Column(String(255), unique=False, index=True, nullable=True)
	hashed_password = Column(String(255), nullable=False)

