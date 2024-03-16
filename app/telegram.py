import asyncio
import threading
from telethon import TelegramClient, events
from .models import AirRaidAlertMessageParser
from .websocket_server import send_event
## If you want to see telethon logs, uncomment the next lines
# import logging
#
# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

async def event_handler(app, client, event):
    message = event.message
    message_parser = AirRaidAlertMessageParser(message)
    region_id = message_parser.region_id()

    if region_id is None:
        print("Unknown region in message: %s" % message_parser.text)
        return

    if message_parser.is_an_air_raid_alert():
        app.country.air_raid_alert(region_id)
    else:
        app.country.air_raid_end(region_id)

    await update_clients(app.country)

async def initialize_telegram_client(app):
    client = TelegramClient(app.config.TELEGRAM_SESSION_FILE_PATH,
                            app.config.TELEGRAM_API_ID,
                            app.config.TELEGRAM_API_HASH,
                            sequential_updates=True)

    chats = [AirRaidAlertMessageParser.CHANNEL_NAME]
    client.add_event_handler(lambda e: event_handler(app, client, e), events.NewMessage(chats=chats))
    await client.start()
    print('Telegram client started!')
    await async_fetch_initial_alerts(client, app.country)
    await update_clients(app.country)

    return client

async def async_fetch_initial_alerts(client, country):
    for tag, region_id in AirRaidAlertMessageParser.REGION_MAP.items():
        messages = await client.get_messages(AirRaidAlertMessageParser.CHANNEL_NAME, search=tag, limit=1)
        if messages:
            message_parser = AirRaidAlertMessageParser(messages[0])
            if message_parser.is_an_air_raid_alert():
                country.air_raid_alert(region_id)
            else:
                country.air_raid_end(region_id)

async def update_clients(country):
    event_data = country.get_active_air_raid_regions()
    send_event(event_data)
    print("Sent data message: %s" % event_data)
