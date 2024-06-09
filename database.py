from datetime import datetime

from sqlalchemy import create_engine, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class SensorDataModel(Base):
    __tablename__ = "sensor_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String)
    dwell_time: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[datetime] = mapped_column(DateTime)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()