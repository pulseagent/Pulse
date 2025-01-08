import logging

from langchain.agents import create_react_agent
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class ReActAgent:
    def __init__(self):
        self.agent: Runnable = None

    def create_agent(self, tools: list) -> "ReActAgent":
        try:
            import langgraph

            llm = ChatOpenAI(model="gpt-4o", temperature=0.01)

            self.agent = create_react_agent(llm=llm,
                                            tools=tools)
            return self.agent
        except Exception as e:
            logger.error(e)
            return None

    async def astream(self, task_data: dict):
        if not self.agent:
            return None

        try:
            result = self.agent.astream(task_data)
            return result
        except Exception as e:
            logger.error(e)
            return None
