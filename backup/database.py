from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user_model import Base
from config import Config

SQLALCHEMY_DATABASE_URL = Config.SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def init_db():
    Base.metadata.create_all(bind=engine)