import asyncio
import sys
import os

# Add parent directory to path to allow importing config and app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, AuthKeyError
from config import Config
from app.models.air_raid_alert_message_parser import AirRaidAlertMessageParser

async def main():
    print("Checking Telegram session status...")

    try:
        client = TelegramClient(
            Config.TELEGRAM_SESSION_FILE_PATH,
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
        
        # Try to connect. If not authorized, client.connect() succeeds but is_user_authorized() is False.
        # However, we want to catch actual auth errors during interaction.
        await client.connect()

        if not await client.is_user_authorized():
            print("\n[ERROR] Session is invalid or user is not authorized.")
            print("Action Required:")
            print("1. Stop the running server (if it is running).")
            print("2. Run 'python setup_session.py' to interactively log in.")
            print("3. Re-run this script to verify.")
            print("4. Start the server again.")
            await client.disconnect()
            sys.exit(1)

        me = await client.get_me()
        print(f"Session is valid. Logged in as: {me.first_name} (ID: {me.id})")

        print(f"Fetching last message from {AirRaidAlertMessageParser.CHANNEL_NAME}...")
        messages = await client.get_messages(AirRaidAlertMessageParser.CHANNEL_NAME, limit=1)
        
        if messages:
            last_msg = messages[0]
            print("\n--- Last Alert Message ---")
            print(f"Date: {last_msg.date}")
            print(f"Text: {last_msg.text}")
            print("--------------------------\n")
        else:
            print(f"No messages found in {AirRaidAlertMessageParser.CHANNEL_NAME}.")

        await client.disconnect()
        sys.exit(0)

    except (SessionPasswordNeededError, ValueError) as e:
        # ValueError can happen if the API ID/Hash are invalid
        print("\n[ERROR] Authentication failed or session is invalid.")
        print(f"Reason: {e}")
        print("\nAction Required:")
        print("1. Stop the running server (if it is running).")
        print("2. Run 'python setup_session.py' to interactively log in.")
        print("3. Re-run this script to verify.")
        print("4. Start the server again.")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
