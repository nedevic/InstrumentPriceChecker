from marshmallow import Schema, ValidationError, fields, validate

from enums.rfq import RfqType


def _validate_type(type_):
    if type_ not in RfqType.get_allowed_types():
        raise ValidationError(
            f"type must have one of these values: {RfqType.get_allowed_types_info()}"
        )


class RfqSchema(Schema):
    type = fields.String(required=True, validate=_validate_type)
    instrument = fields.String(required=True)
    size = fields.Float(required=True, validate=validate.Range(min=0))
    email = fields.Email(required=True)
