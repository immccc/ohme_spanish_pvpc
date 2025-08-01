from ohme import AuthException
import pytest
from charger.tariffs import create_tariff

@pytest.fixture
def with_wrong_credentials(monkeypatch):
    monkeypatch.setenv("OHME_EMAIL", "asdf")
    monkeypatch.setenv("OHME_PASSWORD", "qwerty")

@pytest.mark.asyncio
async def test_create_tariff_fails_with_wrong_credentials(with_wrong_credentials):
    with pytest.raises(AuthException):
        await create_tariff("PVPC")


@pytest.mark.asyncio
async def test_create_succeeds_with_right_credentials():
    await create_tariff("PVPC")
