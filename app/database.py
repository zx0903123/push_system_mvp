from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def init_db():
    """初始化資料庫結構

    目的：匯入資料模型以讓 SQLAlchemy 的 metadata 註冊，並建立遺失的資料表。
    在應用啟動時呼叫 (e.g. startup event) 以確保資料表存在。
    """
    # import all models so they are registered on the metadata
    from app.models import user, message  # noqa: F401

    Base.metadata.create_all(bind=engine)
