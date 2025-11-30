from typing import List
from app import models
from sqlalchemy.orm import Session


def create_message(db: Session, sender: str, title: str, body: str):
	"""建立一則推播訊息並存到資料庫，回傳 Message 物件。"""
	m = models.message.Message(sender=sender, title=title, body=body)
	db.add(m)
	db.commit()
	db.refresh(m)
	return m


def list_messages(db: Session):
	"""取出所有訊息（以 id 倒序），回傳 List[Message]。"""
	return db.query(models.message.Message).order_by(models.message.Message.id.desc()).all()

