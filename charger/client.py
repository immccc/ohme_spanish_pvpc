from ohme import OhmeApiClient

from charger.model import TariffGetResponse, TariffSaveRequest
from pvpc.model import PVPC

class OhmeClientApiWithTariff(OhmeApiClient):
    async def create_tariff(self, name: str, tariff: TariffSaveRequest) -> None:
        await self._make_request(
                "POST", f"/v1/users/me/custom-tariff",
            data=tariff.model_dump()
        )



