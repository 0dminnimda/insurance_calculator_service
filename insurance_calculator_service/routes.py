"""
App initialization and path/route handlers
"""

import logging

from fastapi import FastAPI

from . import __name__ as module_name, __version__


logger = logging.getLogger(module_name)


app = FastAPI(
    title="Insurance calculator",
    version=__version__
)


@app.get("/ping")
async def ping() -> str:
    logger.info("pong")
    return "pong"
