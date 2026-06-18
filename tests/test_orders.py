from bot.client import get_client
from bot.orders import OrderManager

client = get_client()

order_manager = OrderManager(client)

response = order_manager.place_market_order(
    symbol="BTCUSDT",
    side="BUY",
    quantity="0.001"
)

print(response)