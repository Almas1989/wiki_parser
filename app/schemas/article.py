from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

class ArticleBase(BaseModel):
    url: str
    title: str
    content: str

class ArticleCreate(ArticleBase):
    parent_id: Optional[int] = None
    depth_level: int = 0

class ArticleResponse(ArticleBase):
    id: int
    summary: Optional[str] = None
    parent_id: Optional[int] = None
    depth_level: int
    is_processed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "url": "https://ru.wikipedia.org/wiki/Python",
                "title": "Python",
                "content": "Python — это язык программирования...",
                "summary": "Python — язык программирования общего назначения...",
                "parent_id": None,
                "depth_level": 0,
                "is_processed": True,
                "created_at": "2025-06-25T15:00:00",
                "updated_at": "2025-06-25T16:00:00"
            }
        }

class ParseRequest(BaseModel):
    url: HttpUrl

class SummaryResponse(BaseModel):
    url: str
    title: str
    summary: Optional[str] = None
    children_count: int