from pydantic import BaseModel, Field


class Env(BaseModel):
    TELEGRAM_BOT_TOKEN: str = None
    chat_id: str = None
    message_thread_id: int = None
    nats_server: str = Field("127.0.0.1")
    nats_user: str = None
    nats_password: str = None
    log_level: str = Field("info")


class MsgEvents(BaseModel):
    server_name: str
    rcon: str

