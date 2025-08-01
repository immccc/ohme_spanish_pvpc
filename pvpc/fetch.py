from datetime import datetime

import requests

from pvpc.model import PVPC


_URL = "https://api.esios.ree.es/archives/70/download_json?locale=es"


def get(timestamp: datetime):
    """
    Fetches PVPC data for a particular date.

    Parameters:
        timestamp (datetime.datetime): The date for which to fetch energy price per hour.

    Returns:
        dict: A dictionary containing the energy price per hour for the specified date.
        None: If there was an error fetching the data.
    """
    response = requests.get(f"{_URL}&date={timestamp.strftime('%Y-%m-%d')}",)
    response.raise_for_status()

    return _map(response.json())
    
def _map(data: dict) -> PVPC:
    price_per_hour = {}
    date = datetime.strptime(data["PVPC"][0]["Dia"], "%d/%m/%Y")

    for day in data["PVPC"]:
        hour = int(day["Hora"].split("-")[0])
        price = float(day["PCB"].replace(",", ".")) / 100

        price_per_hour[hour] = price

    return PVPC(
        date=date,
        prices_per_hour=price_per_hour,
    )

    