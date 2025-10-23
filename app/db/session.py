from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    import app.models.user  # import all models to register with Base
    from app.db.base import Base  # <-- use the shared Base
    Base.metadata.create_all(bind=engine)
