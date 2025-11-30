from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base


class Message(Base):
	"""推播訊息的 ORM 模型

	欄位：id, sender, title, body, created_at。
	用於存放已發布的推播訊息歷史紀錄。
	"""

	__tablename__ = "messages"

	id = Column(Integer, primary_key=True, index=True)
	sender = Column(String(50), nullable=False)
	title = Column(String(255), nullable=False)
	body = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
