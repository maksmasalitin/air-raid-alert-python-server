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

    await initialize_telegram_client(app)

    asyncio.create_task(start_websocket_server(app))
    print("WebSocket server started and accepting connections")

    return app
