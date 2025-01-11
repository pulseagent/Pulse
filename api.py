import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles

from agents.agent.ai_search_agent import ai_search_agent
from agents.agent.coins_agent import CoinAgent
from agents.logger import LogConfig
from agents.protocol.chat import ChatCompletionRequest

app = FastAPI()
load_dotenv()


@app.post("/chat/completion")
async def completion(chat_request: ChatCompletionRequest):
    agent = CoinAgent()
    resp = agent.arun(chat_request.query, chat_request.conversation_id)
    return StreamingResponse(content=resp, media_type="text/event-stream")

@app.get("/api/pulse/ai/search")
async def ai_search(query: str = Query(default="")):
    return StreamingResponse(content=ai_search_agent(query), media_type="text/event-stream")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == '__main__':
    log_config = LogConfig()
    log_config.setup_logging()
    uvicorn.run(app, host='0.0.0.0', port=8080)