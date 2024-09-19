import asyncio
from binance.client import Client
from telegram import Bot
import schedule
import time

api = "YOUR API"
secret = "YOUR SECRET"
client_futures = Client(api, secret)
TOKEN = "YOUR TOKEN"
CHAT_ID = "YOUR CHAT-ID"  

async def get_futures_balance(asset='USDT'):
    try:
        futures_account_info = client_futures.futures_account()
        wallet_balance = 0.0
        unrealized_profit = 0.0
        total_balance = 0.0

        for asset_info in futures_account_info['assets']:
            if asset_info['asset'] == asset:
                wallet_balance = float(asset_info['walletBalance'])
                unrealized_profit = float(asset_info['unrealizedProfit'])
                total_balance = wallet_balance + unrealized_profit
                break
        
        telegram_mesaj = f"Toplam bakiyemiz {total_balance} {asset}"
        return telegram_mesaj
    
    except Exception as e:
        print("Hata:", e)
        return None

async def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

async def job():
    usdt_balance = await get_futures_balance('USDT')
    if usdt_balance:
        await send_telegram_message(usdt_balance)
    else:
        await send_telegram_message("Bakiye yok.")

schedule.every().hour.at(":48").do(asyncio.run, job())

while True:
    schedule.run_pending()
    time.sleep(1)
