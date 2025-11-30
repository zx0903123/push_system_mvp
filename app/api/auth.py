from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, Token
from app.database import SessionLocal, init_db
from app.crud import user as user_crud
from app.utils import security as security_utils

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
	db = SessionLocal()
	"""DB session 依賴注入（每個 request 提供獨立 Session）。"""
	try:
		yield db
	finally:
		db.close()


@router.on_event("startup")
def on_startup():
	"""應用啟動時建立/同步資料表結構（資料庫初始化）。"""
	init_db()


@router.post("/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
	"""註冊新使用者：驗證是否存在 -> 建立使用者 -> 回傳 access_token。"""

	existing = user_crud.get_user_by_username(db, payload.username)
	if existing:
		raise HTTPException(status_code=400, detail="user_already_exists")

	hashed = security_utils.get_password_hash(payload.password)
	user = user_crud.create_user(db, payload.username, payload.email, hashed)
	token = security_utils.create_access_token(user.username)
	return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	"""使用者登入：驗證帳號密碼，成功則回傳 JWT access_token。"""

	user = user_crud.get_user_by_username(db, form_data.username)
	if not user:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect_credentials")
	if not security_utils.verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect_credentials")

	token = security_utils.create_access_token(user.username)
	return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	"""依賴函式：從 Authorization token 取得當前使用者。

	常用於需要認證的 API endpoint，會在找不到或驗證失敗時拋出 HTTPException。
	"""
	try:
		payload = security_utils.decode_access_token(token)
	except Exception:
		raise HTTPException(status_code=401, detail="invalid_token")
	username = payload.get("sub")
	if not username:
		raise HTTPException(status_code=401, detail="invalid_token")
	user = user_crud.get_user_by_username(db, username)
	if not user:
		raise HTTPException(status_code=401, detail="user_not_found")
	return user

