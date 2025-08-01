from datetime import datetime, timedelta
import os

from charger._pvpc_conversions import get_save_request_from_pvpc
from charger.client import OhmeClientApiWithTariff
from pvpc.fetch import get as fetch_pvpc

async def _get_logged_client() -> OhmeClientApiWithTariff:
    client = OhmeClientApiWithTariff(
        os.getenv("OHME_EMAIL"),
        os.getenv("OHME_PASSWORD")
    )

    logged = await client.async_login()
    if not logged:
        raise ConnectionError("Unable to log in to Ohme")

    return client

async def create_tariff(name: str) -> None:
    date = datetime.today()
    
    pvc_tariffs_current_week = []

    current_weekday = date.weekday()
    for weekday in range(7):
        pvc_tariffs_current_week.insert(0, fetch_pvpc(date))

        delta = weekday - current_weekday if weekday <= current_weekday else weekday - current_weekday - 7
        date = datetime.today() + timedelta(days=delta)

    tariff_save_request = get_save_request_from_pvpc(name, *pvc_tariffs_current_week)

    async with await _get_logged_client() as client:
        await client.create_tariff(name, tariff_save_request)

    



