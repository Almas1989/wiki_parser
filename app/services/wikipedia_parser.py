import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional

from app.schemas.article import ArticleCreate
from app.repositories.article_repository import ArticleRepository
from app.config import settings


class WikipediaParserService:
    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository
        self.max_depth = settings.max_recursion_depth
        self.processed_urls: Set[str] = set()

    async def parse_article_recursive(
        self,
        url: str,
        parent_id: Optional[int] = None,
        depth: int = 0
    ) -> Optional[int]:
        if depth >= self.max_depth or url in self.processed_urls:
            return None

        self.processed_urls.add(url)

        # Проверяем, существует ли уже статья
        if await self.article_repository.exists_by_url(url):
            existing_article = await self.article_repository.get_by_url(url)
            return existing_article.id if existing_article else None

        try:
            async with aiohttp.ClientSession() as session_http:
                async with session_http.get(url) as response:
                    if response.status != 200:
                        print(f"Ошибка получения страницы {url}")
                        return None

                    html = await response.text()
                    soup = BeautifulSoup(html, 'lxml')

                    # Заголовок
                    title_element = soup.find('h1', {'class': 'firstHeading'})
                    title = title_element.get_text(strip=True) if title_element else "Без названия"

                    # Контент
                    content_div = soup.find('div', {'id': 'mw-content-text'})
                    if not content_div:
                        print(f"Не найден контент на странице {url}")
                        return None

                    for element in content_div.find_all(['div', 'table'],
                        {'class': ['navbox', 'infobox', 'metadata', 'ambox']}):
                        element.decompose()

                    content = content_div.get_text(strip=True)[:5000]

                    # Создаем статью
                    article_data = ArticleCreate(
                        url=url,
                        title=title,
                        content=content,
                        parent_id=parent_id,
                        depth_level=depth
                    )

                    article = await self.article_repository.create(article_data)

                    # Ссылки
                    if depth < self.max_depth - 1:
                        wiki_links = self._extract_wikipedia_links(soup, url)
                        limited_links = wiki_links[:3]

                        for link in limited_links:
                            await self.parse_article_recursive(link, parent_id=article.id, depth=depth + 1)

                    return article.id

        except Exception as e:
            print(f"Ошибка при парсинге {url}: {str(e)}")
            return None

    def _extract_wikipedia_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        links = []
        parsed_base = urlparse(base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/') and ':' not in href and '#' not in href:
                full_url = urljoin(base_domain, href)
                if full_url not in self.processed_urls:
                    links.append(full_url)

        return links[:10]  # максимум 10 ссылок
