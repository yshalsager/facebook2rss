from datetime import datetime

from sqlalchemy.orm import Session

from .models.models import Feed
from .session import SessionLocal


def get_feed(db: SessionLocal, page: str):
    return db.query(Feed).filter(Feed.page == page).first()


def add_feed(db: Session, page: str, rss: str) -> Feed:
    feed = Feed(
        page=page,
        rss=rss
    )
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed


def delete_user(db: Session, page: str):
    feed = get_feed(db, page)
    db.delete(feed)
    db.commit()
    return feed


def update_feed(db: Session, page: str, rss: str, timestamp=datetime.utcnow()) -> Feed:
    feed = get_feed(db, page)
    feed.rss = rss
    feed.timestamp = timestamp
    db.add(feed)
    db.commit()
    db.refresh(feed)
    return feed
