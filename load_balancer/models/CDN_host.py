import datetime

from load_balancer.database.connection import Base

from sqlalchemy import (
    Column, String, Integer,
    DateTime, Boolean
)


class CDNHost(Base):
    __tablename__ = 'cdn_host'

    id = Column(Integer, autoincrement=True, primary_key=True)
    host = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    connected = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        """ Show user object info. """
        return f'<CDNHost: {self.id}>'
