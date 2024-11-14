from pydantic import BaseModel
from typing import Optional


class VideoRequest(BaseModel):
    url: str
    min_length: Optional[int] = 100
    max_length: Optional[int] = 300
