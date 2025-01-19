from typing import List

from pydantic import BaseModel


class ToolInfo(BaseModel):
    type: str
    content: str

class AgentCreate(BaseModel):
    name: str
    description: str
    mode: str = 'ReAct'
    icon: str = None
    status: str = None
    tool_prompt: str = None
    max_loops: int = 5
    tenant_id: str = None
    tools: List[ToolInfo] = []

class AgentUpdate(BaseModel):
    name: str = None
    description: str = None
    mode: str = None

class ToolCreate(BaseModel):
    app_id: int
    type: str
    content: str

class ToolUpdate(BaseModel):
    type: str = None
    content: str = None

class DialogueRequest(BaseModel):
    user_id: str
    agent_id: int
    message: str

class DialogueResponse(BaseModel):
    response: str 