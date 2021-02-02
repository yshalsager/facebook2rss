import logging

from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from facebook_rss import config_path
from .models.tables import get_feed_table

logger = logging.getLogger(__name__)

engine = create_engine(f"sqlite:///{config_path}/feeds.db",
                       connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Create a MetaData instance
metadata: MetaData = MetaData()
# reflect db schema to MetaData
metadata.reflect(bind=engine)
# check if the table exists
ins = inspect(engine)
if 'feed' not in ins.get_table_names():
    logger.info("Feed table not found, creating one")
    get_feed_table(metadata)
    metadata.create_all(engine)


# Dependency
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
