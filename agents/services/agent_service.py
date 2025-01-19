from typing import List

from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from agents.models.db import get_db
from agents.models.models import App, Tool
from agents.protocol.schemas import ToolInfo


async def create_agent(
        name: str,
        description: str,
        mode: str = 'ReAct',
        icon: str = None,
        status: str = None,
        tool_prompt: str = None,
        max_loops: int = 5,
        tenant_id: str = None,
        tools: List[ToolInfo] = [],
        session: AsyncSession = Depends(get_db)):
    async with session.begin():
        new_agent = App(
            name=name,
            description=description,
            mode=mode,
            icon=icon,
            status=status,
            tool_prompt=tool_prompt,
            max_loops=max_loops,
            tenant_id=tenant_id
        )
        session.add(new_agent)
        await session.flush()  # Ensure new_agent.id and new_agent.uuid are available

        # Create Tool records
        for tool in tools:
            new_tool = Tool(app_id=new_agent.id, type=tool.type, content=tool.content)
            session.add(new_tool)

    return new_agent.id  # Return ID instead of UUID

async def list_agents(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(App).where(App.is_deleted == False))
    return result.scalars().all()

async def update_agent(
        agent_id: int,
        name: str = None,
        description: str = None,
        mode: str = None,
        session: AsyncSession = Depends(get_db)):
    stmt = update(App).where(App.id == agent_id)\
        .values(name=name, description=description, mode=mode)\
        .execution_options(synchronize_session="fetch")
    await session.execute(stmt)
    await session.commit()

async def delete_agent(agent_id: int, session: AsyncSession = Depends(get_db)):
    stmt = update(App).where(App.id == agent_id)\
        .values(is_deleted=True)\
        .execution_options(synchronize_session="fetch")
    await session.execute(stmt)
    await session.commit()
