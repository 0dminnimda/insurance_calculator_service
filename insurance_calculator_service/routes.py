"""
App initialization and path/route handlers
"""

import logging
from datetime import date
from typing import Dict, List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .__metadata__ import __version__, module_name
from .models import Tariffs


logger = logging.getLogger(module_name)

app = FastAPI(
    title="Insurance calculator",
    version=__version__
)


@app.get("/ping")
async def ping() -> str:
    logger.info("pong")
    return "pong"


@app.post("/set_tariffs")
async def set_tariffs(tariffs: Dict[date, List[Dict[str, str]]]):
    for date_str, tariff_list in tariffs.items():
        for tariff in tariff_list:
            await Tariffs.create(
                cargo_type=tariff["cargo_type"],
                rate=tariff["rate"],
                effective_from_date=date_str
            )
    return {"message": "Tariffs added successfully"}


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={module_name: [f"{module_name}.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
