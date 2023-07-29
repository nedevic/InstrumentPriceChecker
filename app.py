import asyncio

import asyncclick
import httpx

from enums.rfq import RfqType
from logger import logger
from utils.price import get_price_data
from validators.rfq import validate_rfq


@asyncclick.command()
@asyncclick.option(
    "--rfq",
    required=True,
    help=(
        "Please enter a string with the following format: "
        '"<type> <instrument> <size> <email>". '
        f"<type> can be one of: {RfqType.get_allowed_types_info()}."
        "<instrument> is the name of the instrument. "
        "<size> is a positive decimal number. "
        "<email> is a valid email address of a customer."
    ),
)
async def main(rfq: str):
    rfq_data, error = validate_rfq(rfq=rfq)

    if error:
        logger.error(error)
        return

    logger.info(f'Fetching the price for the following rfq: "{rfq}"')
    try:
        async with httpx.AsyncClient() as client:
            price_data = await get_price_data(
                httpx_client=client,
                rfq_data=rfq_data,
            )
            logger.info(f'The price for this rfq is: {price_data["price"]}')
    except Exception as error:
        logger.error(error)


if __name__ == "__main__":
    asyncio.run(main())
