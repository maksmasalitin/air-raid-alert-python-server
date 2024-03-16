from threading import Thread
import asyncio
from config import Config
from .models import Country
from .telegram import initialize_telegram_client
from .websocket_server import start_websocket_server

async def create_app():
    app = type('App', (object,), {})()
    app.country = Country()
    app.config = Config

    telegram_client = await initialize_telegram_client(app)
    telegram_task = asyncio.create_task(telegram_client.run_until_disconnected())

    websocket_task = asyncio.create_task(start_websocket_server(app))

    app.tasks = [telegram_task, websocket_task]
    print("WebSocket server started and accepting connections")

    return app
