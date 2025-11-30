from sqlalchemy.orm import Session
from app import models


def get_user_by_username(db: Session, username: str):
	"""查詢使用者（透過 username）。

	回傳 User 物件或 None。
	"""
	return db.query(models.user.User).filter(models.user.User.username == username).first()


def create_user(db: Session, username: str, email: str, hashed_password: str):
	"""新增使用者到資料庫並回傳建立好的 User 物件。"""
	user = models.user.User(username=username, email=email, hashed_password=hashed_password)
	db.add(user)
	db.commit()
	db.refresh(user)
	return user

