from sqlalchemy import Column, Integer, String
from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="SENT")