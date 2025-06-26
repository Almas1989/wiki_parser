from dependency_injector import containers, providers
from app.database import AsyncSessionLocal
from app.repositories.article_repository import ArticleRepository
from app.services.wikipedia_parser import WikipediaParserService
from app.services.ai_service import AIService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.api.v1.routes"]  # укажи путь к файлу с роутерами
    )

    # Database
    db = providers.Factory(AsyncSessionLocal)

    # Repositories
    article_repository = providers.Factory(
        ArticleRepository,
        db=db
    )

    # Services
    wikipedia_parser_service = providers.Factory(
        WikipediaParserService,
        article_repository=article_repository
    )

    ai_service = providers.Factory(AIService)
