from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
import redis.asyncio as redis
import os

app = FastAPI()

redis_client = redis.from_url(
    f"redis://:{os.getenv('MINDBANK_REDIS_PASSWORD')}@{os.getenv('MINDBANK_REDIS_HOST')}:{os.getenv('MINDBANK_REDIS_PORT')}/0",
    decode_responses=True
)

connected_clients = set()

@app.websocket("/ws/mindbank")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await redis_client.publish('mindbank-channel', data)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe('mindbank-channel')
    async for message in pubsub.listen():
        if message['type'] == 'message':
            for client in connected_clients:
                await client.send_text(message['data'])

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())
