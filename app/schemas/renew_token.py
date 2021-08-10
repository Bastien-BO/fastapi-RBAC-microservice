from pydantic import BaseModel


class RenewToken(BaseModel):
    refresh_token: str
