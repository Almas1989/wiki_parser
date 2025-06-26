import httpx
import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.api_key = settings.deepseek_api_key
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.timeout = 60  # seconds

    async def generate_summary(self, title: str, content: str) -> Optional[str]:
        try:
            prompt = f"""
            Создай краткое резюме (summary) для следующей статьи из Wikipedia.
            Резюме должно быть на русском языке, длиной 2-3 предложения,
            содержать основную суть статьи.

            Заголовок: {title}

            Содержание: {content[:3000]}

            Резюме:
            """

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты помощник, который создает краткие резюме статей Wikipedia на русском языке."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                response.raise_for_status()

                data = response.json()

                if data.get("choices"):
                    content = data["choices"][0]["message"]["content"].strip()
                    return content
                else:
                    logger.warning("Пустой ответ от DeepSeek API")
                    return None

        except Exception as e:
            logger.error(f"Ошибка при генерации summary через DeepSeek: {e}")
            return None
