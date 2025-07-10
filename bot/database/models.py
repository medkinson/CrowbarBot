from sqlalchemy import Column, Integer, String, BigInteger
from database.base import Base

class CrowbarStats(Base):
    __tablename__ = "crowbarstats"

    telegram_id = Column(BigInteger, primary_key=True, unique=True)
    first_name = Column(String(64))
    last_name = Column(String(64))
    crowbars = Column(Integer, default=0)
    last_gift = Column(Integer, default=0)
    last_forging = Column(Integer, default=0)