from .database import Base
from sqlalchemy import Column, Integer, String

class Post(Base):
    __tablename__ = "teleid"

    telegram_id = Column(Integer, primary_key=True, nullable=False)
    faceit_nickname = Column(String, nullable=False)
    search_count = Column(Integer, default='0', nullable=False)
   