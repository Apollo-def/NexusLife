from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

def get_database_url():
    from django.conf import settings
    db = settings.DATABASES['default']
    port = db.get('PORT') or '5432'
    return f"postgresql://{db['USER']}:{db['PASSWORD']}@{db['HOST']}:{port}/{db['NAME']}"

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()
