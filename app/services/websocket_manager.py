from typing import Dict, List
from fastapi import WebSocket
import asyncio
import json

from app.config import settings
import aioredis


class WebSocketManager:
	"""管理 WebSocket 連線並從 Redis 訂閱訊息的管理器。

	- active_connections: 儲存每個 username 對應的 WebSocket 列表
	- 監聽 Redis pub/sub channel 將收到的訊息轉送給對應連線
	"""

	def __init__(self):
		# 每個使用者可以有多個連線 (多裝置)
		self.active_connections: Dict[str, List[WebSocket]] = {}
		self._redis = None
		self._task = None

	async def connect(self, username: str, websocket: WebSocket):
		"""接受新的 WebSocket 連線並將它加入 active_connections。"""
		await websocket.accept()
		self.active_connections.setdefault(username, []).append(websocket)

	def disconnect(self, username: str, websocket: WebSocket):
		"""從 active_connections 移除該 websocket，若使用者無連線則清除 key。"""
		conns = self.active_connections.get(username) or []
		if websocket in conns:
			conns.remove(websocket)
		if not conns:
			self.active_connections.pop(username, None)

	async def send_personal(self, username: str, message: dict):
		"""把訊息發送給指定使用者（所有該使用者的連線）。"""
		conns = self.active_connections.get(username) or []
		for ws in list(conns):
			try:
				await ws.send_json(message)
			except Exception:
				# ignore and remove
				try:
					conns.remove(ws)
				except Exception:
					pass

	async def broadcast(self, message: dict):
		"""廣播訊息給所有已連線的 WebSocket clients。"""
		# send to all connected websockets
		for conns in list(self.active_connections.values()):
			for ws in list(conns):
				try:
					await ws.send_json(message)
				except Exception:
					pass

	async def _ensure_redis(self):
		if self._redis is None:
			self._redis = await aioredis.from_url(settings.REDIS_URL)

	async def _pubsub_listener(self):
		"""Redis pub/sub 的監聽迴圈：接收訊息後解析並 dispatch 給個別使用者或廣播。"""
		await self._ensure_redis()
		pubsub = self._redis.pubsub()
		await pubsub.subscribe("push_notifications")
		async for msg in pubsub.listen():
			if msg is None:
				continue
			if msg.get("type") != "message":
				continue
			try:
				payload = json.loads(msg.get("data"))
			except Exception:
				payload = {"text": str(msg)}

			# if contains target user -> send to that user, else broadcast
			target = payload.get("to")
			if target:
				await self.send_personal(target, payload)
			else:
				await self.broadcast(payload)

	async def start_listener(self):
		"""啟動 background task 去監聽 Redis channel（若尚未啟動）。"""
		if self._task is None:
			self._task = asyncio.create_task(self._pubsub_listener())

