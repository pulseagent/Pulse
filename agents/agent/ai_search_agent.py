from typing import AsyncIterator

from agents.agent.base import ReActAgent
from agents.tools.get_crypto import GetCryptoDataTool
from agents.tools.get_crypto_trend import GetCryptoTrendTool
from agents.tools.score_calculator import ScoreCalculatorTool
from agents.tools.twitter_search import TwitterSearchTool


async def ai_search_agent(query: str) -> AsyncIterator:
    tools = [
        TwitterSearchTool(),
        GetCryptoDataTool(),
        GetCryptoTrendTool(),
        ScoreCalculatorTool()
    ]
    agent = ReActAgent().create_agent(tools)
    yield agent.astream({"query": query})
