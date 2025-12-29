import asyncio
import sys
import os

# Add parent directory to path to allow importing config and app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telethon import TelegramClient
from config import Config

async def main():
    print("Starting interactive Telegram session setup...")
    
    try:
        # Initialize the client using the configuration
        client = TelegramClient(
            Config.TELEGRAM_SESSION_FILE_PATH,
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
        
        # This will trigger the interactive login flow if the session is missing or invalid
        await client.start()
        
        print("Session setup complete!")
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} (ID: {me.id})")
        
        await client.disconnect()
        
    except ValueError as e:
        print("\n[ERROR] Configuration error.")
        print(f"Reason: {e}")
        print("Please check your .env file for TELEGRAM_API_ID and TELEGRAM_API_HASH.")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == '__main__':
    asyncio.run(main())
