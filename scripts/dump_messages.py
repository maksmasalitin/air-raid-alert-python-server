import asyncio
import datetime
import sys
import os

# Add parent directory to path to allow importing config and app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from telethon import TelegramClient
from config import Config
from app.models.air_raid_alert_message_parser import AirRaidAlertMessageParser

async def main():
    print("Starting message dump...")
    
    # Calculate the date 2 weeks ago
    two_weeks_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14)
    print(f"Fetching messages since: {two_weeks_ago}")

    try:
        client = TelegramClient(
            Config.TELEGRAM_SESSION_FILE_PATH,
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
        await client.start()

        channel = AirRaidAlertMessageParser.CHANNEL_NAME
        count = 0
        
        with open('messages.log', 'w', encoding='utf-8') as f:
            # reverse=True fetches oldest first, but here we iterate normally (newest first)
            # wait, if we want "last 2 weeks", commonly we iterate backwards from now until the date.
            async for message in client.iter_messages(channel, offset_date=None, reverse=False):
                if message.date < two_weeks_ago:
                    break
                
                if message.text:
                    f.write(f"--- {message.date} ---\n")
                    f.write(f"{message.text}\n")
                    f.write("-" * 30 + "\n")
                    count += 1
                    if count % 100 == 0:
                        print(f"Processed {count} messages...")

        print(f"Finished. Dumped {count} messages to messages.log")
        await client.disconnect()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
