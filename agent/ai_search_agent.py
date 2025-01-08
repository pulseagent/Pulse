from agent.base import ReActAgent
from tools.twitter_search import TwitterSearchTool


async def ai_search_agent(query: str):
    tools = [
        TwitterSearchTool()
    ]
    agent = ReActAgent().create_agent(tools)
    return agent.astream({"query": query})
