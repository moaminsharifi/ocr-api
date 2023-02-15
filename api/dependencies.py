from config import get_settings
from fastapi import Header, HTTPException

settings = get_settings()


async def get_token_header(token: str = Header()):
    if token != settings.api_token:
        raise HTTPException(status_code=403, detail="Token Is invalid ")
