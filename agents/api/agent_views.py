from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from agents.common.response import RestResponse
from agents.models.db import get_db
from agents.models.response_models import AppModel
from agents.protocol.schemas import AgentCreate, AgentUpdate, DialogueResponse, DialogueRequest
from agents.services import agent_service

router = APIRouter()

@router.post("/agents/create")
async def create_agent(agent: AgentCreate, session: AsyncSession = Depends(get_db)):
    """
    Create a new agent.
    
    - **name**: Name of the agent
    - **description**: Description of the agent
    - **mode**: Mode of the agent, default is 'ReAct'
    - **icon**: Icon of the agent
    - **status**: Status of the agent
    - **tool_prompt**: Tool prompt for the agent
    - **max_loops**: Maximum loops for the agent, default is 5
    - **tenant_id**: Tenant ID for the agent
    """
    agent_id = await agent_service.create_agent(
        agent.name,
        agent.description,
        agent.mode,
        agent.icon,
        agent.status,
        agent.tool_prompt,
        agent.max_loops,
        agent.tenant_id,
        agent.tools,
        session
    )
    return RestResponse(data={"id": agent_id})

@router.get("/agents/get")
async def list_agents(session: AsyncSession = Depends(get_db)):
    """
    Retrieve a list of agents.
    """
    agents = await agent_service.list_agents(session)
    return RestResponse(data=[AppModel.from_orm(agent) for agent in agents])

@router.put("/agents/{agent_id}")
async def update_agent(agent_id: int, agent: AgentUpdate, session: AsyncSession = Depends(get_db)):
    """
    Update an existing agent.
    
    - **agent_id**: ID of the agent to update
    - **name**: New name of the agent
    - **description**: New description of the agent
    - **mode**: New mode of the agent
    """
    await agent_service.update_agent(agent_id, agent.name, agent.description, agent.mode,  session)
    return RestResponse(data="ok")

@router.delete("/agents/{agent_id}")
async def delete_agent(agent_id: int, session: AsyncSession = Depends(get_db)):
    """
    Delete an agent by setting its is_deleted flag to True.
    
    - **agent_id**: ID of the agent to delete
    """
    await agent_service.delete_agent(agent_id, session)
    return RestResponse(data="ok")

@router.post("/agents/{agent_id}/dialogue", response_model=DialogueResponse)
async def dialogue(agent_id: int, request: DialogueRequest):
    """
    Handle a dialogue between a user and an agent.
    
    - **agent_id**: ID of the agent to interact with
    - **user_id**: ID of the user
    - **message**: Message from the user
    """
    # Placeholder logic for generating a response
    response_text = f"Agent {agent_id} received your message: {request.message}"
    return DialogueResponse(response=response_text)
