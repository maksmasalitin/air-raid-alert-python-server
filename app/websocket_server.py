import asyncio
import websockets
import json

connected_clients = set()

async def websocket_handler(websocket, path, app):
    connected_clients.add(websocket)
    print(f"New client connection!")
    try:
        auth_key = await websocket.recv()
        if auth_key in app.config.AUTH_KEYS:
            active_regions = app.country.get_active_air_raid_regions()
            await websocket.send(json.dumps(active_regions))
            await websocket.wait_closed()
        else:
            await websocket.send(json.dumps({'error': 'Authentication failed'}))
            await websocket.close()
    except websockets.exceptions.ConnectionClosed:
        print(f"Connection closed by client")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connected_clients.discard(websocket)
        print(f"Client disconnected!")

async def start_websocket_server(app):
    async with websockets.serve(lambda ws, path: websocket_handler(ws, path, app), "localhost", 6789):
        await asyncio.Future()  # This will run forever unless cancelled

def send_event(event_data):
    for websocket in connected_clients:
        asyncio.create_task(websocket.send(json.dumps(event_data)))
