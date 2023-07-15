from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Result(BaseModel):
    message: str


class Tariffs(models.Model):
    id = fields.IntField(pk=True)
    effective_from_date = fields.DateField()
    cargo_type = fields.CharField(max_length=32)
    rate = fields.FloatField()


TariffListItem_Pydantic = pydantic_model_creator(
    Tariffs,
    name="TariffListItem",
    exclude=("effective_from_date",),
    exclude_readonly=True,
)


class Cargo(models.Model):
    type = fields.CharField(max_length=32)
    price = fields.FloatField()

    class Meta:
        table = None


CargoIn_Pydantic = pydantic_model_creator(Cargo, name="Cargo", exclude_readonly=True)
