import logging
import uuid

import uvicorn
from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from agents.agent.ai_search_agent import ai_search_agent
from agents.agent.coins_agent import CoinAgent
from agents.common.config import SETTINGS
from agents.common.log import Log
from agents.common.otel import Otel, OtelFastAPI
from agents.tools.coin_tools import init_id_maps
from lib.http_security import APIKeyMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/chat/completion")
async def completion(query: str = Query(default=""), conversationId: str = Query(default=str(uuid.uuid4()))):
    logger.info(f"query: {query}, conversationId: {conversationId}")
    agent = CoinAgent()
    resp = agent.arun(query, conversationId)
    return StreamingResponse(content=resp, media_type="text/event-stream")

@app.get("/api/pulse/ai/search")
async def ai_search(query: str = Query(default="")):
    return StreamingResponse(content=ai_search_agent(query), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

def init_app():
    init_id_maps()

if __name__ == '__main__':
    Log.init()
    Otel.init()
    logger.info("Server started.")
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_app()
    OtelFastAPI.init(app)
    uvicorn.run(app, host=SETTINGS.HOST, port=SETTINGS.PORT)