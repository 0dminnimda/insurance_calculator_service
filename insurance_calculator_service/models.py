from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tariffs(models.Model):
    id = fields.IntField(pk=True)
    effective_from_date = fields.DateField()
    cargo_type = fields.CharField(max_length=32)
    rate = fields.FloatField()


Tariff_Pydantic = pydantic_model_creator(Tariffs, name="Tariff")
