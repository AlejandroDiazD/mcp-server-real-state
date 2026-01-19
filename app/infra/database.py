# infra/database.py
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.models import Base
from core.config import settings


engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Creates all database tables defined in the models.
    """
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db_session():
    """
    Context manager that handles the complete session liecycle:
    - Create session
    - Commits if successfull
    - Rolls back on error
    - Always closes session
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
