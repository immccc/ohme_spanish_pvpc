import datetime
from pydantic import BaseModel
import pydantic


class PVPC(BaseModel):
    """
    Represents the energy price per hour for a particular date from REE.
    """

    date: datetime.datetime
    """
    The date for which the energy price is applicable.
    """

    prices_per_hour: dict[int, float]
    """
    The energy price per hour in euros.
    """


    @pydantic.field_validator("prices_per_hour")
    @classmethod
    def validate_hour_keys(cls, prices_per_hour: dict[int, float]) -> dict[int, float]:
        if not all(0 <= hour <= 23 for hour in prices_per_hour.keys()):
            raise ValueError("Hour for prices must be between 0 and 23")
        return prices_per_hour


    def __str__(self):
        return f"PVPC(date={self.date}, prices_per_hour={self.price})"
