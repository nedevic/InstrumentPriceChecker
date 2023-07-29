import httpx

from enums.rfq import RfqType

ENDPOINTS = {
    RfqType.FX.value: "https://5j4oy.mocklab.io/fx",
    RfqType.GOLD.value: "https://5j4oy.mocklab.io/gold",
    RfqType.BOND.value: "https://5j4oy.mocklab.io/bond",
}


async def get_price_data(httpx_client: httpx.AsyncClient, rfq_data: dict) -> dict:
    type_, instrument, size, email = (
        rfq_data[key] for key in ["type", "instrument", "size", "email"]
    )
    response = await httpx_client.post(
        url=ENDPOINTS[type_],
        timeout=1,
        json={
            "instrument": instrument,
            "size": size,
            "email": email,
        },
    )
    response.raise_for_status()
    return response.json()
