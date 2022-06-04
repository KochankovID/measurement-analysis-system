from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DB_URL,
)

SessionBuilder = sessionmaker(autocommit=False, bind=engine, class_=AsyncSession)
