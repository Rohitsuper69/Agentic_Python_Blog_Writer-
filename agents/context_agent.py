import aiohttp
import asyncio
import sys
import os

# Add the project root to sys.path to access config and utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import NEWSDATA_API_KEY 
from utils.helpers import retry

class ContextAgent:
    def __init__(self, topic, subtopics):
        self.topic = topic
        self.subtopics = subtopics

    @retry()
    async def fetch_news(self, session):
        """
        Fetch latest news articles related to the subtopics using the NewsData API.
        Returns top 3 article titles and links.
        """
        url = f"https://newsdata.io/api/1/latest?apikey={NEWSDATA_API_KEY}&q="
        for subtopic in self.subtopics:
            url += subtopic + " AND "
        url = url[:-5]  # Remove trailing ' AND '

        async with session.get(url) as resp:
            data = await resp.json()
            return [
                {
                    "title": a["title"],
                    "link": a["link"]
                } for a in data.get("results", [])[:3]
            ]

    @retry()
    async def fetch_keywords(self, session):
        """
        Fetch related keywords for each subtopic using the Datamuse API.
        """
        res = []
        for subtopic in self.subtopics:
            url = f"https://api.datamuse.com/words?ml={subtopic}&max=10"
            async with session.get(url) as resp:
                data = await resp.json()
                res.append([w["word"] for w in data])
        return res

    @retry()
    async def fetch_quote(self, session):
        """
        Fetch a random quote related to the subtopics using the Quoteslate API.
        """
        url = "https://quoteslate.vercel.app/api/quotes/random?tags="
        for subtopic in self.subtopics:
            url += subtopic + ','
        url = url[:-1]  # Remove trailing comma

        async with session.get(url) as resp:
            data = await resp.json()
            return {
                "content": data.get("content"),
                "author": data.get("author")
            }

    async def gather_context(self):
        """
        Gathers contextual data including news, keywords, and a quote concurrently.
        """
        async with aiohttp.ClientSession() as session:
            news_task = self.fetch_news(session)
            keywords_task = self.fetch_keywords(session)
            quote_task = self.fetch_quote(session)

            news, keywords, quote = await asyncio.gather(
                news_task,
                keywords_task,
                quote_task
            )

        return {
            "news": news,
            "keywords": keywords,
            "quote": quote
        }
