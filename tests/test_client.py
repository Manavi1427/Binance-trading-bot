from bot.client import get_client

client = get_client()

print("Ping:", client.futures_ping())

print("Server Time:")
print(client.futures_time())

print("Account:")
print(client.futures_account())

print("Balance:")
print(client.futures_account_balance())