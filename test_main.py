from pytest_mock import MockerFixture
import pytest
import main

@pytest.fixture()
def mocked_tariff_creation(mocker: MockerFixture) -> dict:
    called_with = {}
    async def fake_create_tariff(name):
        called_with['name'] = name

    mocker.patch("main.create_tariff", side_effect=fake_create_tariff)
    return called_with


@pytest.mark.parametrize(
    "provided_tariff_name,expected_tariff_name",
    [
        (None, "PVPC"),
        ("TestTariff", "TestTariff"),
    ]
)
def test_create_tariff_called_with_name(mocked_tariff_creation: dict, provided_tariff_name: str, expected_tariff_name: str):
    args = main.parse_args(["--name", provided_tariff_name] if provided_tariff_name else [])
    main.main(args)

    assert mocked_tariff_creation['name'] == expected_tariff_name
