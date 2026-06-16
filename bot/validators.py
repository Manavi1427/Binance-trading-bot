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

def validate_order_type(order_type):
    #validate market/limit
    order_type = order_type.upper()

    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type {order_type}, Choose from {VALID_ORDER_TYPES}"
        )
    
    return order_type


def validate_symbol(self, symbol):
    #validate trading symbol

    symbol = symbol.upper()
    if symbol not in self.symbol_rules:
        raise ValidationError(
            f"Invalid symbol {symbol}"
        )
    return symbol

def validate_quantity(self, quanity,symbol):
    #Validate quanitity using binance lot rules

    try:
        quanity= Decimal(str(quanity))
    except InvalidOperation:
        raise ValidationError(
            "Quanity must be numeric"
        )
    
    rules = self.symbol_rules["symbol"]

    if quanity < rules["min_qty"]:
        raise ValidationError(
            f"Quantity must be gretater than {rules["min_qty"]}"
        )
    
    if quanity > rules["max_qty"]:
        raise ValidationError(
            f"Quantity must be greater than {rules["max_qty"]}"
        )
    
    step = rules["step_size"]

    remainder = quanity % step

    if remainder != 0:
        raise ValidationError(
            f"Quantity must follow step size {step}"
        )
    
    return quanity

def validate_price(
        self,
        price,
        symbol,
        order_type
    ):
        """
        Validate LIMIT order price.
        """

        if order_type != "LIMIT":
            return None

        if price is None:
            raise ValidationError(
                "LIMIT orders require a price."
            )

        try:
            price = Decimal(str(price))

        except InvalidOperation:
            raise ValidationError(
                "Price must be numeric."
            )

        rules = self.symbol_rules[symbol]

        if price < rules["min_price"]:
            raise ValidationError(
                f"Price cannot be below "
                f"{rules['min_price']}."
            )

        if price > rules["max_price"]:
            raise ValidationError(
                f"Price cannot exceed "
                f"{rules['max_price']}."
            )

        tick_size = rules["tick_size"]

        remainder = price % tick_size

        if remainder != 0:
            raise ValidationError(
                f"Price must follow tick size "
                f"{tick_size}."
            )

        return price

def validate_order(
        self,
        symbol,
        side,
        order_type,
        quantity,
        price=None
    ):
        """
        Validate an entire order request.
        """

        symbol = self.validate_symbol(symbol)

        side = self.validate_side(side)

        order_type = self.validate_order_type(
            order_type
        )

        quantity = self.validate_quantity(
            quantity,
            symbol
        )

        price = self.validate_price(
            price,
            symbol,
            order_type
        )

        return {
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "quantity": quantity,
            "price": price,
        }








