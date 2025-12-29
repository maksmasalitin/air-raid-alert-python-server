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
    
    print("\n" + "="*60)
    print(f"WebSocket server started at: ws://localhost:6789")
    print("Instruction: To connect, send your AUTH_KEY as the FIRST message.")
    print("="*60 + "\n")

    return app
