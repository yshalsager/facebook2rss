from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from facebook_rss.db.session import Base


class Feed(Base):
    __tablename__ = "feed"

    id = Column(Integer, primary_key=True, index=True)
    page = Column(String, unique=True, index=True, nullable=False)
    rss = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Feed(page={self.page}, timestamp={self.timestamp})>"
