from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import settings


engine = create_engine(settings.DB_URL)

sync_session = sessionmaker(bind=engine)

Base = declarative_base()
