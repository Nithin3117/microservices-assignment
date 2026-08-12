from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal, get_db
from models import Notification
from schemas import NotificationResponse
from nats_client import start_nats


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Notification Service: lifespan started")

    Base.metadata.create_all(bind=engine)

    app.state.db_session = SessionLocal

    print("Notification Service: starting NATS")

    await start_nats(app)

    print("Notification Service: NATS started")

    yield

    if hasattr(app.state, "nats"):
        await app.state.nats.close()

    print("Notification Service: shutdown complete")


app = FastAPI(
    title="Notification Service",
    lifespan=lifespan
)


@app.get("/")
def health_check():
    return {
        "service": "Notification Service",
        "status": "running"
    }


@app.get(
    "/notifications",
    response_model=list[NotificationResponse]
)
def get_notifications(
    db: Session = Depends(get_db)
):
    return db.query(Notification).all()