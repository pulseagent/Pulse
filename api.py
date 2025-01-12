import uuid

import uvicorn
from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from agents.agent.ai_search_agent import ai_search_agent
from agents.agent.coins_agent import CoinAgent

from agents.common.log import Log
from agents.tools.coin_tools import init_id_maps
from lib.http_security import APIKeyMiddleware

app = FastAPI()


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/chat/completion")
async def completion(query: str = Query(default=""), conversationId: str = Query(default=str(uuid.uuid4()))):
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
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host='0.0.0.0', port=8080)