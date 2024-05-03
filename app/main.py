import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

from app.config import CONFIG, log
from app.routers import tags_metadata, routers

middleware = [
    Middleware(ContextMiddleware, plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin())),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=["*"],
    ),
]

app = FastAPI(
    title=CONFIG.PROJECT_NAME,
    middleware=middleware,
    openapi_tags=tags_metadata,
    description=CONFIG.DESCRIPTION,
    version=CONFIG.VERSION,
)

p = pathlib.Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=p, html=True), name="static")

# routers are dynamically collected in routers.__init__.py file
for router in sorted(routers, key=lambda x: x.router.tags[0]):
    app.include_router(router.router)


@app.get("/healthcheck/alive")
async def healthcheck():
    """
    Simple endpoint to check if the service is alive
    """
    return {"message": "I'm alive!"}


@app.get("/healthcheck/environment")
async def environment():
    """
    Endpoint to check whether backend is running in right environment.

    Returns:
        the current environment as well as the respective sql servers
    """
    response = {
        "environment": [CONFIG.MODE],
        "sqlserver": [CONFIG.SQLSRV_SERVER],
        "bisqlserver": [CONFIG.BISQL_SERVER],
    }

    return response


# MUST be located after last route definition to include all routes
api_routes = app.routes

if __name__ == "__main__":
    log.info("starting API service")
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT)
