import json
import random
from datetime import date, timedelta
from typing import Dict, Iterable, List

import pytest
from httpx import AsyncClient
from utils import anyio_backend, client, do_test, setup

from insurance_calculator_service.models import Tariffs

setup()

PREVIOUS_DATE = str(date.today() - timedelta(days=30))
CURRENT_DATE = str(date.today())
NEXT_DATE = str(date.today() + timedelta(days=30))


CARGO_TYPES = [
    "Glass",
    "Electronics",
    "Other",
]


def random_nice_float(magnitude: float) -> float:
    return round(random.uniform(-magnitude, magnitude), 3)


def random_tarif_list(cargo_types: Iterable[str] = CARGO_TYPES) -> List[Dict[str, str]]:
    data = []

    for cargo_type in cargo_types:
        rate = random_nice_float(0.5)
        data.append({"cargo_type": cargo_type, "rate": str(rate)})

    return data


@pytest.mark.anyio
async def test_set_tariffs_empty(client: AsyncClient):
    data = {}
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 200, response.text

    count = await Tariffs.all().count()
    assert count == 0


@pytest.mark.anyio
async def test_set_tariffs(client: AsyncClient):
    # Set up tariffs
    data = {
        PREVIOUS_DATE: random_tarif_list(),
        CURRENT_DATE: random_tarif_list(),
    }
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 200, response.text

    count = await Tariffs.all().count()
    assert count == len(CARGO_TYPES) * len(data)

    for from_date, tariff_list in data.items():
        for tariff in tariff_list:
            count = await Tariffs.filter(
                effective_from_date=from_date,
                cargo_type=tariff["cargo_type"],
                rate=tariff["rate"],
            ).count()
            assert count == 1, (tariff, from_date)


@pytest.mark.anyio
async def test_insurance_cost(client: AsyncClient):
    # Set up tariffs
    data = {
        PREVIOUS_DATE: random_tarif_list(),
        CURRENT_DATE: random_tarif_list(),
    }
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 200, response.text

    for cargo_index, cargo_type in enumerate(CARGO_TYPES):
        price = random_nice_float(1000)
        cargo_data = {"type": cargo_type, "price": price}
        response = await client.post("/insurance_cost", json=cargo_data)
        assert response.status_code == 200, response.text

        rate = float(data[CURRENT_DATE][cargo_index]["rate"])
        assert json.loads(response.text) == {"message": str(rate * price)}


@pytest.mark.anyio
async def test_insurance_cost_nonexistant(client: AsyncClient):
    # Set up tariffs
    data = {
        PREVIOUS_DATE: random_tarif_list(),
        CURRENT_DATE: random_tarif_list(),
    }
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 200, response.text

    cargo_data = {"type": "New", "price": 420}
    response = await client.post("/insurance_cost", json=cargo_data)
    assert response.status_code == 404, response.text
    assert json.loads(response.text) == {"detail": "Tariff not found"}


# TODO: add more thorrough testing for insurance_cost


@pytest.mark.anyio
async def test_invalid_date_format(client: AsyncClient):
    data = {"2022/01/01": [{"cargo_type": "Glass", "rate": "0.05"}]}
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_invalid_rate_format(client: AsyncClient):
    data = {"2022-01-01": [{"cargo_type": "Glass", "rate": "5%"}]}
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_missing_rate_field(client: AsyncClient):
    data = {"2022-01-01": [{"cargo_type": "Glass"}]}
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 422, response.text


@pytest.mark.anyio
async def test_missing_cargo_type_field(client: AsyncClient):
    data = {"2022-01-01": [{"rate": "0.05"}]}
    response = await client.put("/set_tariffs", json=data)
    assert response.status_code == 422, response.text


if __name__ == "__main__":
    do_test(__file__)
