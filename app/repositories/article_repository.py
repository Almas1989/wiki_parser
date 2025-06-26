from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.article import Article
from app.schemas.article import ArticleCreate


class ArticleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, article_data: ArticleCreate) -> Article:
        article = Article(**article_data.model_dump())
        self.db.add(article)
        await self.db.commit()
        await self.db.refresh(article)
        return article

    async def get_by_url(self, url: str) -> Optional[Article]:
        query = (
            select(Article)
            .options(selectinload(Article.children))
            .where(Article.url == url)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, article_id: int) -> Optional[Article]:
        query = (
            select(Article)
            .options(selectinload(Article.children))
            .where(Article.id == article_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_unprocessed_root_articles(self) -> List[Article]:
        query = (
            select(Article)
            .where(
                Article.parent_id.is_(None),
                Article.is_processed == False
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_summary(self, article_id: int, summary: str) -> None:
        query = (
            update(Article)
            .where(Article.id == article_id)
            .values(
                summary=summary,
                is_processed=True
            )
        )
        await self.db.execute(query)
        await self.db.commit()

    async def exists_by_url(self, url: str) -> bool:
        query = select(Article.id).where(Article.url == url)
        result = await self.db.execute(query)
        return result.scalar_one_or_none() is not None
