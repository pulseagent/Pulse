import json
import logging
from typing import AsyncIterator

from agents.agent.abstract_agent import AbstractAgent
from agents.memory.local_memory import local_memory
from agents.memory.memory import MemoryObject
from agents.models.openai import openai
from agents.prompts.tool_prompts import tool_prompt
from agents.swarms.agent import Agent
from agents.tools import coin_tools

logger = logging.getLogger(__name__)

class CoinAgent(AbstractAgent):

    def __init__(self):
        def stopping_condition(response: str):
            return "Final Answer:" in response

        self.agent: Agent = Agent(
            agent_name="Coins Agent",
            llm=openai.get_model(),
            tool_system_prompt=tool_prompt(),
            tools=[
                coin_tools.query_markets_by_ids,
                coin_tools.query_price_by_ids,
                coin_tools.query_historical_data_by_ids
            ],
            max_loops=5,
            output_type="list",
            stopping_condition=stopping_condition,
            system_prompt="You are Coins Agent, a highly intelligent and efficient assistant. Your primary responsibility is to assist users by answering their queries about Coins. You can leverage specialized tools to perform accurate and detailed Coins-related queries on behalf of users.",
        )

    async def arun(self, query: str, conversation_id: str) -> AsyncIterator[str]:
        memory_list = local_memory.get_memory_by_conversation_id(conversation_id)
        response = ""
        try:
            for memory in memory_list:
                self.agent.add_memory(memory)
            async for data in self.agent.run_stream(query):
                if not isinstance(data, str):
                    continue
                if data and data.startswith("Final Answer:"):
                    data = data.replace("Final Answer:", "")
                response += data
                if data:
                    yield f'event: message\ndata: {json.dumps({"text": data}, ensure_ascii=False)}\n\n'
        except Exception as e:
            logger.error("Error running the agent: {}", e, exc_info=True)
        finally:
            local_memory.save_memory(conversation_id, MemoryObject(input=query, output=response))
