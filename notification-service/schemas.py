from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    type: str
    status: str

    class Config:
        from_attributes = True