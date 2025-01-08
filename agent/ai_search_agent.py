from typing import AsyncGenerator

from agent.base import ReActAgent
from tools.get_crypto import GetCryptoDataTool
from tools.get_crypto_trend import GetCryptoTrendTool
from tools.score_calculator import ScoreCalculatorTool
from tools.twitter_search import TwitterSearchTool


async def ai_search_agent(query: str) -> AsyncGenerator:
    tools = [
        TwitterSearchTool(),
        GetCryptoDataTool(),
        GetCryptoTrendTool(),
        ScoreCalculatorTool()
    ]
    agent = ReActAgent().create_agent(tools)
    return agent.astream({"query": query})
