from sqlalchemy import Table, Column, INT, VARCHAR, TEXT, TIMESTAMP


def get_feed_table(metadata):
    return Table('feed', metadata,
                 Column('id', INT(), primary_key=True, autoincrement=True, nullable=False, index=True),
                 Column('page', VARCHAR(50), nullable=False),
                 Column('rss', TEXT(), nullable=False),
                 Column('timestamp', TIMESTAMP(), nullable=False)
                 )
