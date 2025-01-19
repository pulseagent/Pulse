import logging

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from agents.agent.tools.coin_tools import init_id_maps
from agents.api import agent_views, api_views, file_views, tool_views
from agents.common.config import SETTINGS
from agents.common.log import Log
from agents.common.otel import Otel, OtelFastAPI
from lib.http_security import APIKeyMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(agent_views.router, prefix="/api")
app.include_router(api_views.router, prefix="/api")
app.include_router(file_views.router, prefix="/api")
app.include_router(tool_views.router, prefix="/api")
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