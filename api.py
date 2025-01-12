import uuid

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from agents.agent.ai_search_agent import ai_search_agent
from agents.agent.coins_agent import CoinAgent
from agents.logger import LogConfig
from lib.http_security import APIKeyMiddleware

app = FastAPI()
load_dotenv()


@app.get("/api/chat/completion")
async def completion(query: str = Query(default=""), conversationId: str = Query(default=str(uuid.uuid4()))):
    agent = CoinAgent()
    resp = agent.arun(query, conversationId)
    return StreamingResponse(content=resp, media_type="text/event-stream")

@app.get("/api/pulse/ai/search")
async def ai_search(query: str = Query(default="")):
    return StreamingResponse(content=ai_search_agent(query), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    log_config = LogConfig()
    log_config.setup_logging()
    app.add_middleware(APIKeyMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host='0.0.0.0', port=8080)