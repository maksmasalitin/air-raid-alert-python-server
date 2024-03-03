import asyncio
import threading
from telethon import TelegramClient, events
from .models import AirRaidAlertMessageParser
from .websocket_server import send_event

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
    async def create_client():
        return TelegramClient(app.config.TELEGRAM_SESSION_FILE_PATH,
                              app.config.TELEGRAM_API_ID,
                              app.config.TELEGRAM_API_HASH)

    async def run_client():
        client = await create_client()
        chats = [AirRaidAlertMessageParser.CHANNEL_NAME]
        client.add_event_handler(lambda e: event_handler(app, client, e), events.NewMessage(chats=chats))
        await client.start()
        await fetch_initial_alerts(client, app.country)
        await update_clients(app.country)
        await client.run_until_disconnected()

    threading.Thread(target=lambda: asyncio.run(run_client()), daemon=True).start()

async def fetch_initial_alerts(client, country):
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
