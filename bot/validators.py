from decimal import Decimal,InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

class ValidationError(Exception):
    pass 

class Validator:
    def __init__(self, exchange_info):
        #initialize valiadtor with exchange metadata

        self.symbol_rules= {}

        for symbol_data in exchange_info["symbols"]:
            symbol = symbol_data["symbol"]

            filters = {
                f["filterType"] : f
                for f in symbol_data["filters"]
            }

            self.symbol_rules[symbol] = {
                "min_qty": Decimal(
                    filters["LOT_SIZE"]["minQty"]
                ),
                "max_qty": Decimal(
                    filters["LOT_SIZE"]["maxQty"]
                ),
                "step_size": Decimal(
                    filters["LOT_SIZE"]["stepSize"]
                ),
                "tick_size": Decimal(
                    filters["PRICE_FILTER"]["tickSize"]
                ),
                "min_price": Decimal(
                    filters["PRICE_FILTER"]["minPrice"]
                ),
                "max_price": Decimal(
                    filters["PRICE_FILTER"]["maxPrice"]
                ),
            }

@staticmethod
def valid_side(side):
    #validate buy/sell

    side = side.upper()
    if side not in VALID_SIDES:
        raise ValidationError(
            f"Invalid side, {side} choose from {VALID_SIDES}"
        )
    return side 





