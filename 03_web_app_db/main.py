from datetime import datetime, timezone

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker

DATABASE_URL = "postgresql+psycopg://user:password@db:5432/app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Request(Base):
    __tablename__ = "request"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_root(db: Session = Depends(get_db)):
    db.add(Request())
    db.commit()
    count = db.scalar(func.count(Request.id))
    return {"request_count": count}
