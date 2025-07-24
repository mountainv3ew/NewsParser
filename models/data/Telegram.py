from pydantic import BaseModel


class TelegramMessage(BaseModel):
    user_id: int
    text: str
