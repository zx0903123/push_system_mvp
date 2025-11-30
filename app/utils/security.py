from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
	"""比對輸入密碼與資料庫中的 hashed_password 是否相符。"""
	return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
	"""將明碼密碼使用 bcrypt hash 後回傳，供儲存使用。"""
	return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
	"""生成 JWT 存取權杖 (access token)。

	subject: 通常放使用者識別（sub），expires_delta: 可指定到期時間。
	回傳已簽署的 JWT 字串。
	"""
	to_encode = {"sub": subject}
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
	"""解碼並驗證 JWT，失敗時會拋出 JWTError。

	回傳解碼後的 payload（例如包含 sub 與 exp）。
	"""
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		return payload
	except JWTError:
		# 呼叫端會處理例外，這裡直接往上拋
		raise

