import asyncio
import websockets

async def mindbank_agent():
    uri = "ws://34.162.62.64:7576/ws/mindbank"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Agent Connected: Real-time test initiated.")
        while True:
            message = await websocket.recv()
            print(f"Received Real-Time Message: {message}")

asyncio.run(mindbank_agent())
