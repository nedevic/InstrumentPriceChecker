from marshmallow import ValidationError

from schemas.rfq_schema import RfqSchema


def validate_rfq(rfq: str):
    validated_data = None
    error = None

    try:
        if rfq.count(" ") != 3:  # 4 entries separated by 3 spaces
            raise ValueError

        type_, instrument, size, email = rfq.split()

        validated_data = RfqSchema().load(
            {
                "type": type_,
                "instrument": instrument,
                "size": size,
                "email": email,
            }
        )

    except ValueError:
        error = (
            "Invalid RFQ format! Please enter a string with "
            'this format: "<type> <instrument> <size> <email>"'
        )

    except ValidationError as err:
        error = str(err.messages)

    return validated_data, error
