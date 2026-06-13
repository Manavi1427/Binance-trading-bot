from bot.client import get_client

client = get_client()

print("connected succesfully")
print(client.futures_account_balance)
