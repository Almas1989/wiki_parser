from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.article_repository import ArticleRepository
from app.services.wikipedia_parser import WikipediaParserService
from app.services.ai_service import AIService
from app.schemas.article import ParseRequest, SummaryResponse

router = APIRouter()

async def get_article_repository(db: AsyncSession = Depends(get_db)) -> ArticleRepository:
    return ArticleRepository(db)

async def get_wikipedia_parser(
    article_repo: ArticleRepository = Depends(get_article_repository)
) -> WikipediaParserService:
    return WikipediaParserService(article_repo)

async def get_ai_service() -> AIService:
    return AIService()

@router.post("/parse")
async def parse_wikipedia_article(
    request: ParseRequest,
    background_tasks: BackgroundTasks,
    parser: WikipediaParserService = Depends(get_wikipedia_parser)
):
    """Запуск парсинга статьи Wikipedia с рекурсивным обходом ссылок"""

    background_tasks.add_task(parser.parse_article_recursive, str(request.url))

    return {
        "message": "Парсинг запущен в фоновом режиме",
        "url": str(request.url)
    }

@router.get("/summary")
async def get_article_summary(
    url: str,
    article_repo: ArticleRepository = Depends(get_article_repository),
    ai_service: AIService = Depends(get_ai_service)
) -> SummaryResponse:
    """Получение summary статьи по URL"""

    article = await article_repo.get_by_url(url)
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    # Если summary еще не создан, создаем его
    if not article.summary and article.parent_id is None:  # Только для корневых статей
        summary = await ai_service.generate_summary(article.title, article.content)
        if summary:
            await article_repo.update_summary(article.id, summary)
            article.summary = summary

    # Подсчитываем количество дочерних статей
    children_count = len(article.children) if hasattr(article, 'children') else 0

    return SummaryResponse(
        url=article.url,
        title=article.title,
        summary=article.summary,
        children_count=children_count
    )