import json
import logging
import sys
from typing import AsyncIterator

from rich.traceback import install

from agents.agent.abstract_agent import AbstractAgent
from agents.memory.local_memory import local_memory
from agents.memory.memory import MemoryObject
from agents.models.openai import openai
from agents.prompts.tool_prompts import tool_prompt
from agents.swarms.agent import Agent
from agents.tools import coin_tools

logger = logging.getLogger(__name__)


class CoinAgent(AbstractAgent):

    stop_condition = ["Final Answer:", "Tool Clarify: "]
    default_final_answer = "Sorry, I can't help with that. Try rephrasing or asking a related question for better results!"

    def __init__(self):
        def stopping_condition(response: str):
            for stop_word in self.stop_condition:
                if stop_word in response:
                    return True
            return False

        self.agent: Agent = Agent(
            agent_name="Pulse Agent",
            llm=openai.get_model(),
            tool_system_prompt=tool_prompt(),
            tools=[
                coin_tools.query_price_by_ids,
                coin_tools.query_historical_data_by_ids,
                coin_tools.query_markets_by_currency,
                coin_tools.query_top_gainers_losers,
                coin_tools.query_token_price_by_id,
            ],
            max_loops=6,
            output_type="list",
            stopping_condition=stopping_condition,
            system_prompt="You are an intelligent and efficient assistant. Your primary responsibility is to assist users by addressing their questions and providing accurate information. You can solve problems directly or utilize specialized tools to perform detailed tasks and deliver precise solutions.",
        )

    async def arun(self, query: str, conversation_id: str) -> AsyncIterator[str]:
        memory_list = local_memory.get_memory_by_conversation_id(conversation_id)
        response = ""
        try:
            for memory in memory_list:
                self.agent.add_memory(memory)
            is_finalized = False
            async for data in self.agent.run_stream(query):
                if not isinstance(data, str):
                    continue
                for stop_word in self.stop_condition:
                    if data and stop_word in data:
                        data = data.replace(stop_word, "")
                response += data
                is_finalized = True
                if data:
                    yield self.send_message(data)
            if not is_finalized:
                yield self.send_message(self.default_final_answer)
        except Exception as e:
            print(f"Error occurred: {e}", file=sys.stderr)
            logger.error("Error running the agent: {}", e, exc_info=True)
        finally:
            local_memory.save_memory(conversation_id, MemoryObject(input=query, output=response))

    def send_message(self, message: str) -> str:
        return f'event: message\ndata: {json.dumps({"text": message}, ensure_ascii=False)}\n\n'
