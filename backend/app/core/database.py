from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

from app.core.config import settings

# 数据库URL配置
DATABASE_URL = settings.DATABASE_URL.replace("mysql+aiomysql://", "mysql://")
ASYNC_DATABASE_URL = settings.DATABASE_URL

# 异步数据库连接
database = Database(ASYNC_DATABASE_URL)

# SQLAlchemy配置
engine = create_engine(
    DATABASE_URL,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
    echo=settings.DEBUG,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基础模型类
Base = declarative_base()

# 元数据
metadata = MetaData()

# 数据库依赖
async def get_database():
    return database

def get_db():
    """同步数据库会话依赖"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 