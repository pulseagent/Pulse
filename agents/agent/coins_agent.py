import json
import logging
from datetime import datetime, timezone
from typing import AsyncIterator

from agents.agent.abstract_agent import AbstractAgent
from agents.memory.memory import MemoryObject
from agents.memory.redis_memory import RedisMemory
from agents.models.openai import openai
from agents.prompts.tool_prompts import tool_prompt
from agents.protocol.inner.tool_output import ToolOutput
from agents.swarms.async_agent import AsyncAgent
from agents.tools import coin_tools, ai_search_tool

logger = logging.getLogger(__name__)


class CoinAgent(AbstractAgent):

    stop_condition = ["Final Answer:", "Tool Clarify: "]
    default_final_answer = "Sorry, I can't help with that. Try rephrasing or asking a related question for better results!"
    redis_memory: RedisMemory = RedisMemory()
    need_now_time: bool = True

    def __init__(self):
        def stopping_condition(response: str):
            for stop_word in self.stop_condition:
                if stop_word in response:
                    return True
            return False

        self.agent: AsyncAgent = AsyncAgent(
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
            async_tools=[
                ai_search_tool.ai_search
            ],
            max_loops=6,
            output_type="list",
            stopping_condition=stopping_condition,
            system_prompt="You are an Pulse Agent.Your can provide you with cryptocurrency information and transaction data, as well as assist in generating professional research reports on the crypto market. You can solve problems directly or utilize specialized tools to perform detailed tasks and deliver precise solutions.",
        )

    async def arun(self, query: str, conversation_id: str) -> AsyncIterator[str]:
        memory_list = self.redis_memory.get_memory_by_conversation_id(conversation_id)
        response = ""
        try:
            self.agent.short_memory.add(role="System Time", content=f"UTC Now: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
            for memory in memory_list:
                self.agent.add_memory_object(memory)

            is_finalized = False
            async for data in self.agent.acompletion(query):
                if isinstance(data, ToolOutput):
                    yield data.get_output()
                    response = "..."
                    is_finalized = True
                    continue
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
            logger.error("Error running the agent: {}", e, exc_info=True)
        finally:
            self.redis_memory.save_memory(conversation_id, MemoryObject(input=query, output=response))

    def send_message(self, message: str) -> str:
        return f'event: message\ndata: {json.dumps({"text": message}, ensure_ascii=False)}\n\n'
