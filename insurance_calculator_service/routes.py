"""
App initialization and path/route handlers
"""

import logging
from datetime import date
from typing import Dict, List

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from .__metadata__ import __version__, module_name
from .models import Tariffs, Result

logger = logging.getLogger(module_name)

app = FastAPI(title="Insurance calculator", version=__version__)


@app.get("/ping", response_model=Result)
async def ping():
    logger.info("pong")
    return Result(message="pong")


@app.put("/set_tariffs", response_model=Result)
async def set_tariffs(tariffs: Dict[date, List[Dict[str, str]]]):
    for from_date, tariff_list in tariffs.items():
        for tariff in tariff_list:
            await Tariffs.create(
                cargo_type=tariff["cargo_type"],
                rate=tariff["rate"],
                effective_from_date=from_date,
            )
    return Result(message="Tariffs added successfully")


register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={module_name: [f"{module_name}.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
