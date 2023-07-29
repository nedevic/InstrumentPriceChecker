import httpx
import pytest

from enums.rfq import RfqType
from utils.price import get_price_data
from validators.rfq import validate_rfq


class TestRfqValidator:
    def test_success(self):
        validated, _ = validate_rfq(rfq="fx_spot FX_INSTRUMENT 25 john.doe@gmail.com")
        assert validated == {
            "type": "fx_spot",
            "instrument": "FX_INSTRUMENT",
            "size": 25,
            "email": "john.doe@gmail.com",
        }

    @pytest.mark.parametrize(
        "rfq_input, expected_error",
        [
            (
                "a b c",
                (
                    "Invalid RFQ format! Please enter a string with "
                    'this format: "<type> <instrument> <size> <email>"'
                ),
            ),
            (
                "fx_spot FX_INSTRUMENT invalid john.doe@gmail.com",
                "{'size': ['Not a valid number.']}",
            ),
        ],
    )
    def test_failure(self, rfq_input, expected_error):
        _, error = validate_rfq(rfq=rfq_input)
        assert error == expected_error


class TestPriceUtils:
    rfq_data = {
        "type": RfqType.FX.value,
        "instrument": "instrument",
        "size": "size",
        "email": "email",
    }

    @pytest.mark.asyncio
    async def test_get_price_data_success(self, monkeypatch):
        class HttpxAsyncClientMock:
            @staticmethod
            async def post(*args, **kwargs):
                class MockResponse:
                    @staticmethod
                    def raise_for_status():
                        pass

                    @staticmethod
                    def json():
                        return {"price": 300}

                return MockResponse()

        monkeypatch.setattr(httpx, "AsyncClient", HttpxAsyncClientMock)

        price_data = await get_price_data(
            httpx_client=httpx.AsyncClient(),
            rfq_data=self.rfq_data,
        )

        assert price_data == {"price": 300}

    @pytest.mark.asyncio
    async def test_get_price_data_failure_404(self, monkeypatch):
        class HttpxAsyncClientMock:
            @staticmethod
            async def post(*args, **kwargs):
                class MockResponse:
                    @staticmethod
                    def raise_for_status():
                        raise httpx.HTTPError("404")

                return MockResponse()

        monkeypatch.setattr(httpx, "AsyncClient", HttpxAsyncClientMock)

        with pytest.raises(httpx.HTTPError):
            await get_price_data(
                httpx_client=httpx.AsyncClient(),
                rfq_data=self.rfq_data,
            )

    @pytest.mark.asyncio
    async def test_get_price_data_failure_timeout(self, monkeypatch):
        class HttpxAsyncClientMock:
            @staticmethod
            async def post(*args, **kwargs):
                raise httpx.TimeoutException("timeout")

        monkeypatch.setattr(httpx, "AsyncClient", HttpxAsyncClientMock)

        with pytest.raises(httpx.TimeoutException):
            await get_price_data(
                httpx_client=httpx.AsyncClient(),
                rfq_data=self.rfq_data,
            )
