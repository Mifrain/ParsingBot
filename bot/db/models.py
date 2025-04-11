from sqlalchemy import Column, Integer, String, Float

from bot.db.base import Base, engine


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)
    price = Column(Float, default=None, nullable=True)


Base.metadata.create_all(bind=engine)