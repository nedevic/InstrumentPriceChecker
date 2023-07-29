import httpx
import pytest
from asyncclick.testing import CliRunner

from app import main

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.parametrize(
    "input_rfq, expected_output",
    [
        ("fx_spot FX_INSTRUMENT 25 john.doe@gmail.com", 100),
        ("gold_call GOLD_INSTRUMENT 1 john.doe@gmail.com", 2000),
        ("bond BOND_INSTRUMENT 20 john.doe@gmail.com", 400),
    ],
)
@pytest.mark.asyncio
async def test_app_success(input_rfq, expected_output, caplog, monkeypatch):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def raise_for_status():
                pass

            @staticmethod
            def json():
                return {"price": expected_output}

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    runner = CliRunner()
    await runner.invoke(main, ["--rfq", input_rfq])
    assert f"The price for this rfq is: {expected_output}" in caplog.text


@pytest.mark.parametrize(
    "input_rfq, expected_output",
    [
        ("fx_spot INVALID_INSTRUMENT 25 john.doe@gmail.com", 100),
    ],
)
@pytest.mark.asyncio
async def test_app_failure_on_404_status(
    input_rfq, expected_output, caplog, monkeypatch
):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def raise_for_status():
                raise httpx.HTTPError("404: not found")

        return MockResponse()

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    runner = CliRunner()
    await runner.invoke(main, ["--rfq", input_rfq])
    assert "404: not found" in caplog.text


@pytest.mark.parametrize(
    "input_rfq, expected_output",
    [
        ("fx_spot FX_INSTRUMENT 25 notvalid", "email': ['Not a valid email address.']"),
        (
            "fx_spot FX_INSTRUMENT -5 john.doe@gmail.com",
            "'size': ['Must be greater than or equal to 0.'",
        ),
        (
            "fx_spot FX_INSTRUMENT notvalid john.doe@gmail.com",
            "'size': ['Not a valid number.']",
        ),
        (
            "notvalid FX_INSTRUMENT 25 john.doe@gmail.com",
            'type must have one of these values: "fx_spot", "gold_call", "bond"',
        ),
        (
            "notvalid",
            'Please enter a string with this format: "<type> <instrument> <size> <email>"',
        ),
        (
            "a b c d e",
            'Please enter a string with this format: "<type> <instrument> <size> <email>"',
        ),
        ("a b c d", "email': ['Not a valid email address.']"),
        ("a b c d", "'size': ['Not a valid number.']"),
    ],
)
@pytest.mark.asyncio
async def test_app_failure_on_bad_input(input_rfq, expected_output, caplog):
    runner = CliRunner()
    await runner.invoke(main, ["--rfq", input_rfq])
    assert expected_output in caplog.text
