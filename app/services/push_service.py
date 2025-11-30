import asyncio
import json
from app.config import settings
from app.services.websocket_manager import WebSocketManager
import aioredis


"""Push service: 負責把要推播的內容發佈到 redis，使得各實例能透過 pub/sub 轉發即時通知。

這裡同時暴露 manager 實例，可在 web 應用中使用該 manager 來直接送達連線內的 clients。
"""

manager = WebSocketManager()


def publish_message(payload: dict):
	"""把訊息 publish 到 Redis 的 pub/sub channel，跨實例廣播用。

	如果 Redis 無法連線，會在開發/測試階段靜默失敗以避免阻塞主流程。
	"""
	async def _publish():
		try:
			redis = await aioredis.from_url(settings.REDIS_URL)
			await redis.publish("push_notifications", json.dumps(payload))
		except Exception:
			# swallow publish errors during development / tests
			return

	try:
		asyncio.create_task(_publish())
	except RuntimeError:
		import asyncio as _asyncio
		_asyncio.run(_publish())

