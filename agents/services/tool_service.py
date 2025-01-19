from fastapi import Depends
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from agents.models.db import get_db
from agents.models.models import Tool


async def create_tool(app_id: int, type: str, content: str, session: AsyncSession = Depends(get_db)):
    new_tool = Tool(app_id=app_id, type=type, content=content)
    session.add(new_tool)
    await session.commit()
    return new_tool.id

async def update_tool(tool_id: int, type: str = None, content: str = None, session: AsyncSession = Depends(get_db)):
    stmt = update(Tool).where(Tool.id == tool_id)\
        .values(type=type, content=content)\
        .execution_options(synchronize_session="fetch")
    await session.execute(stmt)
    await session.commit()

async def delete_tool(tool_id: int, session: AsyncSession = Depends(get_db)):
    stmt = update(Tool).where(Tool.id == tool_id)\
        .values(is_deleted=True)\
        .execution_options(synchronize_session="fetch")
    await session.execute(stmt)
    await session.commit() 