import json
from ohme import AuthException
import pytest
from charger import tariffs

class MockOhmeHttpResponse:
    status = 200
    json_data: dict[str, any]

    def __init__(self, json_data: dict[str, any]={}):
        self.json_data = json_data

    async def json(self):
        return self.json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class MockOhmeHttpClientSession:
    called_payloads: list
    session_response: dict[str, any]

    def __init__(self, session_response: dict[str, any], called_payloads: list, *args, **kwargs):
        self.session_response = session_response
        self.called_payloads = called_payloads

    def post(self, *_, **__):
        return MockOhmeHttpResponse(self.session_response)

    def request(self, *_, **kwargs):
        self.called_payloads.append(kwargs.get("data"))
        return MockOhmeHttpResponse()

    async def close(self):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, _, __, ___):
        pass


@pytest.fixture
def with_ohme_credentials(monkeypatch):
    monkeypatch.setenv("OHME_EMAIL", "asdf")
    monkeypatch.setenv("OHME_PASSWORD", "qwerty")

@pytest.mark.asyncio
async def test_create_tariff_fails_with_wrong_credentials(with_ohme_credentials):
    # Connecting to non mocked Ohme API will fail
    with pytest.raises(AuthException):
        await tariffs.create_tariff("PVPC")


@pytest.mark.asyncio
async def test_create_succeeds_with_right_credentials(monkeypatch, with_ohme_credentials):

    received_payload = []

    monkeypatch.setattr(
        "aiohttp.ClientSession",
        lambda : MockOhmeHttpClientSession(
            {
                "idToken": "1",
                "refreshToken": "2",
            }, received_payload
        ),
        raising=False
    )

    await tariffs.create_tariff("PVPC")

    _assert_tariff_is_created_from_current_week(json.loads(received_payload[0]))

def _assert_tariff_is_created_from_current_week(ohme_tariff_request_as_json: dict[str, any]) -> None:
    assert ohme_tariff_request_as_json["pricingSchedule"]
    assert isinstance(ohme_tariff_request_as_json["pricingSchedule"], list)

    actual_days_hour_count = {}
    for price in ohme_tariff_request_as_json["pricingSchedule"]:
        assert len(price["activeDays"]) == 1, "Price should apply only for one specific day"
        actual_days_hour_count[price["activeDays"][0]] = actual_days_hour_count.get(price["activeDays"][0], 0) + 1

        assert price["price"] >= 1, "Price should be in cents and greater than 1 (don't ask me, it's just how Ohme API operates)"

        _assert_price_time_range(price)

    _assert_tariff_days(actual_days_hour_count)


def _assert_tariff_days(actual_days_hour_count: dict[str, int]):
    assert actual_days_hour_count.keys() == {"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"}, \
       "Price should apply for all days of the week"
    
    wrong_days = {day: count for day, count in actual_days_hour_count.items() if count != 24}
    assert not wrong_days, f"Price should apply for all 24 hours of the day, but got: {wrong_days}"

def _assert_price_time_range(price: dict):
    startTime = price["startTime"].split(":")
    endTime = price["endTime"].split(":")

    assert startTime[1] == "00", "Start time hour should not have minutes"
    assert endTime[1] == "00", "End time hour should not have minutes"

    if int(endTime[0]) == 0:
        assert int(startTime[0]) == 23, "Price should apply for just one hour"
    else:
        assert int(endTime[0]) - int(startTime[0]) == 1, "Price should apply for just one hour"
