from openai import OpenAI

from app.core.settings import settings

oa_client = OpenAI(api_key=settings.OPENROUTER_API_KEY, base_url="https://openrouter.ai/api/v1")
