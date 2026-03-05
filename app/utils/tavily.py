from tavily.tavily import TavilyClient

from app.core.settings import settings

tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)
