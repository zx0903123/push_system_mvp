from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth as auth_api, message as message_api
from app.services import push_service
from app.database import init_db
from app.utils import security


app = FastAPI(title="push_system_mvp")


app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


app.include_router(auth_api.router)
app.include_router(message_api.router)


manager = push_service.manager


@app.on_event("startup")
async def startup_event():
	"""啟動事件：初始化資料庫並啟動 Redis pub/sub 監聽器。

	這樣能確保應用啟動時資料表存在，並使 WebSocketManager 可以接收跨實例的推播。
	"""
	# create tables and start background listeners
	init_db()
	try:
		await manager.start_listener()
	except Exception:
		# Redis might not be available during development — continue gracefully
		pass


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
	"""WebSocket 連線端點。

	需在 query string 中提供 token，後端會驗證後將 websocket 註冊到 WebSocketManager。
	接著持續保持連線，直到 client 主動斷開或網路中斷。
	"""
	try:
		payload = security.decode_access_token(token)
		username = payload.get("sub")
	except Exception:
		await websocket.close(code=1008)
		return

	try:
		await manager.connect(username, websocket)
		# Keep connection alive
		while True:
			await websocket.receive_text()
	except WebSocketDisconnect:
		manager.disconnect(username, websocket)

