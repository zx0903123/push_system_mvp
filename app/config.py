from pydantic import BaseSettings


class Settings(BaseSettings):
	"""全域設定（可由 .env 覆寫）

	說明: 包含應用名稱、DB/Redis 連線字串、JWT 設定等。
	在開發環境可以直接修改這邊或建立 .env 檔案。
	"""

	APP_NAME: str = "push_system_mvp"
	DEBUG: bool = True

	# Database - change to postgres/mysql in production
	DATABASE_URL: str = "sqlite:///./push_system.db"

	# Redis for caching and pub/sub
	REDIS_URL: str = "redis://localhost:6379/0"

	SECRET_KEY: str = "CHANGEME_CHANGE_IN_PROD"
	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

	class Config:
		# 指定讀取環境變數檔案 .env
		env_file = ".env"


settings = Settings()

