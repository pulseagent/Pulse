from swarms import Agent

from agents.agent.core.abstract_agent import AbstractAgent
from agents.agent.llm.openai import openai
from agents.agent.prompts.tool_prompts import tool_prompt
from agents.agent.tools import demo_tool


class SimpleAgent(AbstractAgent):

    def __init__(self):
        self.agent: Agent = Agent(
            agent_name="Terminal-Agent",
            llm=openai.get_model(),
            tool_system_prompt=tool_prompt(),
            tools=[demo_tool.terminal],
            prompt_template="{system_prompt}\n\n{tool_prompt}\n\n{user_prompt}",
            max_loops=2,
            output_type="list",
            system_prompt="You are an agent that can execute terminal commands. Use the tools provided to assist the user.",
        )

    async def arun(self, query: str, conversation_id: str) -> str:
        results = await self.agent.arun(query)
        return results[-1]