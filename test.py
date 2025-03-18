import asyncio
import websockets
import json


async def chat():
    uri = "ws://127.0.0.1:8000/ws/chat/"
    async with websockets.connect(uri) as websocket:
        # await websocket.send(json.dumps({"message": "Hello, WebSocket!"}))
        response = await websocket.recv()
        print("Received:", response)


asyncio.run(chat())
