import logging

import fastapi
import uvicorn
from fastapi import Query
from sse_starlette import EventSourceResponse

from agent.ai_search_agent import ai_search_agent

logger = logging.getLogger(__name__)

app = fastapi.FastAPI()


@app.get("/api/pulse/ai/search")
async def ai_search(query: str = Query(default="")):
    return EventSourceResponse(ai_search_agent(query))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="warning")
