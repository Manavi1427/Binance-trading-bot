# bot/orders.py

from binance.exceptions import (
    BinanceAPIException,
    BinanceOrderException
)


class OrderManager:
    """
    Handles all Binance order execution logic.
    """

    def __init__(self, client):
        self.client = client

    def place_market_order(
        self,
        symbol,
        side,
        quantity
    ):
        """
        Place a MARKET order.
        """

        try:
            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=str(quantity)
            )

            return self._format_response(response)

        except BinanceOrderException as e:
            raise RuntimeError(
                f"Order Error: {e}"
            )

        except BinanceAPIException as e:
            raise RuntimeError(
                f"Binance API Error: {e.message}"
            )

        except Exception as e:
            raise RuntimeError(
                f"Unexpected Error: {str(e)}"
            )

    def place_limit_order(
        self,
        symbol,
        side,
        quantity,
        price
    ):
        """
        Place a LIMIT order.
        """

        try:
            response = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                quantity=str(quantity),
                price=str(price),
                timeInForce="GTC"
            )

            return self._format_response(response)

        except BinanceOrderException as e:
            raise RuntimeError(
                f"Order Error: {e}"
            )

        except BinanceAPIException as e:
            raise RuntimeError(
                f"Binance API Error: {e.message}"
            )

        except Exception as e:
            raise RuntimeError(
                f"Unexpected Error: {str(e)}"
            )

    def place_order(
        self,
        symbol,
        side,
        order_type,
        quantity,
        price=None
    ):
        """
        Generic order dispatcher.
        """

        order_type = order_type.upper()

        if order_type == "MARKET":
            return self.place_market_order(
                symbol,
                side,
                quantity
            )

        if order_type == "LIMIT":
            return self.place_limit_order(
                symbol,
                side,
                quantity,
                price
            )

        raise ValueError(
            f"Unsupported order type: {order_type}"
        )

    @staticmethod
    def _format_response(response):
        """
        Return only useful fields from Binance response.
        """

        return {
            "order_id": response.get("orderId"),
            "symbol": response.get("symbol"),
            "status": response.get("status"),
            "side": response.get("side"),
            "type": response.get("type"),
            "orig_qty": response.get("origQty"),
            "executed_qty": response.get("executedQty"),
            "price": response.get("price"),
            "avg_price": response.get("avgPrice"),
            "client_order_id": response.get(
                "clientOrderId"
            ),
        }