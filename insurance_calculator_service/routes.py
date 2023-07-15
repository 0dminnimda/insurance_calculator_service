"""
App initialization and path/route handlers
"""

import logging
from datetime import date
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from .__metadata__ import __version__, module_name
from .models import CargoIn_Pydantic, Result, Tariffs
from .options import DB_URL

logger = logging.getLogger(module_name)

app = FastAPI(title="Insurance calculator", version=__version__)


@app.get("/ping", response_model=Result)
async def ping():
    logger.info("pong")
    return Result(message="pong")


@app.put("/set_tariffs", response_model=Result)
async def set_tariffs(tariffs: Dict[date, List[Dict[str, str]]]):
    await Tariffs.all().delete()

    for from_date, tariff_list in tariffs.items():
        for tariff in tariff_list:
            await Tariffs.create(
                cargo_type=tariff["cargo_type"],
                rate=tariff["rate"],
                effective_from_date=from_date,
            )
    return Result(message="Tariffs added successfully")


@app.post(
    "/insurance_cost",
    response_model=Result,
    responses={404: {"model": HTTPNotFoundError}},
)
async def insurance_cost(cargo: CargoIn_Pydantic):
    tariff = (
        await Tariffs.filter(
            effective_from_date__lte=date.today(), cargo_type=cargo.type
        )
        .order_by("-effective_from_date")
        .first()
    )
    if tariff is None:
        raise HTTPException(status_code=404, detail="Tariff not found")
    return Result(message=tariff.rate * cargo.price)


register_tortoise(
    app,
    db_url=DB_URL,
    modules={module_name: [f"{module_name}.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
