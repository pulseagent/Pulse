from datetime import datetime

from pydantic import BaseModel


class AppModel(BaseModel):

    id: int
    name: str
    description: str
    mode: str
    icon: str
    status: str
    tool_prompt: str
    max_loops: int
    is_deleted: bool
    tenant_id: str
    update_time: datetime
    create_time: datetime

    class Config:
        orm_mode = True
        from_attributes = True