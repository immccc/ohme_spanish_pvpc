from pvpc.fetch import get
from datetime import datetime


def test_fetch():
    date = datetime(2025, 7, 1)
    pvpc = get(date)


    assert len(pvpc.prices_per_hour.keys()) == 24, "There should be 24 prices for each hour of the day"
    for hour in range(24):
        assert hour in pvpc.prices_per_hour, f"Price for hour {hour} is missing"
        assert isinstance(pvpc.prices_per_hour[hour], float), f"Price for hour {hour} should be a float"


