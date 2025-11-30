from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.schemas.message import MessageCreate, MessageOut
from app.crud import message as message_crud
from app.api.auth import get_current_user, get_db
from app.services import push_service


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageOut)
def create_message(payload: MessageCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
	"""建立並儲存一則訊息，然後發佈至 Redis 以便即時轉發給線上用戶。"""
	m = message_crud.create_message(db, current_user.username, payload.title, payload.body)
	# publish to redis for realtime delivery (non-blocking)
	push_service.publish_message(dict(id=m.id, sender=m.sender, title=m.title, body=m.body))
	return m


@router.get("/", response_model=List[MessageOut])
def list_messages(db: Session = Depends(get_db)):
	"""列出資料庫中的歷史訊息（可分頁/篩選，再擴充）。"""
	return message_crud.list_messages(db)

