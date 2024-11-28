from decimal import Decimal

def is_decimal(string: str) -> bool:
    try:
        Decimal(string)
        return True
    except ValueError:
        return False
