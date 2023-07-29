import enum


class RfqType(enum.Enum):
    FX = "fx_spot"
    GOLD = "gold_call"
    BOND = "bond"

    @staticmethod
    def get_allowed_types() -> list:
        return [instrument_type.value for instrument_type in RfqType]

    @staticmethod
    def get_allowed_types_info() -> str:
        return ", ".join(f'"{value}"' for value in RfqType.get_allowed_types())
