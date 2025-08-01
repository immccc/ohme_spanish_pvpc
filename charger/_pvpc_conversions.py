import datetime
from charger.model import PricingPeriod, TariffSaveRequest
from pvpc.model import PVPC



def get_save_request_from_pvpc(name: str, *pvpc_tariffs_last_7_days: PVPC) -> TariffSaveRequest:
    return TariffSaveRequest(
        defaultPrice=1.0,
        dstSensitive=True,
        pricingSchedule=[ 
            PricingPeriod(
                activeDays=[pvpc.date.strftime("%A").upper()],
                endTime=datetime.datetime(hour=(hour + 1) % 24, minute=0, year=pvpc.date.year, month=pvpc.date.month, day=pvpc.date.day).strftime("%H:%M"),
                id="",
                price=round(price, 4)*100,
                startTime=datetime.datetime(hour=hour, minute=0, year=pvpc.date.year, month=pvpc.date.month, day=pvpc.date.day).strftime("%H:%M"),
            ) for pvpc in pvpc_tariffs_last_7_days for hour, price in pvpc.prices_per_hour.items()
        ],
        supplierDisplayName=name,
        timeZone="Europe/Madrid"
    )

