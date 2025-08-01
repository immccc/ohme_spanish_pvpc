from typing import Optional
from pydantic import BaseModel

class Price(BaseModel):
    currencyCode: str
    amount: str

class PricePeriod(BaseModel):
    startTime: int
    durationMinutes: int
    costPerKWH: Price

class PeriodGroup(BaseModel):
    title: str
    tariffPeriods: list[PricePeriod]

class TariffInfo(BaseModel):
    """
    Represents the tariff information for charging in Ohme.
    """

    tariffNamename: str
    logoUrl: str
    distinctPrices: int
    lowestPrice: Price
    highestPrice: Price
    cheapestPeriod: PricePeriod
    periodGroups: list[PeriodGroup]

class UserDefinedTariff(BaseModel):
    id: str
    supplierId: str
    supplierDisplayName: str
    tariffDisplayName: str
    currencyCode: str
    currencyUnit: str
    logoUrl: Optional[str]
    weekdayTariff: list
    weekendTariff: list
    periodLengthInMinutes: int
    timeZone: str

class TariffGetResponse(BaseModel):
    """
    Represents a tariff for charging in Ohme.
    """
    tariffInfo: TariffInfo
    userDefinedTariff: UserDefinedTariff


class PricingPeriod(BaseModel):
    """
    Represents a pricing period for a tariff to be saved.
    """
    activeDays: list[str]
    endTime: str
    id: str
    price: float
    startTime: str


class TariffSaveRequest(BaseModel):
    """
    Represents a request to save a tariff in Ohme.
    """
    defaultPrice: float
    dstSensitive: bool
    pricingSchedule: list[PricingPeriod]
    supplierDisplayName: str
    timeZone: str