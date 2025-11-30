from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
	"""用於建立推播訊息的 request schema。"""
	title: str
	body: str


class MessageOut(BaseModel):
	"""回傳給 client 的訊息格式 (含時間、發送者)。"""
	id: int
	sender: str
	title: str
	body: str
	created_at: datetime

	class Config:
		orm_mode = True

