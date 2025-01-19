from typing import AsyncIterator

from agents.agent.core.base import ReActAgent
from agents.agent.tools.get_crypto import GetCryptoDataTool
from agents.agent.tools.get_crypto_trend import GetCryptoTrendTool
from agents.agent.tools.score_calculator import ScoreCalculatorTool
from agents.agent.tools.twitter_search import TwitterSearchTool


async def ai_search_agent(query: str) -> AsyncIterator:
    tools = [
        TwitterSearchTool(),
        GetCryptoDataTool(),
        GetCryptoTrendTool(),
        ScoreCalculatorTool()
    ]
    agent = ReActAgent().create_agent(tools)
    yield agent.astream({"query": query})
