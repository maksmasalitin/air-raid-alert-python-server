import asyncio
import threading
from telethon import TelegramClient, events
from .models import AirRaidAlertMessageParser

async def event_handler(app, client, socketio, event):
    message = event.message
    message_parser = AirRaidAlertMessageParser(message)
    region_id = message_parser.region_id()

    if region_id is None:
        print("Unknown region in message: %s" % message_parser.text)
        return

    event_data = {
        'region_id': region_id,
        'timestamp': message_parser.timestamp.isoformat() if message_parser.timestamp else None,
        'event': 'air_raid_alert' if message_parser.is_an_air_raid_alert() else 'air_raid_end'
    }

    # Update the country status based on the message type
    with app.app_context():
      if message_parser.is_an_air_raid_alert():
          app.country.air_raid_alert(region_id, message_parser.timestamp)
      else:
          app.country.air_raid_end(region_id, message_parser.timestamp)

    socketio.emit('event', event_data)

def initialize_telegram_client(app, socketio):
    async def create_client():
        return TelegramClient('Map manager', app.config['TELEGRAM_API_ID'], app.config['TELEGRAM_API_HASH'])

    async def run_client():
        client = None
        while True:
            try:
                if client:
                    await client.disconnect()

                client = await create_client()
                client.add_event_handler(lambda e: event_handler(app, client, socketio, e),
                                         events.NewMessage(chats=[AirRaidAlertMessageParser.CHANNEL_NAME]))
                await client.start()
                await async_fetch_initial_alerts(client, app.country)
                await client.run_until_disconnected()
            except OSError as e:
                print(f"Network error encountered: {e}. Retrying...")
            except Exception as e:
                print(f"Unexpected error: {e}. Attempting to reconnect...")
            finally:
                if client:
                    await client.disconnect()
                await asyncio.sleep(5)  # Delay before retrying

    async def async_telegram_operations():
        await run_client()

    threading.Thread(target=lambda: asyncio.run(async_telegram_operations()), daemon=True).start()



async def async_fetch_initial_alerts(client, country):
    for tag, region_id in AirRaidAlertMessageParser.REGION_MAP.items():
        messages = await client.get_messages(AirRaidAlertMessageParser.CHANNEL_NAME, search=tag, limit=1)
        if messages:
            message_parser = AirRaidAlertMessageParser(messages[0])
            if message_parser.is_an_air_raid_alert():
                country.air_raid_alert(region_id, message_parser.timestamp)
            else:
                country.air_raid_end(region_id, message_parser.timestamp)
